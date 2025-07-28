
// Sample Cypher to link Procedures and Drugs to OntologyConcepts (e.g., MeSH, SNOMED, RxNorm)

// Create example OntologyConcepts
MERGE (oc1:OntologyConcept {id: "D012345", name: "Metformin", source: "MeSH"})
MERGE (oc2:OntologyConcept {id: "C0011860", name: "HbA1c Test", source: "UMLS"})
MERGE (oc3:OntologyConcept {id: "RXN123456", name: "GLP-1 receptor agonists", source: "RxNorm"})
MERGE (oc4:OntologyConcept {id: "C0011849", name: "Type 2 Diabetes Mellitus", source: "UMLS"});

// Link Drugs to OntologyConcepts
MATCH (d:Drug {name: "Metformin"}), (o:OntologyConcept {name: "Metformin"})
MERGE (d)-[:IN]->(o);

MATCH (d:Drug {name: "GLP-1"}), (o:OntologyConcept {name: "GLP-1 receptor agonists"})
MERGE (d)-[:IN]->(o);

// Link Procedures to OntologyConcepts
MATCH (p:Procedure {code: "83036"}), (o:OntologyConcept {name: "HbA1c Test"})
MERGE (p)-[:IN]->(o);

// Link Conditions to OntologyConcepts
MATCH (c:Condition {code: "E11.9"}), (o:OntologyConcept {name: "Type 2 Diabetes Mellitus"})
MERGE (c)-[:IN]->(o);
