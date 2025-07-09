
// Cypher script to load extended patient journey data from CSV

// Constraints (optional but recommended)
CREATE CONSTRAINT IF NOT EXISTS ON (m:Member) ASSERT m.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS ON (c:Condition) ASSERT c.code IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS ON (d:Drug) ASSERT d.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS ON (p:Procedure) ASSERT p.code IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS ON (l:LabResult) ASSERT (l.name, l.value) IS NODE KEY;
CREATE CONSTRAINT IF NOT EXISTS ON (o:Outcome) ASSERT o.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS ON (demo:Demographic) ASSERT (demo.age, demo.sex, demo.zip) IS NODE KEY;

LOAD CSV WITH HEADERS FROM 'file:///extended_patient_journey.csv' AS row
WITH row,
     split(row.medications, ', ') AS meds,
     toInteger(row.age) AS age,
     toFloat(row.lab_value) AS lab_val

MERGE (m:Member {id: row.member_id})
MERGE (demo:Demographic {age: age, sex: row.sex, zip: row.zip_code})
MERGE (m)-[:HAS_DEMO]->(demo)

MERGE (c:Condition {code: row.diagnosis_code, name: row.diagnosis})
MERGE (m)-[:HAS_DIAGNOSIS]->(c)

MERGE (p:Procedure {code: row.procedure_code, name: row.procedure_name})
MERGE (m)-[:UNDERWENT {date: date(row.visit_date)}]->(p)

MERGE (l:LabResult {name: row.lab_test, value: lab_val})
MERGE (m)-[:HAS_LAB {date: date(row.visit_date)}]->(l)

MERGE (o:Outcome {name: row.outcome})
MERGE (m)-[:ACHIEVES {date: date(row.visit_date)}]->(o)

FOREACH (drug IN meds |
  MERGE (d:Drug {name: drug})
  MERGE (m)-[:TAKES]->(d)
)
