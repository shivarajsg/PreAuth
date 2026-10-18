import pandas as pd
df = pd.read_csv('rulebook_collection/domains/advanced_imaging/rules/guideline_coverage_inventory.csv')
for idx, r in df.iterrows():
    print(f"{r['guideline_id']:10s} | {r['physical_start_page']:4d} - {r['physical_end_page']:4d} | {r['printed_page_range']}")
