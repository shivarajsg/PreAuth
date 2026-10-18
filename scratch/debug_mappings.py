import os
import csv
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAINS_DIR = os.path.join(BASE_DIR, "rulebook_collection", "domains")

DOMAINS = [
    "advanced_imaging",
    "cardiology",
    "musculoskeletal_surgery",
    "interventional_pain_management",
    "radiation_oncology",
    "physical_medicine",
    "sleep_health",
    "genetic_testing",
    "centene_dme_orthotics_prosthetics",
]

active_rules = {}
for d in DOMAINS:
    rule_path = os.path.join(DOMAINS_DIR, d, "rules", "draft_rules.json")
    with open(rule_path, encoding="utf-8") as f:
        data = json.load(f)
        rules = data if isinstance(data, list) else data.get("rules", [])
        active_rules[d] = {r["rule_id"]: r for r in rules}

for d in DOMAINS:
    map_path = os.path.join(DOMAINS_DIR, d, "supporting_documents", "policy_rule_mapping.csv")
    with open(map_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        rule_id = r["rule_id"].strip()
        if rule_id and rule_id not in active_rules[d]:
            print(f"Domain {d}: rule_id {rule_id} not in active_rules! (mapping_id={r['mapping_id']})")
