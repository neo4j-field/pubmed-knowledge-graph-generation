
from Bio import Entrez
import time
import json
import xml.etree.ElementTree as ET

# Replace with your email (required by NCBI)
Entrez.email = "your_email@solarahealth.org"

def search_pubmed(term, max_results=3):
    """Searches PubMed and returns a list of PMIDs."""
    handle = Entrez.esearch(db="pmc", term=term, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

def extract_title_from_xml(xml_text):
    """Extract article title from PMC XML."""
    try:
        # Parse the XML
        root = ET.fromstring(xml_text)
        title_temp = ""
        # Look for title in various possible locations
        # Method 1: article-title in article-meta
        title_elem = root.find('.//article-title')
        if title_elem is not None:
            title_temp =  ''.join(title_elem.itertext()).strip()
        
        # Method 2: title-group
        title_group = root.find('.//title-group/article-title')
        if title_group is not None:
            title_temp = ''.join(title_group.itertext()).strip()
        
        # Method 3: Look in front matter
        front_title = root.find('.//front//article-title')
        if front_title is not None:
            title_temp = ''.join(front_title.itertext()).strip()
        
        return title_temp.replace("/", "_").replace("\\", "_").replace(" ", "_")
        
    except ET.ParseError as e:
        return f"XML parsing error: {e}"
    except Exception as e:
        return f"Error extracting title: {e}"

def fetch_articles(pmid_list):
    """Fetches article summaries (title, abstract) from PubMed."""
    ids = ",".join(pmid_list)
    with Entrez.efetch(db="pmc", id=ids, rettype="full", retmode="full") as handle:
        return handle.read()

def fetch_single_article(pmid):
    """Fetches a single article from PubMed."""
    with Entrez.efetch(db="pmc", id=pmid, rettype="full", retmode="full") as handle:
        return handle.read()

# def fetch_articles_detailed(pmid_list):
#     """Fetch article metadata using efetch in medline format."""
#     ids = ",".join(pmid_list)
#     with Entrez.efetch(db="pmc", id=ids, rettype="medline", retmode="text") as handle:
#         return handle.read()

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

    print(f"🔍 Searching PMC for: {query}")
    ids = search_pubmed(query, max_results=3)
    print(f"🔗 Found {len(ids)} articles")


    if ids:
        for id in ids:
            print(f"Fetching article {id}")
            xml_text = fetch_single_article(id)
            title = extract_title_from_xml(xml_text)
            print(f"Title: {title}")
            save_results(xml_text, f"articles/{id}-{title}.xml")
            print(f"Saved article {id} to {title}.xml")
    else:
        print("❌ No articles found")
