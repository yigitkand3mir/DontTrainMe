# 🛡️ DontDisplay

**Anonymize your LLM prompts safely** — Automatically hides names, companies, and locations worldwide.

## Features

- ✅ Detects and replaces **person names**, **organizations**, and **locations**
- ✅ Generates **different fake data every time** (reproducible with seed)
- ✅ Supports **text + file upload** (.txt, .md, .docx, .pdf)
- ✅ Shows clear **Mapping table** (Original → Fake)
- ✅ Works with **Turkish, English, and 20+ languages**
- ✅ Completely free & open source
- ✅ **No data is stored** — runs locally

## Usage

### Easiest Way (Web)

1. Go to the [Hugging Face Space](https://huggingface.co/spaces)
2. Paste your text or upload a file
3. Click **Anonymize**
4. Copy the result and paste it into any LLM

### Local Installation

```bash
git clone https://github.com/yigitkand3mir/DontDisplay.git
cd DontDisplay
pip install -r requirements.txt
python app.py
```

## How it works

1. Uses **multilingual spaCy** (`xx_ent_wiki_sm`) for Named Entity Recognition
2. Replaces entities with realistic fake data using **Faker**
3. Extra regex layer catches names spaCy might miss
4. Replaces longer matches first to avoid partial replacements

## Example

**Original:**
> John Smith met with Acme Corp in New York yesterday. Maria Garcia also joined the call from Istanbul.

**Anonymized:**
> Michael Brown met with NovaTech Inc. in London yesterday. Sophia Patel also joined the call from Berlin.

## Contributing

Pull requests and issues are welcome!

## License

MIT

---

Made for LLM users who care about privacy. Works globally.
