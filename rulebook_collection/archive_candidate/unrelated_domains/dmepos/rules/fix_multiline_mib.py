import re
from pathlib import Path

p = Path(r"c:\Users\KumarShiva\Downloads\PreAuth\rulebook_collection\domains\centene_dme_orthotics_prosthetics\rules\build_rules_data_107.py")
text = p.read_text(encoding="utf-8")

def repl_multiline_mib(m):
    block = m.group(1)
    if "Deny" in block:
        return '"missing_information_behavior": "FAIL_CONDITION",'
    elif "Route" in block or "Medical Director" in block or "Therapy Advisor" in block or "secondary" in block.lower():
        return '"missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",'
    elif "Check plan" in block or "InterQual" in block or "decision support" in block.lower() or "benefit" in block.lower():
        return '"missing_information_behavior": "CANNOT_DETERMINE",'
    else:
        return '"missing_information_behavior": "PEND_FOR_DOCUMENTATION",'

# Regex matches "missing_information_behavior": ( ... ),
text = re.sub(r'"missing_information_behavior":\s*\((.*?)\),', repl_multiline_mib, text, flags=re.DOTALL)

p.write_text(text, encoding="utf-8")
print("Successfully replaced multiline missing_information_behavior!")
