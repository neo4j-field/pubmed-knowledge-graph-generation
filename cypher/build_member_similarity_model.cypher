
// Sample data setup for Member Similarity Model

// Create Members
CREATE (m1:Member {id: 'P001'}),
       (m2:Member {id: 'P002'}),
       (m3:Member {id: 'P003'});

// Create Demographics
CREATE (d1:Demographic {age: 55, sex: 'M'}),
       (d2:Demographic {age: 57, sex: 'F'}),
       (d3:Demographic {age: 60, sex: 'M'});

// Link Members to Demographics
MATCH (m1:Member {id: 'P001'}), (d1:Demographic)
CREATE (m1)-[:HAS_DEMO]->(d1);
MATCH (m2:Member {id: 'P002'}), (d2:Demographic)
CREATE (m2)-[:HAS_DEMO]->(d2);
MATCH (m3:Member {id: 'P003'}), (d3:Demographic)
CREATE (m3)-[:HAS_DEMO]->(d3);

// Create Conditions
CREATE (c1:MedicalCondition {code: 'E11.9', name: 'Type 2 Diabetes'}),
       (c2:MedicalCondition {code: 'I10', name: 'Hypertension'});

// Link Members to Conditions
MATCH (m1:Member {id: 'P001'}), (c1:MedicalCondition)
CREATE (m1)-[:HAS_DIAGNOSIS]->(c1);
MATCH (m2:Member {id: 'P002'}), (c1:MedicalCondition)
CREATE (m2)-[:HAS_DIAGNOSIS]->(c1), (m2)-[:HAS_DIAGNOSIS]->(c2);
MATCH (m3:Member {id: 'P003'}), (c1:MedicalCondition), (c2:MedicalCondition)
CREATE (m3)-[:HAS_DIAGNOSIS]->(c1), (m3)-[:HAS_DIAGNOSIS]->(c2);

// Create Medications
CREATE (dMet:Medication {name: 'Metformin'}),
       (dGLP:Medication {name: 'GLP-1'}),
       (dSul:Medication {name: 'Sulfonylurea'});

// Link Members to Medications
MATCH (m1:Member {id: 'P001'}), (dMet:Medication), (dGLP:Medication)
CREATE (m1)-[:TAKES]->(dMet), (m1)-[:TAKES]->(dGLP);
MATCH (m2:Member {id: 'P002'}), (dMet:Medication), (dSul:Medication)
CREATE (m2)-[:TAKES]->(dMet), (m2)-[:TAKES]->(dSul);
MATCH (m3:Member {id: 'P003'}), (dMet:Medication)
CREATE (m3)-[:TAKES]->(dMet);

// Create Procedures
CREATE (pHbA1c:Procedure {code: '83036', name: 'HbA1c Test'});

// Link Members to Procedures
MATCH (m1:Member {id: 'P001'}), (pHbA1c:Procedure)
CREATE (m1)-[:UNDERWENT]->(pHbA1c);
MATCH (m2:Member {id: 'P002'}), (pHbA1c:Procedure)
CREATE (m2)-[:UNDERWENT]->(pHbA1c);
MATCH (m3:Member {id: 'P003'}), (pHbA1c:Procedure)
CREATE (m3)-[:UNDERWENT]->(pHbA1c);

// Create Lab Results
CREATE (l1:LabResult {name: 'A1C', value: 8.2}),
       (l2:LabResult {name: 'A1C', value: 6.7}),
       (l3:LabResult {name: 'A1C', value: 7.3});

// Link Members to Lab Results
MATCH (m1:Member {id: 'P001'}), (l1:LabResult)
CREATE (m1)-[:HAS_LAB]->(l1);
MATCH (m2:Member {id: 'P002'}), (l2:LabResult)
CREATE (m2)-[:HAS_LAB]->(l2);
MATCH (m3:Member {id: 'P003'}), (l3:LabResult)
CREATE (m3)-[:HAS_LAB]->(l3);
