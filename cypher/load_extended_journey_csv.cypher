
// Cypher script to load extended patient journey data from CSV

// Constraints (optional but recommended)
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Member) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (c:MedicalCondition) REQUIRE c.code IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (c:MedicalCondition) REQUIRE c.name IS NODE KEY;
CREATE CONSTRAINT IF NOT EXISTS FOR (d:Medication) REQUIRE d.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Procedure) REQUIRE p.code IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (l:LabResult) REQUIRE (l.name, l.value) IS NODE KEY;
CREATE CONSTRAINT IF NOT EXISTS FOR (o:ClinicalOutcome) REQUIRE o.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (demo:Demographic) REQUIRE (demo.age, demo.sex, demo.zip) IS NODE KEY;

LOAD CSV WITH HEADERS FROM 'file:///extended_patient_journey.csv' AS row
WITH row,
     split(row.medications, ', ') AS meds,
     toInteger(row.age) AS age,
     toFloat(row.lab_value) AS lab_val

MERGE (m:Member {id: row.member_id})
MERGE (demo:Demographic {age: age, sex: row.sex, zip: row.zip_code})
MERGE (m)-[:HAS_DEMO]->(demo)

MERGE (c:MedicalCondition {icd10Code: row.diagnosis_code, name: row.diagnosis})
MERGE (m)-[:HAS_DIAGNOSIS]->(c)

MERGE (p:Procedure {code: row.procedure_code, name: row.procedure_name})
MERGE (m)-[:UNDERWENT {date: date(row.visit_date)}]->(p)

MERGE (l:LabResult {name: row.lab_test, value: lab_val})
MERGE (m)-[:HAS_LAB {date: date(row.visit_date)}]->(l)

MERGE (o:ClinicalOutcome {name: row.outcome})
MERGE (m)-[:ACHIEVES {date: date(row.visit_date)}]->(o)

FOREACH (med IN meds |
  MERGE (d:Medication {name: med})
  MERGE (m)-[:TAKES]->(d)
)
