import os
from PIL import Image, ImageDraw, ImageFont

def create_architecture_diagram():
    width = 1200
    height = 650
    img = Image.new("RGB", (width, height), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Header
    draw.text((600, 25), "KAVACH: 3-Checkpoint Security-Governed Agentic DevOps Architecture", fill="#0F172A", anchor="mm")
    draw.text((600, 50), "End-to-End Governance Topology: Untrusted Input -> In-Flight Planning & RAG -> Post-Flight AST Package Firewall", fill="#64748B", anchor="mm")

    # Local Perimeter Box
    draw.rectangle([(30, 80), (820, 600)], outline="#94A3B8", width=2, fill="#F8FAFC")
    draw.text((45, 95), "TRUST BOUNDARY: LOCAL / ON-PREMISE ENTERPRISE PERIMETER", fill="#475569")

    # Cloud Perimeter Box
    draw.rectangle([(850, 80), (1170, 600)], outline="#F87171", width=2, fill="#FEF2F2")
    draw.text((865, 95), "UNTRUSTED THIRD-PARTY CLOUD", fill="#DC2626")

    # Box 1: Developer Intent
    draw.rounded_rectangle([(50, 140), (240, 260)], radius=8, fill="#FFFFFF", outline="#CBD5E1", width=2)
    draw.text((145, 175), "Developer Intent", fill="#1E293B", anchor="mm")
    draw.text((145, 205), "Natural Language Prompt\n(Voice / Text / Hinglish)", fill="#64748B", anchor="mm")

    # Box 2: Pre-Flight Gate
    draw.rounded_rectangle([(270, 130), (510, 310)], radius=8, fill="#EFF6FF", outline="#3B82F6", width=2)
    draw.rectangle([(270, 130), (510, 160)], fill="#3B82F6")
    draw.text((390, 145), "CHECKPOINT 1: PRE-FLIGHT GATEWAY", fill="#FFFFFF", anchor="mm")
    draw.text((285, 175), "[*] Delimiter & Injection Shield", fill="#1E3A8A")
    draw.text((285, 205), "[*] Multilingual PII/SPDI Scanner", fill="#1E3A8A")
    draw.text((285, 235), "[*] Shannon Entropy Credential Check", fill="#1E3A8A")
    draw.text((285, 265), "[*] Zero-Knowledge Token Vault", fill="#1E3A8A")

    # Box 3: In-Flight Planning & RAG
    draw.rounded_rectangle([(540, 130), (800, 310)], radius=8, fill="#F0FDF4", outline="#22C55E", width=2)
    draw.rectangle([(540, 130), (800, 160)], fill="#22C55E")
    draw.text((670, 145), "CHECKPOINT 2: IN-FLIGHT RAG", fill="#FFFFFF", anchor="mm")
    draw.text((555, 175), "[*] Qdrant Dense Vector Retrieval", fill="#14532D")
    draw.text((555, 205), "[*] AST Call-Graph Dependency Tree", fill="#14532D")
    draw.text((555, 235), "[*] Hybrid Blast-Radius Scoring", fill="#14532D")
    draw.text((555, 265), "[*] Risk Policy Gate (ALLOW/REVIEW)", fill="#14532D")

    # Box 4: External Cloud LLM
    draw.rounded_rectangle([(870, 150), (1150, 290)], radius=8, fill="#FFFFFF", outline="#EF4444", width=2)
    draw.text((1010, 185), "Third-Party Cloud LLM", fill="#991B1B", anchor="mm")
    draw.text((1010, 210), "(Gemini 1.5 / Claude / GPT-4o)", fill="#DC2626", anchor="mm")
    draw.text((1010, 240), "Only Receives Scrubbed Tokens", fill="#B91C1C", anchor="mm")
    draw.text((1010, 260), "Zero Raw PII / Credentials Exfiltrated", fill="#7F1D1D", anchor="mm")

    # Box 5: Post-Flight AST Package Firewall & Generation
    draw.rounded_rectangle([(270, 360), (800, 560)], radius=8, fill="#FAF5FF", outline="#A855F7", width=2)
    draw.rectangle([(270, 360), (800, 390)], fill="#A855F7")
    draw.text((535, 375), "CHECKPOINT 3: POST-FLIGHT GENERATION & AST PACKAGE FIREWALL", fill="#FFFFFF", anchor="mm")

    # Sub-box 5A
    draw.rounded_rectangle([(285, 405), (525, 545)], radius=6, fill="#FFFFFF", outline="#D8B4FE", width=1)
    draw.text((405, 425), "AST Package Firewall", fill="#581C87", anchor="mm")
    draw.text((300, 450), "[*] Statically parse ast.Import", fill="#6B21A8")
    draw.text((300, 475), "[*] Whitelist STDLIB & internal", fill="#6B21A8")
    draw.text((300, 500), "[*] Verify against PyPI Registry", fill="#6B21A8")
    draw.text((300, 525), "[+] 100% Hallucination Catch Rate", fill="#047857")

    # Sub-box 5B
    draw.rounded_rectangle([(545, 405), (785, 545)], radius=6, fill="#FFFFFF", outline="#D8B4FE", width=1)
    draw.text((665, 425), "Closed-Loop Validation", fill="#581C87", anchor="mm")
    draw.text((560, 450), "[*] Sandboxed AST Reflexion Loop", fill="#6B21A8")
    draw.text((560, 475), "[*] Local Token Rehydration Vault", fill="#6B21A8")
    draw.text((560, 500), "[*] CycloneDX v1.5 SBOM Ledger", fill="#6B21A8")
    draw.text((560, 525), "[+] SLSA Level 3 Digital Attestation", fill="#047857")

    # Box 6: Verified Commit
    draw.rounded_rectangle([(50, 410), (240, 530)], radius=8, fill="#F0FDF4", outline="#16A34A", width=2)
    draw.text((145, 445), "Verified Commit / PR", fill="#15803D", anchor="mm")
    draw.text((145, 475), "CI/CD Security Gate Passed", fill="#166534", anchor="mm")
    draw.text((145, 500), "93.4% Validity | <47ms Overhead", fill="#15803D", anchor="mm")

    # Connecting Lines
    draw.line([(240, 200), (270, 200)], fill="#1E293B", width=2)
    draw.line([(510, 200), (540, 200)], fill="#1E293B", width=2)
    draw.line([(800, 200), (870, 200)], fill="#0284C7", width=2)
    draw.line([(1010, 290), (1010, 460), (800, 460)], fill="#A855F7", width=2)
    draw.line([(270, 470), (240, 470)], fill="#16A34A", width=2)

    output_path = os.path.join(os.path.dirname(__file__), "..", "figures", "figure1_architecture.png")
    img.save(output_path, "PNG")
    print(f"Generated {output_path}")

if __name__ == "__main__":
    create_architecture_diagram()
