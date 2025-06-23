
from Bio import Entrez
import time
import json

# Replace with your email (required by NCBI)
Entrez.email = "your_email@solarahealth.org"

def search_pubmed(term, max_results=25):
    """Searches PubMed and returns a list of PMIDs."""
    handle = Entrez.esearch(db="pubmed", term=term, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

def fetch_articles(pmid_list):
    """Fetches article summaries (title, abstract) from PubMed."""
    ids = ",".join(pmid_list)
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="abstract", retmode="text")
    return handle.read()

def fetch_articles_detailed(pmid_list):
    """Fetch article metadata using efetch in medline format."""
    ids = ",".join(pmid_list)
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
    return handle.read()

def save_results(results_text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(results_text)

if __name__ == "__main__":
    # Example 1: Drug-focused search
    query = "Metformin GLP-1 Type 2 Diabetes"

    # You can also try:
    # query = "HbA1c monitoring procedure"
    # query = "cardiovascular outcomes AND obesity"
    # query = "retinopathy AND screening AND diabetes"

    print(f"🔍 Searching PubMed for: {query}")
    ids = search_pubmed(query, max_results=20)
    print(f"🔗 Found {len(ids)} articles")

    # Fetch and save abstract text
    abstract_text = fetch_articles(ids)
    save_results(abstract_text, "pubmed_abstracts.txt")

    # Optionally fetch detailed metadata
    metadata_text = fetch_articles_detailed(ids)
    save_results(metadata_text, "pubmed_metadata.txt")

    print("✅ Articles saved to pubmed_abstracts.txt and pubmed_metadata.txt")
