
LOAD CSV WITH HEADERS FROM 'file:///import/patients.csv' AS row
MERGE (p:Patient {patient_id: row.patient_id})
SET p.age = toInteger(row.age),
    p.gender = row.gender;


LOAD CSV WITH HEADERS FROM 'file:///import/providers.csv' AS row
MERGE (pr:Provider {provider_id: row.provider_id})
SET pr.name = row.provider_name,
    pr.specialty = row.specialty;


LOAD CSV WITH HEADERS FROM 'file:///import/claims_with_all_codes.csv' AS row
MERGE (c:Claim {claim_id: row.claim_id})
SET c.date = date(row.date),
    c.type = row.claim_type,
    c.icd9 = row.icd9,
    c.cpt4 = row.cpt4,
    c.ndc = row.ndc,
    c.rxnorm = row.rxnorm
WITH c, row
MATCH (p:Patient {patient_id: row.patient_id})
MERGE (p)-[:HAS_CLAIM]->(c)
WITH c, row
MATCH (pr:Provider {provider_id: row.provider_id})
MERGE (c)-[:PROVIDED_BY]->(pr);


LOAD CSV WITH HEADERS FROM 'file:///import/patient_journey_with_providers.csv' AS row
MERGE (e:Event {event_id: row.event_id})
SET e.date = date(row.event_date),
    e.event_type = row.event_type
WITH e, row
MATCH (p:Patient {patient_id: row.patient_id})
MERGE (p)-[:HAS_EVENT]->(e);


LOAD CSV WITH HEADERS FROM 'file:///import/conditions.csv' AS row
MERGE (d:Diagnosis {code: row.icd9_code})
SET d.description = row.description
WITH d, row
MATCH (p:Patient {patient_id: row.patient_id})
MERGE (p)-[:HAS_CONDITION]->(d);


LOAD CSV WITH HEADERS FROM 'file:///import/care_gaps.csv' AS row
MERGE (g:CareGap {gap_id: row.gap_id})
SET g.description = row.description,
    g.status = row.status
WITH g, row
MATCH (p:Patient {patient_id: row.patient_id})
MERGE (p)-[:HAS_GAP]->(g);


LOAD CSV WITH HEADERS FROM 'file:///import/risk_scores.csv' AS row
MERGE (r:RiskScore {risk_id: row.risk_id})
SET r.score = toFloat(row.score),
    r.risk_group = row.risk_group
WITH r, row
MATCH (p:Patient {patient_id: row.patient_id})
MERGE (p)-[:HAS_RISK_SCORE]->(r);
