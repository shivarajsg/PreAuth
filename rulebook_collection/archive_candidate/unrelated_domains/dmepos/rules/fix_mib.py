import re
from pathlib import Path

p = Path(r"c:\Users\KumarShiva\Downloads\PreAuth\rulebook_collection\domains\centene_dme_orthotics_prosthetics\rules\build_rules_data_107.py")
text = p.read_text(encoding="utf-8")

# Replace missing_information_behavior lines
def repl_mib(m):
    val = m.group(1)
    if "Deny" in val:
        return '"missing_information_behavior": "FAIL_CONDITION",'
    elif "Route" in val or "peer" in val.lower() or "secondary" in val.lower():
        return '"missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",'
    elif "Check plan" in val or "InterQual" in val or "benefit" in val.lower():
        return '"missing_information_behavior": "CANNOT_DETERMINE",'
    else:
        return '"missing_information_behavior": "PEND_FOR_DOCUMENTATION",'

text = re.sub(r'"missing_information_behavior":\s*"(.*?)",', repl_mib, text)
p.write_text(text, encoding="utf-8")
print("Updated missing_information_behavior in build_rules_data_107.py")
