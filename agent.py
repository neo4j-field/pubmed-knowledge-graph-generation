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
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent


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

config = {"configurable": {"thread_id": "1"}}

SYSTEM_PROMPT = """You are a Neo4j expert that knows how to write Cypher queries to address healthcare questions.
As a Cypher expert
* You must always ensure you have the data model schema to inform your queries
* If an error is returned from the database, you may refactor your query or ask the user to provide additional information
* If an empty result is returned, use your best judgement to determine if the query is correct."""

# This function will be called every time before the node that calls LLM
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
        max_tokens=500,
        start_on="human",
        end_on=("human", "tool"),
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