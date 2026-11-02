# Architecture & Approach

## Data flow

```
CSV | Selectable-text PDF | Manually-entered invoice
                         |
                         v
            Human verification / correction
                         |
                         v
            Session ledger (pandas DataFrame)
                         |
       +-----------------+--------------------+
       |                 |                    |
       v                 v                    v
  Finance summaries    Review engine     Scenario engine
  - sales              - blank GSTIN     - weekly receipts
  - purchases          - basic format    - weekly spending
  - receivables        - overdue bills   - known unpaid dues
       |                 |                    |
       +-----------------+--------------------+
                         v
              Streamlit + Plotly UX
                         |
              User-approved CSV export
                         |
              Optional consented LLM Q&A
```

## Why this architecture is practical

- **Deployable with a basic Streamlit Cloud account:** no container, external database, paid API key or server required.
- **Reproducible:** fixed synthetic demo dates and deterministic financial formulas; numbers can be traced to invoices.
- **Expandable:** `engine.py` separates domain logic from presentation. A database and role-based security can replace session storage.
- **Human in the loop:** tax and invoice values are reviewed by the owner; there is no automatic legal filing.

## Cash-flow simulation formula

For each week:

`Closing = Opening + expected scenario receipts + unpaid sales due − scenario costs − unpaid supplier payments due`

The next week's opening equals the previous week's closing. This is a **scenario projection**, not statistical prediction.

## Suggested production roadmap

1. Interview at least 15 micro-enterprise owners and accountants; record actual baseline time.
2. Add persistent database, authenticated accounts, encryption, audit logs and tenant isolation.
3. Integrate production-grade OCR with user correction and document-level confidence indicators.
4. Add verified compliance rule updates and CA review instead of guessing tax deadlines.
5. Apply privacy impact assessment, data retention, consent, and secure API access before processing real records.
6. Pilot with 25 micro-enterprises; measure admin time saved, extraction correction rate, usability and trust.
