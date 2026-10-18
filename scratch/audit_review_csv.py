import glob
import json
import csv
import os

review_queue_counts = {}
mismatches = []

for path in sorted(glob.glob('rulebook_collection/domains/*/rules/draft_rules.json')):
    dname = path.replace('\\', '/').split('/')[2]
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
        rules = data if isinstance(data, list) else data.get('rules', [])
    
    rules_needing_review = {r['rule_id']: r for r in rules if (r.get('status') or r.get('extraction_status')) == 'NEEDS_HUMAN_REVIEW'}
    
    # Check queue file: human_review_queue.csv
    queue_path = os.path.join(os.path.dirname(path), 'human_review_queue.csv')
    if os.path.isfile(queue_path):
        with open(queue_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            q_rows = list(reader)
            q_rule_ids = {row.get('rule_id') for row in q_rows if 'rule_id' in row}
            review_queue_counts[dname] = (len(rules_needing_review), len(q_rows))
            
            # Check if all rules_needing_review are in queue
            missing_in_q = set(rules_needing_review.keys()) - q_rule_ids
            extra_in_q = q_rule_ids - set(r['rule_id'] for r in rules)
            if missing_in_q:
                mismatches.append(f"{dname}: Rules needing review missing in queue: {missing_in_q}")
            if extra_in_q:
                mismatches.append(f"{dname}: Queue contains non-existent rule IDs: {extra_in_q}")
    else:
        review_queue_counts[dname] = (len(rules_needing_review), "NO_QUEUE_FILE")

print("Review Queue Summary per Domain (Rules Needing Review vs Queue Rows):")
for d, counts in review_queue_counts.items():
    print(f"  {d}: {counts[0]} rules needing review, {counts[1]} queue rows")

if mismatches:
    print("\nMismatches found:")
    for m in mismatches:
        print(f"  {m}")
else:
    print("\nAll review-needed rules perfectly match human_review_queue.csv records across all domains!")
