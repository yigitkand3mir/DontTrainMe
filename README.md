# 🛡️ DontDisplay

**Anonymize your LLM prompts safely** — Automatically hides names, companies, and locations worldwide.

## ✨ Features
- ✅ Detects and replaces **person names**, **organizations**, and **locations**
- ✅ Generates **different fake data every time** (reproducible with seed)
- ✅ Supports **text + file upload** (.txt, .md, .docx, .pdf)
- ✅ Shows clear **Mapping table** (Original → Fake)
- ✅ Works with **Turkish, English, and 20+ languages**
- ✅ Completely free & open source
- ✅ **No data is stored** — everything runs locally

## 🚀 Usage

### Easiest Way (Web)
1. Go to the [Hugging Face Space](https://huggingface.co/spaces/yigitkand3mir/DontDisplay)
2. Paste your text or upload a file
3. Click **Anonymize**
4. Copy the result and paste it into any LLM

### Local Installation
```bash
git clone https://github.com/yigitkand3mir/DontDisplay.git
cd DontDisplay
pip install -r requirements.txt
python app.py
