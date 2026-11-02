"""Transparent, reproducible finance calculations for FinSaarthi AI's demonstration.
No claim of statutory GST determination, credit scoring or production-grade OCR.
"""
from __future__ import annotations
from datetime import date, timedelta
import io
import re
from typing import Dict
import numpy as np
import pandas as pd

REFERENCE_DAY = date(2026, 11, 2)
REQUIRED = ['invoice_id', 'date', 'due_date', 'customer', 'category', 'type', 'amount', 'tax_amount', 'gstin', 'status', 'notes']


def demo_invoices() -> pd.DataFrame:
    """Fixed synthetic transactions, never real user or customer data."""
    entities = [
        ('Green Valley Retail','Retail','Sale','33AABCG1234F1Z5'),
        ('Kaveri Supermart','Retail','Sale','33AAACK9988P1Z2'),
        ('Brightway Services','Services','Sale',''),
        ('Metro Distributors','Wholesale','Purchase','33AAACM2211C1Z9'),
        ('Sunrise Supplies','Supplies','Purchase','33AAACS1400E1Z4'),
        ('Lakshmi Traders','Wholesale','Sale','33AAACL5412D1Z7'),
        ('Nila Packaging','Supplies','Purchase',''),
        ('Vetri Stores','Retail','Sale','33AAACV4200L1Z3'),
    ]
    rows = []
    for i in range(36):
        name, cat, typ, gstin = entities[(i*5 + (i//8)) % len(entities)]
        base = REFERENCE_DAY - timedelta(days=165-i*5)
        amt = 7800 + (i*4783)%41000
        tax = round(amt * (0.18/1.18), 2)
        if i in (4, 23): gstin = ''
        if i == 20: tax = 0
        paid = i < 25 and i % 5 != 1
        due = base + timedelta(days=15 + i%12)
        if i>=29: due=REFERENCE_DAY + timedelta(days=5+(i-29)*4)
        rows.append({
            'invoice_id': f'CT-{2026}-{i+101:04d}', 'date': base.isoformat(),
            'due_date': due.isoformat(), 'customer':name,'category':cat,'type':typ,
            'amount':float(amt),'tax_amount':tax,'gstin':gstin,
            'status':'Paid' if paid else 'Unpaid', 'notes':'Synthetic demo invoice',
        })
    return pd.DataFrame(rows, columns=REQUIRED)


def clean_invoices(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    for col in REQUIRED:
        if col not in d: d[col] = '' if col not in ('amount','tax_amount') else 0.0
    for col in ('amount', 'tax_amount'):
        d[col] = pd.to_numeric(d[col], errors='coerce').fillna(0).clip(lower=0)
    for col in ('date','due_date'):
        d[col] = pd.to_datetime(d[col], errors='coerce').dt.strftime('%Y-%m-%d').fillna(REFERENCE_DAY.isoformat())
    for col in ('invoice_id','customer','category','gstin','notes'):
        d[col] = d[col].fillna('').astype(str).str.strip()
    d['type'] = d['type'].fillna('Sale').astype(str).str.title().where(lambda s:s.isin(['Sale','Purchase']),'Sale')
    d['status'] = d['status'].fillna('Unpaid').astype(str).str.title().where(lambda s:s.isin(['Paid','Unpaid']),'Unpaid')
    return d[REQUIRED].reset_index(drop=True)


def overview(df: pd.DataFrame) -> Dict[str,float]:
    d=clean_invoices(df)
    sales=d[d.type=='Sale']; buys=d[d.type=='Purchase']
    return {
        'revenue':round(float(sales.amount.sum()),2),
        'purchases':round(float(buys.amount.sum()),2),
        'receivable':round(float(sales.loc[sales.status=='Unpaid','amount'].sum()),2),
        'payable':round(float(buys.loc[buys.status=='Unpaid','amount'].sum()),2),
        'invoice_count':len(d),
        'net':round(float(sales.amount.sum()-buys.amount.sum()),2),
    }


def issues(df:pd.DataFrame, today:date=REFERENCE_DAY) -> pd.DataFrame:
    d=clean_invoices(df)
    out=[]
    for _,r in d.iterrows():
        problems=[]
        gstin=r.gstin.strip().upper()
        if not gstin: problems.append(('Missing GSTIN','Review', 'GSTIN field is blank; verify whether GST registration applies.'))
        elif not re.fullmatch(r'\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d]', gstin):
            problems.append(('GSTIN format check','Review', 'GSTIN does not match a basic 15-character format check.'))
        if float(r.tax_amount)==0:
            problems.append(('Tax amount check','Review','Zero tax recorded; confirm the applicable treatment.'))
        if r.status=='Unpaid' and date.fromisoformat(r.due_date)<today:
            problems.append(('Overdue payment','High','Due date has passed and the invoice is marked unpaid.'))
        for name,priority,message in problems:
            out.append({'Invoice':r.invoice_id,'Issue':name,'Priority':priority,'Detail':message})
    return pd.DataFrame(out, columns=['Invoice','Issue','Priority','Detail'])


def forecast(df:pd.DataFrame, opening_balance:float, projected_weekly_sales:float,
             projected_weekly_costs:float, weeks:int=8, today:date=REFERENCE_DAY) -> pd.DataFrame:
    d=clean_invoices(df)
    weeks=max(1,min(weeks,16))
    balance=opening_balance
    records=[]
    for week in range(weeks):
        start=today+timedelta(days=7*week)
        end=start+timedelta(days=6)
        due=pd.to_datetime(d.due_date,errors='coerce')
        unpaid=d[d.status=='Unpaid']
        relevant=unpaid[(pd.to_datetime(unpaid.due_date).dt.date>=start) & (pd.to_datetime(unpaid.due_date).dt.date<=end)]
        expected_in=float(relevant.loc[relevant.type=='Sale','amount'].sum())
        expected_out=float(relevant.loc[relevant.type=='Purchase','amount'].sum())
        income=projected_weekly_sales + expected_in
        expenses=projected_weekly_costs + expected_out
        balance=balance+income-expenses
        records.append({'Week':f'W{week+1}', 'Period':f'{start:%d %b}–{end:%d %b}',
                        'Expected inflows':round(income,2),'Expected outflows':round(expenses,2),
                        'Projected closing balance':round(balance,2)})
    return pd.DataFrame(records)


def monthly(df:pd.DataFrame)->pd.DataFrame:
    d=clean_invoices(df)
    d['period']=pd.to_datetime(d.date).dt.to_period('M')
    grouped=d.pivot_table(index='period',columns='type',values='amount',aggfunc='sum',fill_value=0)
    grouped=grouped.sort_index().reindex(columns=['Sale','Purchase'],fill_value=0).reset_index()
    grouped['Month']=grouped['period'].dt.strftime('%b %Y')
    return grouped[['Month','Sale','Purchase']]


def extract_pdf_details(data:bytes) -> dict:
    """Best-effort text extraction, NOT OCR. Always requires human verification."""
    from pypdf import PdfReader
    reader=PdfReader(io.BytesIO(data))
    text='\n'.join(page.extract_text() or '' for page in reader.pages[:5])[:25000]
    amount_matches=re.findall(r'(?:grand\s*total|invoice\s*total|amount\s*due|total)\s*[:₹Rs. ]*([\d,]+(?:\.\d{1,2})?)',text,re.I)
    gstin=re.findall(r'\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d]\b',text,re.I)
    ids=re.findall(r'(?:invoice\s*(?:no\.?|number|#))\s*[:# -]*([\w/-]+)',text,re.I)
    dates=re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b',text)
    amount=float(amount_matches[-1].replace(',','')) if amount_matches else None
    return {'raw_text':text,'amount':amount,'gstin':gstin[0].upper() if gstin else '',
            'invoice_id':ids[0] if ids else '', 'date':dates[0] if dates else ''}


def assistant(question:str,df:pd.DataFrame,lang:str='English') -> str:
    """Context-aware rule-based assistant; offline and always available.

    Outputs native-language Tamil/Hindi messages for supported task intents.
    This is not a trained language model, translation service, or legal adviser.
    """
    q=question.lower().strip()
    m=overview(df); alerts=issues(df)
    money=lambda x:f'₹{x:,.0f}'
    if any(w in q for w in ['gst','compliance','வரி','ஜிஎஸ்டி','जीएसटी']): intent='gst'
    elif any(w in q for w in ['cash','balance','flow','பணம்','नकद']): intent='cash'
    elif any(w in q for w in ['sales','revenue','income','விற்பனை','बिक्री']): intent='sales'
    elif any(w in q for w in ['loan','credit','finance','கடன்','ऋण']): intent='credit'
    elif any(w in q for w in ['invoice','bill','receipt','விலைப்பட்டியல்','इनवॉइस']): intent='invoice'
    else: intent='general'
    by_lang={
        'English':{
          'gst':f'There are {len(alerts)} invoice review flags. Check missing GSTINs, zero-tax entries, and overdue payments. These are basic checks, not GST filings or legal advice.',
          'cash':f'Unpaid customer invoices total {money(m["receivable"])}; unpaid supplier invoices total {money(m["payable"])}. Try Cash-Flow Lab to estimate your weekly balance.',
          'sales':f'Recorded demo sales total {money(m["revenue"])}. Customer receivables are {money(m["receivable"])}. These are synthetic values, not a bank balance.',
          'credit':'Use Credit Passport to review your loan document checklist. It is not a lender-issued credit score or loan approval.',
          'invoice':f'There are {m["invoice_count"]} invoices. You can search, add, upload a compatible CSV, or parse selectable text from PDF; always verify extracted fields.',
          'general':f'I can explain records, document-readiness checks, receivables, cash-flow scenarios and loan paperwork. This demo contains {m["invoice_count"]} invoices and {len(alerts)} review flags.'},
        'Tamil':{
          'gst':f'பதிவுகளில் {len(alerts)} சரிபார்ப்பு குறிப்புகள் உள்ளன. GSTIN, வரித் தொகை, நிலுவைப் பணம் ஆகியவற்றைச் சரிபார்க்கவும். இது GST தாக்கல் சேவை அல்ல.',
          'cash':f'வாடிக்கையாளர்களிடமிருந்து வரவேண்டிய தொகை {money(m["receivable"])}. சப்ளையர்களுக்குச் செலுத்த வேண்டியது {money(m["payable"])}. Cash-Flow Lab பகுதியில் பணப்புழக்கத்தை மதிப்பிடலாம்.',
          'sales':f'மாதிரி பதிவுகளின் மொத்த விற்பனை {money(m["revenue"])}. வரவேண்டிய தொகை {money(m["receivable"])}. இவை உண்மையான வங்கி இருப்புகள் அல்ல.',
          'credit':'Credit Passport பகுதியில் கடன் விண்ணப்பத்திற்கான ஆவணங்களின் பட்டியலைப் பார்க்கலாம். இது கடன் மதிப்பெண் அல்லது கடன் ஒப்புதல் அல்ல.',
          'invoice':f'இந்த மாதிரி கணக்கில் {m["invoice_count"]} இன்வாய்ஸ்கள் உள்ளன. Invoice Studio மூலம் பதிவுகளைச் சேர்க்கவும், தேடவும், CSV பதிவேற்றவும். எல்லா விவரங்களையும் உறுதிசெய்யவும்.',
          'general':f'இன்வாய்ஸ், வரித் தயார்நிலை, பணப்புழக்கம், கடன் ஆவணங்கள் குறித்த உதவிகளை வழங்க முடியும். இங்கு {m["invoice_count"]} மாதிரி பதிவுகள் உள்ளன.'},
        'Hindi':{
          'gst':f'इस डेमो में {len(alerts)} समीक्षा संकेत हैं। GSTIN, दर्ज टैक्स और बकाया भुगतान की जाँच करें। यह GST रिटर्न दाखिल करने या कानूनी सलाह का विकल्प नहीं है।',
          'cash':f'ग्राहकों से {money(m["receivable"])} प्राप्त होने हैं और सप्लायर्स को {money(m["payable"])} देने हैं। Cash-Flow Lab में साप्ताहिक अनुमान देखें।',
          'sales':f'डेमो रिकॉर्ड में कुल बिक्री {money(m["revenue"])} है। ग्राहकों से प्राप्तियाँ {money(m["receivable"])} हैं। ये वास्तविक बैंक डेटा नहीं हैं।',
          'credit':'Credit Passport में ऋण आवेदन के दस्तावेज़ों की सूची तैयार करें। यह क्रेडिट स्कोर या ऋण स्वीकृति नहीं है।',
          'invoice':f'इस डेमो में {m["invoice_count"]} इनवॉइस हैं। Invoice Studio में खोजें, नए रिकॉर्ड जोड़ें या CSV अपलोड करें। सभी विवरण सत्यापित करें।',
          'general':f'मैं इनवॉइस, GST तैयारी, नकदी प्रवाह और ऋण दस्तावेज़ों के बारे में जानकारी दे सकता हूँ। डेमो में {m["invoice_count"]} रिकॉर्ड हैं।'}}
    return by_lang.get(lang,by_lang['English'])[intent]
