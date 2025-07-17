"""
This script validates the entity graph.
"""
import os
import pandas as pd
from pyneoinstance import Neo4jInstance, load_yaml_file

config = load_yaml_file("pyneoinstance_config.yaml")

db_info = config['db_info']

validation_queries = config['validation_queries']

graph = Neo4jInstance(db_info.get('uri', os.getenv("NEO4J_URI", "neo4j://localhost:7687")), # use config value -> use env value -> use default value
                      db_info.get('user', os.getenv("NEO4J_USER", "neo4j")), 
                      db_info.get('password', os.getenv("NEO4J_PASSWORD", "password")))


def get_entity_graph_counts() -> tuple[dict[str, int], dict[str, int]]:
    """
    Get the node and relationship counts of the entity graph.
    """

    node_counts = {
        "Medication": {
                "count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medication_count']).loc[0, 'count'],
                "orphan_count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medication_orphan_count']).loc[0, 'count'],
                "domain_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medication_domain_rels']).loc[0, 'count'],
                "lexical_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medication_lexical_rels']).loc[0, 'count'],
        },
        "TreatmentArm": {
                "count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_treatment_arm_count']).loc[0, 'count'],
                "orphan_count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_treatment_arm_orphan_count']).loc[0, 'count'],
                "domain_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_treatment_arm_domain_rels']).loc[0, 'count'],
                "lexical_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_treatment_arm_lexical_rels']).loc[0, 'count'],
        },
        "ClinicalOutcome": {
                "count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_clinical_outcome_count']).loc[0, 'count'],
                "orphan_count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_clinical_outcome_orphan_count']).loc[0, 'count'],
                "domain_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_clinical_outcome_domain_rels']).loc[0, 'count'],
                "lexical_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_clinical_outcome_lexical_rels']).loc[0, 'count'],
        },
        "StudyPopulation": {
                "count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_study_population_count']).loc[0, 'count'],
                "orphan_count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_study_population_orphan_count']).loc[0, 'count'],
                "domain_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_study_population_domain_rels']).loc[0, 'count'],
                "lexical_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_study_population_lexical_rels']).loc[0, 'count'],
        },
        "MedicalCondition": {
                "count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medical_condition_count']).loc[0, 'count'],
                "orphan_count": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medical_condition_orphan_count']).loc[0, 'count'],
                "domain_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medical_condition_domain_rels']).loc[0, 'count'],
                "lexical_rels": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medical_condition_lexical_rels']).loc[0, 'count'],
        },
    }

    rel_counts = {
        "MedicationUsedInTreatmentArm": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medication_used_in_treatment_arm_count']).loc[0, 'count'],
        "TreatmentArmHasClinicalOutcome": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_treatment_arm_has_clinical_outcome_count']).loc[0, 'count'],
        "StudyPopulationHasMedicalCondition": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_study_population_has_medical_condition_count']).loc[0, 'count'],
        "StudyPopulationInTreatmentArm": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_study_population_in_treatment_arm_count']).loc[0, 'count'],
    }

    return node_counts, rel_counts

def get_entity_graph_properties() -> dict[str, pd.DataFrame]:
    """
    Get the properties of the entity graph.
    """
    node_props = {}
    rel_props = {
            "MedicationUsedInTreatmentArm": graph.execute_read_query(database=db_info['database'], query=validation_queries['get_medication_used_in_treatment_arm_properties']),
    }
    return node_props, rel_props



def calculate_relationship_status(count: int, expected: int) -> str:
    """
    Calculate the status of a count.
    """
    percent = count / expected

    if percent == 1:
        return '✅'
    elif percent > 0.7:
        return '🟡'
    else:
        return '❌' 

def calculate_node_status(count: int, orphan_count: int, domain_rels: int, lexical_rels: int) -> str:
    """
    Calculate the status of a node.
    """
    orphaned_percent = orphan_count / count

    if orphaned_percent > 0.5 or domain_rels == 0:
        return '❌'
    elif orphaned_percent > 0.2 or lexical_rels == 0:
        return '🟡'
    else:
        return '✅'

