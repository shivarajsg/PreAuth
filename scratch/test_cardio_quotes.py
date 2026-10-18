import fitz
import re
from pathlib import Path

base = Path("rulebook_collection/domains/cardiology/policy_pdfs/current_2026")
doc1 = fitz.open(base / "2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf")
doc2 = fitz.open(base / "2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf")
doc3 = fitz.open(base / "Cardiac Claim Edit - Stress Echo and Doppler Add-On.pdf")
doc4 = fitz.open(base / "Cardiovascular Service Group Grid_January2026.pdf")

def norm(text):
    text = text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()

def check_quote(doc, page_num, quote):
    p_text = norm(doc[page_num - 1].get_text("text"))
    q_text = norm(quote)
    if q_text in p_text:
        return True, "MATCH"
    else:
        return False, f"MISMATCH on p.{page_num}"

# Test a few sample quotes
q_preamble = "Where a specific clinical indication is not directly addressed in this guideline, medical necessity determination will be made based on clinical judgment"
print("Preamble Diag p.2:", check_quote(doc1, 2, q_preamble))

q_ccta = "Evaluation of patients with stable chest pain or anginal equivalent"
print("CCTA p.7:", check_quote(doc1, 7, q_ccta))
