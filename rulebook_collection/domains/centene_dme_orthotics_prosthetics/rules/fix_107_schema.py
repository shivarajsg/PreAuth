import re
from pathlib import Path

p = Path(r"c:\Users\KumarShiva\Downloads\PreAuth\rulebook_collection\domains\centene_dme_orthotics_prosthetics\rules\build_rules_data_107.py")
text = p.read_text(encoding="utf-8")

text = text.replace('"operator": "AND"', '"operator": "ALL_OF"')
text = text.replace('"operator": "OR"', '"operator": "ANY_OF"')
text = text.replace('"expected_value":', '"value":')

def repl_page(m):
    p_num = int(m.group(1))
    return f'"source_page": {{"physical_page": {p_num}, "printed_page": "Page {p_num} of 24"}}'

text = re.sub(r'"source_page":\s*(\d+)', repl_page, text)

p.write_text(text, encoding="utf-8")
print("Fixed schema formatting in build_rules_data_107.py")