def generate_markdown_entity_graph_validation_report() -> str:
    """
    Generate a report of the entity graph validation.
    """
    node_counts, rel_counts = get_entity_graph_counts()
    node_props, rel_props = get_entity_graph_properties()

    analysis = f"""
# Entity Graph Validation

| Entity Node      | Count | Orphaned | Domain Rels | Lexical Rels | Status |
|------------------|-------|----------|-------------|--------------|--------|
| Medication       | {node_counts['Medication']['count']} | {node_counts['Medication']['orphan_count']} | {node_counts['Medication']['domain_rels']} | {node_counts['Medication']['lexical_rels']} | {calculate_node_status(node_counts['Medication']['count'], node_counts['Medication']['orphan_count'], node_counts['Medication']['domain_rels'], node_counts['Medication']['lexical_rels'])} |
| TreatmentArm     | {node_counts['TreatmentArm']['count']} | {node_counts['TreatmentArm']['orphan_count']} | {node_counts['TreatmentArm']['domain_rels']} | {node_counts['TreatmentArm']['lexical_rels']} | {calculate_node_status(node_counts['TreatmentArm']['count'], node_counts['TreatmentArm']['orphan_count'], node_counts['TreatmentArm']['domain_rels'], node_counts['TreatmentArm']['lexical_rels'])} |
| ClinicalOutcome  | {node_counts['ClinicalOutcome']['count']} | {node_counts['ClinicalOutcome']['orphan_count']} | {node_counts['ClinicalOutcome']['domain_rels']} | {node_counts['ClinicalOutcome']['lexical_rels']} | {calculate_node_status(node_counts['ClinicalOutcome']['count'], node_counts['ClinicalOutcome']['orphan_count'], node_counts['ClinicalOutcome']['domain_rels'], node_counts['ClinicalOutcome']['lexical_rels'])} |
| MedicalCondition | {node_counts['MedicalCondition']['count']} | {node_counts['MedicalCondition']['orphan_count']} | {node_counts['MedicalCondition']['domain_rels']} | {node_counts['MedicalCondition']['lexical_rels']} | {calculate_node_status(node_counts['MedicalCondition']['count'], node_counts['MedicalCondition']['orphan_count'], node_counts['MedicalCondition']['domain_rels'], node_counts['MedicalCondition']['lexical_rels'])}
| StudyPopulation  | {node_counts['StudyPopulation']['count']} | {node_counts['StudyPopulation']['orphan_count']} | {node_counts['StudyPopulation']['domain_rels']} | {node_counts['StudyPopulation']['lexical_rels']} | {calculate_node_status(node_counts['StudyPopulation']['count'], node_counts['StudyPopulation']['orphan_count'], node_counts['StudyPopulation']['domain_rels'], node_counts['StudyPopulation']['lexical_rels'])} |

| Entity Relationship | Count | Expected | Diff | Status |
|---------------------|-------|----------|------|--------|
| (:Medication)-[:USED_IN_TREATMENT_ARM]->(:TreatmentArm) | {rel_counts['MedicationUsedInTreatmentArm']} | {node_counts['TreatmentArm']['count']} | {node_counts['TreatmentArm']['count'] - rel_counts['MedicationUsedInTreatmentArm']} | {calculate_relationship_status(rel_counts['MedicationUsedInTreatmentArm'], node_counts['TreatmentArm']['count'])} |
| (:TreatmentArm)-[:HAS_CLINICAL_OUTCOME]->(:ClinicalOutcome) | {rel_counts['TreatmentArmHasClinicalOutcome']} | {node_counts['TreatmentArm']['count']} | {node_counts['TreatmentArm']['count'] - rel_counts['TreatmentArmHasClinicalOutcome']} | {calculate_relationship_status(rel_counts['TreatmentArmHasClinicalOutcome'], node_counts['TreatmentArm']['count'])} |
| (:StudyPopulation)-[:HAS_MEDICAL_CONDITION]->(:MedicalCondition) | {rel_counts['StudyPopulationHasMedicalCondition']} | {node_counts['StudyPopulation']['count']} | {node_counts['StudyPopulation']['count'] - rel_counts['StudyPopulationHasMedicalCondition']} | {calculate_relationship_status(rel_counts['StudyPopulationHasMedicalCondition'], node_counts['StudyPopulation']['count'])} |
| (:StudyPopulation)-[:IN_TREATMENT_ARM]->(:TreatmentArm) | {rel_counts['StudyPopulationInTreatmentArm']} | {node_counts['TreatmentArm']['count']} | {node_counts['TreatmentArm']['count'] - rel_counts['StudyPopulationInTreatmentArm']} | {calculate_relationship_status(rel_counts['StudyPopulationInTreatmentArm'], node_counts['TreatmentArm']['count'])} |

"""

    return analysis

