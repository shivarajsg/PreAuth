from pathlib import Path

p = Path(r"c:\Users\KumarShiva\Downloads\PreAuth\rulebook_collection\domains\centene_dme_orthotics_prosthetics\rules\build_rules_data_107.py")
text = p.read_text(encoding="utf-8")

# 1. RULE-DME-107-039: oral anti- spasmodic
text = text.replace("oral anti-spasmodic drugs", "oral anti- spasmodic drugs")

# 2. RULE-DME-107-052: Start from A. Replacement necessary on Page 12
old_q52 = """              "Replacement requests for manual wheelchairs are medically"
              " necessary when documentation supports one of the following: A."
              " Replacement necessary due to loss, theft, or irreparable damage"
              " and both of the following: 1. Documentation supports continued"
              " medical necessity; 2. Replacement is with the same or similar"
              " equipment; B. All of the following: 1. Replacement is due to"
              " one of the following reasons: a. Replacement necessary after"
              " reasonable useful lifetime of five years or more; b. Change in"
              " member/enrollee status requiring different equipment than"
              " currently in use and growth features of current equipment have"
              " been maximized;\""""

new_q52 = """              "A. Replacement necessary due to loss, theft, or irreparable damage"
              " and both of the following: 1. Documentation supports continued"
              " medical necessity; 2. Replacement is with the same or similar"
              " equipment; B. All of the following: 1. Replacement is due to"
              " one of the following reasons: a. Replacement necessary after"
              " reasonable useful lifetime of five years or more; b. Change in"
              " member/enrollee status requiring different equipment than"
              " currently in use and growth features of current equipment have"
              " been maximized;\""""

text = text.replace(old_q52, new_q52)

# 3. RULE-DME-107-055: self- propel
text = text.replace("self-propel a manual wheelchair", "self- propel a manual wheelchair")

# 4. RULE-DME-107-056: Criterion A on Page 12
old_q56 = """              "Medically necessary when meeting all of the following: A. Less"
              " than 5 years old (as evident by the age/date of purchase"
              " information provided); B. Cost of repairs is less than the cost"
              " of replacement; C. Information is provided to support the need"
              " for repairs due to normal wear and tear, as opposed to"
              " abuse/misuse or overutilization (as based on review of previous"
              " repair history, age and overall condition).\""""

new_q56 = """              "Medically necessary when meeting all of the following: A. Less"
              " than 5 years old (as evident by the age/date of purchase"
              " information provided);\""""

text = text.replace(old_q56, new_q56)

p.write_text(text, encoding="utf-8")
print("Updated 4 quotes in build_rules_data_107.py")
