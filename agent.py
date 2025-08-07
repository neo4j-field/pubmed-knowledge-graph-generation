import asyncio
import os

from dotenv import load_dotenv

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_core.messages.utils import (
    trim_messages, 
    count_tokens_approximately
)
from langchain_core.messages import AnyMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState

from langchain_core.tools import StructuredTool
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from openai import OpenAI

from pydantic import BaseModel, Field, field_validator
from pyneoinstance import Neo4jInstance, load_yaml_file


if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

neo4j_cypher_mcp = StdioServerParameters(
    command="uvx",
    args=["mcp-neo4j-cypher@0.3.0", "--transport", "stdio"],
    env={
            "NEO4J_URI": os.getenv("NEO4J_URI"), 
            "NEO4J_USERNAME": os.getenv("NEO4J_USERNAME"), 
            "NEO4J_PASSWORD": os.getenv("NEO4J_PASSWORD"),
            "NEO4J_DATABASE": os.getenv("NEO4J_DATABASE"),
        },
)


neo4j_config = load_yaml_file("pyneoinstance_config.yaml").get("db_info")

def _embed_text(text: str) -> list[float]:
    """
    Embed text using the OpenAI API.
    """

    embedding_client = OpenAI()
    response = embedding_client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        encoding_format="float",
        dimensions=768, # must be the same dimensions as the vector index
    )
    return response.data[0].embedding


def research_medication(medication_name: str, research_prompt: str) -> str:
    """
    Search the database for information about a specific medication.
    """

    if neo4j_config is None:
        raise ValueError("Neo4j config not found in `pyneoinstance_config.yaml` under `db_info` key")
    
    g = Neo4jInstance(uri=neo4j_config["uri"], user=neo4j_config["user"], password=neo4j_config["password"])

    query = """
call db.index.vector.queryNodes("chunk_vector_index", 10, $embedding)
yield node, score
with node
match p = (node)-[:HAS_NEXT_CHUNK]-(:Chunk)
where exists {(node)-[:HAS_ENTITY]->(:Medication {name: $medication_name})}
with nodes(p) as nodes
unwind nodes as n
with distinct n
match (n)-[:PART_OF_DOCUMENT]-(d:Document)
return n.id as chunk_id, 
       d.id as document_id, 
       d.name as document_title, 
       n.text as chunk_text
    """

    embedding = _embed_text(f"Medication: {medication_name}\n{research_prompt}")

    results_df = g.execute_read_query(query, 
                                      neo4j_config["database"],
                                      {"embedding": embedding, "medication_name": medication_name})
    return results_df.to_dict(orient="records")

class ResearchMedicationInput(BaseModel):
    medication_name: str = Field(..., description="The name of the medication to research. ")
    research_prompt: str = Field(..., description="A prompt describing the information desired about the medication.")

    @field_validator("medication_name")
    def validate_medication_name(cls, v: str) -> str:
        return v.lower()
    
research_medication_tool = StructuredTool.from_function(
    func=research_medication,
    name="research_medication",
    description="Research a medication by name and provide information about it.",
    args_schema=ResearchMedicationInput,
    return_direct=False,
)


config = {"configurable": {"thread_id": "1"}}

SYSTEM_PROMPT = """You are a Neo4j expert that knows how to write Cypher queries to address healthcare questions.
As a Cypher expert, when writing queries:
* You must always ensure you have the data model schema to inform your queries
* If an error is returned from the database, you may refactor your query or ask the user to provide additional information
* If an empty result is returned, use your best judgement to determine if the query is correct.

If using a tool that does NOT require writing a Cypher query, you do not need the database schema.

As a healthcare expert, when answering questions:
* Always provide citations in your responses that refer to the underlying documents
* Answers must always be grounded in the context you are provided"""


def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    """
    Returns a list of messages generated at runtime, based on input or configuration.

    Based on the documentation:
    https://langchain-ai.github.io/langgraph/agents/agents/#4-add-a-custom-prompt
    """
    filtered_messages = [msg for msg in state["messages"] if not isinstance(msg, ToolMessage)]
    return [{"role": "system", "content": SYSTEM_PROMPT}] + filtered_messages

def pre_model_hook(state):
    """
    This function will be called every time before the node that calls LLM.

    Documentation: 
    https://langchain-ai.github.io/langgraph/how-tos/create-react-agent-manage-message-history/?h=create_react_agent
    """
    trimmed_messages = trim_messages(
        state["messages"],
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=30_000,
        start_on="human",
        end_on=("human", "tool"),
        include_system=True,
    )
    # You can return updated messages either under `llm_input_messages` or 
    # To keep the original message history unmodified in the graph state and pass the updated history only as the input to the LLM, 
    #     return updated messages under `llm_input_messages` key
    # To overwrite the original message history in the graph state with the updated history, 
    #     return updated messages under `messages` key
    return {"llm_input_messages": trimmed_messages}

async def print_astream(async_stream, output_messages_key="llm_input_messages"):
    """
    Print the stream of messages from the agent.
    Based on the documentation:
    https://langchain-ai.github.io/langgraph/how-tos/create-react-agent-manage-message-history/?h=create_react_agent#keep-the-original-message-history-unmodified
    """

    async for chunk in async_stream:
        for node, update in chunk.items():
            print(f"Update from node: {node}")
            messages_key = (
                output_messages_key if node == "pre_model_hook" else "messages"
            )
            for message in update[messages_key]:
                if isinstance(message, tuple):
                    print(message)
                else:
                    message.pretty_print()

        print("\n\n")

async def main():
    """
    Main function to run the agent.

    Based on the documentation:
    https://github.com/langchain-ai/langchain-mcp-adapters?tab=readme-ov-file#client
    """
    async with stdio_client(neo4j_cypher_mcp) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # We only need to get schema and execute read queries
            allowed_tools = [tool for tool in tools if tool.name in {"get_neo4j_schema", "read_neo4j_cypher"}]
            allowed_tools.append(research_medication_tool)
            print("tools:")
            for tool in allowed_tools:
                print(tool)

            # Create and run the agent
            agent = create_react_agent("openai:gpt-4.1", 
                                       allowed_tools, 
                                       pre_model_hook=pre_model_hook, 
                                       checkpointer=InMemorySaver(),
                                       prompt=SYSTEM_PROMPT)
            
            print("\n===================================== Chat =====================================\n")

            while True:
                user_input = input("> ")
                if user_input.lower() in {"exit", "quit", "q"}:
                    break
                
                await print_astream(agent.astream({"messages": user_input}, config=config, stream_mode="updates"))

if __name__ == "__main__":
    asyncio.run(main())