def generate_rich_entity_graph_validation_report() -> str:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text

    console = Console()
    
    node_counts, rel_counts = get_entity_graph_counts()
    
    # Create Entity Nodes table with grouped headers
    nodes_table = Table(title="Entity Graph Validation - Nodes", show_header=True, header_style="bold magenta")
    
    # Add columns with sub-groupings
    nodes_table.add_column("Entity Node", style="cyan", no_wrap=True)
    nodes_table.add_column("Total", justify="right", style="white")
    nodes_table.add_column("Orphaned", justify="right", style="yellow")
    nodes_table.add_column("Domain Rels\nTotal", justify="right", style="blue", min_width=10)
    nodes_table.add_column("Domain Rels\nAvg/Node", justify="right", style="bright_blue", min_width=10)
    nodes_table.add_column("Lexical Rels\nTotal", justify="right", style="green", min_width=10)
    nodes_table.add_column("Lexical Rels\nAvg/Node", justify="right", style="bright_green", min_width=10)
    nodes_table.add_column("Status", justify="center", style="bold")
    
    # Add rows
    for entity_node, data in node_counts.items():
        # Calculate averages
        domain_avg = int(data['domain_rels'] / data['count']) if data['count'] > 0 else 0
        lexical_avg = int(data['lexical_rels'] / data['count']) if data['count'] > 0 else 0
        
        status = calculate_node_status(data['count'], data['orphan_count'], data['domain_rels'], data['lexical_rels'])
        nodes_table.add_row(
            entity_node,
            str(data['count']),
            str(data['orphan_count']),
            str(data['domain_rels']),
            str(domain_avg),
            str(data['lexical_rels']),
            str(lexical_avg),
            status
        )
    
    # Create Relationships table
    rels_table = Table(title="Entity Graph Validation - Relationships", show_header=True, header_style="bold magenta")
    rels_table.add_column("Relationship", style="cyan")
    rels_table.add_column("Actual", justify="right", style="white")
    rels_table.add_column("Expected", justify="right", style="white")
    rels_table.add_column("Missing", justify="right", style="red")
    rels_table.add_column("Status", justify="center", style="bold")
    
    # Add relationship rows
    rel_mappings = [
        ("(:Medication)-[:USED_IN_TREATMENT_ARM]->(:TreatmentArm)", 
         rel_counts['MedicationUsedInTreatmentArm'], 
         node_counts['TreatmentArm']['count']),
        ("(:TreatmentArm)-[:HAS_CLINICAL_OUTCOME]->(:ClinicalOutcome)", 
         rel_counts['TreatmentArmHasClinicalOutcome'], 
         node_counts['TreatmentArm']['count']),
        ("(:StudyPopulation)-[:HAS_MEDICAL_CONDITION]->(:MedicalCondition)", 
         rel_counts['StudyPopulationHasMedicalCondition'], 
         node_counts['StudyPopulation']['count']),
        ("(:StudyPopulation)-[:IN_TREATMENT_ARM]->(:TreatmentArm)", 
         rel_counts['StudyPopulationInTreatmentArm'], 
         node_counts['TreatmentArm']['count'])
    ]
    
    for rel_name, actual, expected in rel_mappings:
        missing = expected - actual
        status = calculate_relationship_status(actual, expected)
        rels_table.add_row(
            rel_name,
            str(actual),
            str(expected),
            str(missing),
            status
        )
    
    # Display tables
    console.print(Text("Entity Graph Validation", style="bold magenta"))
    console.print(nodes_table)
    console.print()
    console.print(rels_table)

if __name__ == "__main__":
    generate_rich_entity_graph_validation_report()

