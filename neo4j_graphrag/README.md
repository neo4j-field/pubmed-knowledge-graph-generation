# Neo4j GraphRAG Python Package Example

This directory contains knowledge graph generation code using the Neo4j GraphRAG Python Package. It is a single notebook that creates a pipeline to parse PDFs, extract entities, ingest data into Neo4j and perform some simple post processing.

## Differences From Main Notebooks
* No constraints or indexes for lexical and entity graphs
* Lexical graph has different labels, types and properties due to GraphRAG package internal configuration
* No custom post processing Cypher

## Known Bugs
* Running the notebook `1_generate_patient_graph.ipynb` will break the ingestion step of this notebook. This is because the constraints are incompatibile with how the knowledge graph generation module handles ingestion.
* Medication nodes are ingested with empty properties. An empty property should not exist, if it is not found. Here they are instead populated with empty strings or empty lists.
* Running the pipeline more than once for a document will generate duplicated lexical graph.