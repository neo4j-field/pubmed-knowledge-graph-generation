
// Load synthetic patient journey data

// Create constraints (optional for performance)
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Member) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (c:Condition) REQUIRE c.code IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (d:Drug) REQUIRE d.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Procedure) REQUIRE p.code IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (l:LabResult) REQUIRE (l.name, l.value) IS NODE KEY;
CREATE CONSTRAINT IF NOT EXISTS FOR (demo:Demographic) REQUIRE (demo.age, demo.sex, demo.zip) IS NODE KEY;

// Example for one row - parameterized loading can be used for batch

MERGE (m:Member {id: 'P001'})
MERGE (demo:Demographic {age: 65, sex: 'M', zip: '90210'})
MERGE (m)-[:HAS_DEMO]->(demo)
MERGE (cond:Condition {code: 'I10', name: 'Hypertension'})
MERGE (m)-[:HAS_DIAGNOSIS]->(cond)
MERGE (p:Procedure {code: '83036', name: 'HbA1c Test'})
MERGE (m)-[:UNDERWENT {date: date('2023-06-15')}]->(p)
MERGE (l:LabResult {name: 'A1C', value: 6.8})
MERGE (m)-[:HAS_LAB {date: date('2023-06-15')}]->(l)
MERGE (d:Drug {name: 'Metformin'})
MERGE (m)-[:TAKES]->(d)
MERGE (d2:Drug {name: 'GLP-1'})
MERGE (m)-[:TAKES]->(d2)
MERGE (o:Outcome {name: 'A1C Controlled'})
MERGE (m)-[:ACHIEVES {date: date('2023-06-15')}]->(o)
