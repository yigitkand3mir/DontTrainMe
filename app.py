import gradio as gr
import spacy
from faker import Faker
import re
import random
from docx import Document
import PyPDF2

fake = Faker("en_US")

try:
    nlp = spacy.load("xx_ent_wiki_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "xx_ent_wiki_sm"], check=True)
    nlp = spacy.load("xx_ent_wiki_sm")


def get_text_from_file(file):
    if file is None:
        return ""
    name = file.name.lower()
    if name.endswith((".txt", ".md")):
        return file.read().decode("utf-8")
    elif name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return ""


def find_extra_names(text):
    # Catch capitalized words that spaCy might miss
    pattern = r"\b([A-ZÀ-ÿ][a-zà-ÿ]+(?:\s+[A-ZÀ-ÿ][a-zà-ÿ]+){0,3})\b"
    return list(set(re.findall(pattern, text)))


def anonymize(text, seed=None):
    if not text or not text.strip():
        return "", {}

    if seed is not None:
        random.seed(seed)
        fake.seed_instance(seed)

    doc = nlp(text)
    replacements = {}

    for ent in doc.ents:
        if ent.label_ in ("PERSON", "ORG", "GPE", "LOC"):
            orig = ent.text.strip()
            if orig and orig not in replacements and len(orig) > 1:
                if ent.label_ == "PERSON":
                    replacements[orig] = fake.name()
                elif ent.label_ == "ORG":
                    replacements[orig] = fake.company()
                else:
                    replacements[orig] = fake.city()

    for name in find_extra_names(text):
        if name not in replacements and len(name) > 2 and not any(c.isdigit() for c in name):
            replacements[name] = fake.name()

    # Replace longer matches first
    for orig, new in sorted(replacements.items(), key=lambda x: -len(x[0])):
        text = re.sub(rf"\b{re.escape(orig)}\b", new, text)

    return text, replacements


def process(text_input, file_input, seed):
    text = (text_input or "").strip()
    if file_input:
        file_text = get_text_from_file(file_input)
        if file_text:
            text = f"{text}\n\n{file_text}" if text else file_text

    if not text.strip():
        return "Please enter text or upload a file.", {}, ""

    seed_val = int(seed) if seed else None
    anonymized, mapping = anonymize(text, seed=seed_val)

    if not mapping:
        return anonymized, {}, "No names or entities found."

    mapping_str = "\n".join(f"• {old} → {new}" for old, new in mapping.items())
    return anonymized, mapping, mapping_str


with gr.Blocks(title="DontDisplay", theme=gr.themes.Soft()) as demo:
    gr.HTML("""
    <div style="text-align:center; margin-bottom:20px">
        <h1 style="font-size:2.4em; margin-bottom:8px">🛡️ DontDisplay</h1>
        <p style="font-size:1.15em; color:#555">Hide names, companies and places in your prompts • Works in any language</p>
    </div>
    """)

    with gr.Row():
        with gr.Column():
            text_in = gr.Textbox(label="Text", placeholder="Paste your prompt here...", lines=14)
            file_in = gr.File(label="Upload file (.txt / .md / .docx / .pdf)", file_types=[".txt", ".md", ".docx", ".pdf"])
            with gr.Row():
                seed_in = gr.Number(label="Seed (optional)", precision=0)
                gr.Button("Random Seed", size="sm").click(lambda: random.randint(100000, 999999), outputs=seed_in)
            gr.Button("Anonymize", variant="primary", size="lg").click(
                process, inputs=[text_in, file_in, seed_in], outputs=["Anonymized Text", "Mapping", "Changed Entities"]
            )

        with gr.Column():
            out_text = gr.Textbox(label="Anonymized Text", lines=14, interactive=False)
            mapping_json = gr.JSON(label="Mapping")
            mapping_box = gr.Textbox(label="Changed Entities", lines=8, interactive=False)
            with gr.Row():
                gr.Button("Copy Anonymized Text").click(lambda x: x, inputs=out_text, outputs=out_text)
                gr.Button("Clear").click(lambda: ("", None, "", {}, ""), outputs=[text_in, file_in, out_text, mapping_json, mapping_box])

    gr.Markdown("""
    ### How it works
    - Detects person names, organizations and locations using multilingual NLP
    - Replaces them with realistic fake data (different every run unless you use a seed)
    - Supports Turkish, English and many other languages
    - Nothing is stored. Everything runs in your session.
    """)


if __name__ == "__main__":
    demo.launch()