# FinSaarthi AI — Code Titan

> **Problem statement:** 3.1 (the first option under MSME Finance and Compliance; full official wording was truncated in the hackathon form screenshot)  
> **Team:** CODE TITAN  
> **Team leader:** MURALIDHAR SM  
> **Participation:** Solo participant  
> **Status:** Working Streamlit prototype with synthetic demo data

**FinSaarthi AI** is a finance-and-compliance workflow co-pilot for Indian micro-enterprises. It converts disconnected financial recordkeeping into an approachable dashboard, invoice ledger, GST document-readiness checks, transparent cash-flow scenario planning, credit document preparation, and guided business Q&A.

## Launch it on Streamlit Community Cloud (GitHub → streamlit.io)

1. Unzip this project. Keep **`app.py`, `engine.py`, and `requirements.txt` in the top/root folder** of your GitHub repository. Include `.streamlit/config.toml`, the `assets/` and `docs/` folders as well.
2. Create a new public GitHub repo (e.g., `finsaarthi-ai-code-titan`). Upload the unzipped files using **Add file → Upload files**, then commit. Do **not** upload the ZIP itself as the only file; Streamlit needs actual `.py` files.
3. Open **https://share.streamlit.io/** and sign in with GitHub. Click **Create app / New app**, select your repository and branch (usually `main`).
4. Set **Main file path** to `app.py`, and click **Deploy**. Streamlit Community Cloud installs libraries from `requirements.txt` automatically.
5. Share the generated `https://...streamlit.app` URL with the judges.

### Run locally

Requires Python 3.10–3.12 (3.11 recommended).

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Modules to show the judges

| Page | Working functionality |
|---|---|
| Command Center | Six-month synthetic ledger, revenue and spending charts, open invoices and prioritised actions |
| Invoice Studio | Search/filter/export, add invoices, mark paid/delete, import compatible CSV, parse selectable text from PDF |
| Compliance Hub | Basic GSTIN-format/blank-field and tax amount review; overdue payment alerts; checklist and CSV export |
| Cash-Flow Lab | Adjustable opening balance, future receipts/costs, time-window invoice cash flows and scenario graph |
| Credit Passport | Interactive financial-document checklist and downloadable preparation report (not credit scoring) |
| Ask FinSaarthi | Contextual rules-based question answering; optional user-authorised external AI if configured |
| About | System architecture, planned roadmap and transparent feature limitations |

### Optional AI connection

The assistant **works without any API key** using transparent, rules-based guidance. For optional LLM answers, create `OPENAI_API_KEY` in Streamlit Cloud **App settings → Secrets** (use `OPENAI_API_KEY = "..."`), then explicitly tick the option to send the current question and **summary figures** to the external model. Optional API usage can incur charges and requires network connectivity. **Never commit real keys**. The user's opt-in defaults to off.

### Data privacy & product limits

- Demo inputs are synthetic. All state is held **in Streamlit session memory**; refreshing/restarting a session can discard changes. There is no production database or login system.
- CSV import is supported. PDF processing extracts **selectable text**, *not OCR from scanned PDFs or images*. Image uploads are previewed for manual entry.
- Review flags are simple workflow checks, not tax-law determinations. The demo **does not file GST returns, verify GST registration, integrate banks, generate real credit scores, or guarantee loans**.
- Cash-flow projection is **an adjustable scenario formula**, not a trained predictive model.
- For real-world deployment: add consent management, authentication, encrypted persistent storage, OCR, verifiable tax-rule updates, audit trail and professional compliance review.

## Project structure

```text
app.py                   # Main Streamlit application, seven pages
engine.py                # Finance calculations, alerts and PDF text extraction
requirements.txt         # Deployment dependencies
.streamlit/config.toml   # Theme and UI settings
.streamlit/secrets.toml.example # Optional external API key example
assets/logo.svg          # Original logo
assets/dashboard_preview.png # Illustrative UI preview (not live data)
data/demo_invoices.csv   # Synthetic records
README.md
HACKATHON_SUBMISSION.txt # Copy-paste project text
docs/DEMO_SCRIPT.md      # 3-minute judge demo
 docs/ARCHITECTURE.md    # Technical architecture
 docs/LIMITATIONS.md     # Honest prototype limitations
 docs/FinSaarthi_AI_Code_Titan_Pitch_Deck.pptx
```

Built for the hackathon by **CODE TITAN** — **MURALIDHAR SM**, solo participant.
