"""FinSaarthi AI — deployable Streamlit demo by CODE TITAN (solo lead MURALIDHAR SM)."""
from __future__ import annotations
import html
import os
from datetime import date, timedelta
import uuid
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from engine import (REFERENCE_DAY, REQUIRED, demo_invoices, clean_invoices,
                    overview, issues, monthly, forecast, extract_pdf_details, assistant)

st.set_page_config(page_title='FinSaarthi AI | Code Titan', page_icon='🟢', layout='wide', initial_sidebar_state='expanded')

NAV=['✦  Command Center','▤  Invoice Studio','◈  Compliance Hub','↗  Cash-Flow Lab','◇  Credit Passport','✧  Ask FinSaarthi','◎  About the Project']
NAV_KEYS=['overview','invoices','compliance','cashflow','credit','assistant','about']
COLORS={'navy':'#101D38','ink':'#14213D','muted':'#6D7B90','teal':'#0CB69E','orange':'#F37A57','blue':'#5B79F3','bg':'#F5F7FC'}

CSS='''
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');
:root {--dark:#101D38;--teal:#0CB69E;--muted:#65758B;}
html,body,[class*="css"],button,input,.stMarkdown {font-family:'DM Sans',sans-serif!important;}
.block-container{padding-top:1.35rem;padding-bottom:3rem;max-width:1470px;}
[data-testid="stAppViewContainer"]{background:linear-gradient(135deg,#f7f9fd 0%,#f1f6fb 66%,#f6f9fb 100%);}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#101c35 0%,#132744 100%);}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#d5e3ee;}
[data-testid="stSidebar"] [data-testid="stRadio"] label{color:#e6eef5!important;padding:7px 10px;border-radius:12px;}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#233c58;}
[data-testid="stSidebar"] div[role="radiogroup"]{gap:6px;}
[data-testid="stSidebar"] .stRadio > label{display:none;}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"]{color:#fff!important;}
[data-testid="stSidebar"] div[data-testid="stButton"] button{background:#213956;color:white;border:1px solid #496078;}
h1,h2,h3,h4{font-family:'Manrope',sans-serif!important;letter-spacing:-.035em!important;color:#11213D;}
h1{font-size:2rem!important;font-weight:800!important;}
h2{font-size:1.4rem!important;font-weight:800!important;}
[data-testid="stMetric"]{background:#ffffff;border:1px solid #e4eaf1;border-radius:17px;padding:17px 20px;box-shadow:0 6px 20px rgba(15,30,65,.025);}
[data-testid="stMetricLabel"]{color:#6f7c8f!important;font-size:.88rem!important;}
[data-testid="stMetricValue"]{color:#111f39!important;font-weight:800;font-size:1.95rem!important;}
[data-testid="stMetricDelta"]{color:#07917d!important;}
.stButton>button[kind="primary"],.stDownloadButton>button[kind="primary"],div[data-testid="stFormSubmitButton"] button[kind="primary"]{background:#0ba993;color:white;border:none;border-radius:10px;min-height:42px;font-weight:700;}
.stButton>button,.stDownloadButton>button{border-radius:10px;font-weight:600;}
[data-testid="stVerticalBlockBorderWrapper"]{border-color:#e4eaf1!important;}
.stTabs [data-baseweb="tab-list"]{gap:12px;}
.stTabs [data-baseweb="tab"]{font-weight:700;border-radius:8px;}
div[data-testid="stAlert"]{border-radius:13px;}
.hero{background:radial-gradient(ellipse at 100% 0%,rgba(25,194,174,.21),transparent 37%),linear-gradient(110deg,#111F3B,#172F4B);color:white;padding:32px 36px;border-radius:22px;overflow:hidden;position:relative;margin-bottom:20px;border:1px solid #274057;}
.hero .eyebrow{font-size:10px;font-weight:800;letter-spacing:2.2px;color:#91e9d8;margin-bottom:13px;}
.hero .heading{font-family:Manrope,sans-serif;font-size:34px;line-height:1.17;font-weight:800;letter-spacing:-1.4px;max-width:780px;}
.hero .sub{font-size:14px;line-height:1.65;color:#bbcfdf;max-width:790px;margin-top:13px;}
.pill{display:inline-block;font-weight:800;letter-spacing:.7px;border:1px solid #a7eade;background:#e4faf4;color:#058773;padding:7px 11px;border-radius:99px;font-size:10px;margin:0 8px 10px 0;}
.smallcap{color:#687a90;font-size:12px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:6px;}
.note-card{padding:18px 20px;border:1px solid #e0e8f0;border-radius:14px;background:white;margin:6px 0 12px;box-shadow:0 4px 18px #172a4208;}
.note-card strong{font-family:Manrope,sans-serif;color:#172640;font-size:15px;}
.note-card p{color:#687a90;font-size:13px;line-height:1.55;margin:8px 0 0;}
.feature-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:12px 0;}
.feature{padding:21px 20px;border-radius:15px;background:white;border:1px solid #e3eaf0;min-height:148px;}
.feature .n{font-size:12px;color:#0ca893;font-weight:800;letter-spacing:1px;}
.feature h4{font-size:15px;margin:12px 0 8px;font-weight:800;}
.feature p{font-size:12px;color:#69788d;line-height:1.6;margin:0;}
.sectionbar{display:flex;justify-content:space-between;align-items:center;margin:4px 0 12px;}
.sectionbar .title{font-size:19px;font-weight:800;color:#16243c;}
.sectionbar .hint{font-size:11px;color:#8290a2;}
.footnote{font-size:11px;color:#8796a6;line-height:1.55;padding-top:10px;}
.project-banner{font-size:12px;color:#6a7990;margin-top:-4px;margin-bottom:14px;}
@media(max-width:740px){.hero{padding:25px 21px}.hero .heading{font-size:26px}.feature-grid{grid-template-columns:1fr}}
</style>
'''
st.markdown(CSS, unsafe_allow_html=True)

if 'invoices' not in st.session_state:
    st.session_state.invoices=demo_invoices()
if 'chatlog' not in st.session_state:
    st.session_state.chatlog=[]
if 'business_name' not in st.session_state:
    st.session_state.business_name='Kaveri Micro Enterprises (Demo)'
if 'credit_docs' not in st.session_state:
    st.session_state.credit_docs={'Registration / Udyam':True,'PAN / identity':True,'Recent invoices':True,'Bank statements':False,'GST-related records':False,'Profit and loss statement':False,'Business address proof':True}


def esc(v): return html.escape(str(v),quote=True)
def fmt(v:float)->str: return f'₹{v:,.0f}'
def chart_style(fig,height=335):
    fig.update_layout(height=height,margin=dict(l=14,r=14,t=20,b=15),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans',size=11,color='#64758A'),hovermode='x unified',legend=dict(orientation='h',y=1.12,x=0),xaxis=dict(showgrid=False,zeroline=False),yaxis=dict(gridcolor='#E9EEF4',zeroline=False))
    return fig

def page_title(kicker,title,description):
    st.markdown(f'<div class="smallcap">{esc(kicker)}</div>',unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="project-banner">{esc(description)}</div>',unsafe_allow_html=True)

def note(title,desc):
    st.markdown(f'<div class="note-card"><strong>{esc(title)}</strong><p>{esc(desc)}</p></div>',unsafe_allow_html=True)

with st.sidebar:
    st.markdown('''<div style="padding:15px 4px 19px"><div style="font-size:24px;font-weight:850;color:white;letter-spacing:-.9px">◈ FinSaarthi<span style="color:#2fdbc0"> AI</span></div><div style="letter-spacing:2px;color:#8baac3;font-size:10px;margin-top:7px">BY CODE TITAN  ·  2026</div></div>''',unsafe_allow_html=True)
    selected=st.radio('Navigate',NAV,label_visibility='collapsed')
    st.divider()
    st.markdown('<div style="color:#93b5c9;font-size:11px;letter-spacing:1.5px;font-weight:800">WORKSPACE</div>',unsafe_allow_html=True)
    st.markdown('<div style="color:white;font-size:13px;font-weight:700;margin:12px 0 5px">🟢 Live interactive demo</div><div style="color:#a7bccd;font-size:11px;line-height:1.6">All business figures are synthetic. Changes last for this browser session.</div>',unsafe_allow_html=True)
    if st.button('↺  Reset demo data',use_container_width=True):
        st.session_state.invoices=demo_invoices()
        st.session_state.chatlog=[]
        st.rerun()
    st.markdown('<div style="border-top:1px solid #34485d;margin-top:21px;padding-top:17px;color:#c3d3df;font-size:12px;line-height:1.9">TEAM  <b style="color:white">CODE TITAN</b><br>LEAD  <b style="color:white">MURALIDHAR SM</b><br>MODE  <b style="color:white">SOLO PARTICIPANT</b></div>',unsafe_allow_html=True)

page=NAV_KEYS[NAV.index(selected)]
df=clean_invoices(st.session_state.invoices)
st.session_state.invoices=df
m=overview(df)

if page=='overview':
    st.markdown('''<div class="hero"><div class="eyebrow">THE MSME FINANCE & COMPLIANCE CO-PILOT</div><div class="heading">Less paperwork.<br>More possibility.</div><div class="sub">Your business at a glance: invoices, payments, readiness and next actions — designed to make everyday financial operations feel effortless.</div><div style="margin-top:20px"><span style="color:#92e6d8;font-size:12px;font-weight:800">CAPTURE &nbsp; → &nbsp; COMPLY &nbsp; → &nbsp; GROW</span></div></div>''',unsafe_allow_html=True)
    st.markdown('<span class="pill">● INTERACTIVE PROTOTYPE</span><span class="pill">● SYNTHETIC DEMO DATA</span><span class="pill">● CODE TITAN</span>',unsafe_allow_html=True)
    st.markdown('<div class="sectionbar"><span class="title">Business pulse</span><span class="hint">Demo ledger · May–Nov 2026</span></div>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    a.metric('Total recorded sales',fmt(m['revenue']),help='Sum of sale invoices in this demo')
    b.metric('Customer receivables',fmt(m['receivable']),help='Unpaid sale invoices')
    c.metric('Supplier payables',fmt(m['payable']),help='Unpaid purchase invoices')
    d.metric('Documents to review',str(len(issues(df))),help='Invoice-level review flags, not tax violations')
    c1,c2=st.columns([1.7,1],gap='large')
    with c1:
        st.subheader('Income and spending')
        dmonth=monthly(df)
        fig=go.Figure()
        fig.add_bar(x=dmonth.Month,y=dmonth.Sale,name='Sales',marker_color='#0FC5A9',marker_line_width=0)
        fig.add_bar(x=dmonth.Month,y=dmonth.Purchase,name='Purchases',marker_color='#6B80E9',marker_line_width=0)
        fig.update_layout(barmode='group',bargap=.33)
        st.plotly_chart(chart_style(fig),use_container_width=True)
    with c2:
        st.subheader('Revenue mix')
        breakdown=df[df.type=='Sale'].groupby('category',as_index=False).amount.sum()
        fig=go.Figure(go.Pie(labels=breakdown.category,values=breakdown.amount,hole=.7,marker_colors=['#16BFA7','#5D7DEE','#FF9A69','#A3B7D2'],textinfo='percent'))
        fig.update_layout(height=335,margin=dict(l=8,r=8,t=8,b=8),showlegend=True,legend=dict(orientation='h',y=-.05),paper_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans',size=11,color='#64758A'))
        st.plotly_chart(fig,use_container_width=True)
    st.subheader('Recommended next actions')
    v=issues(df)
    high=v[v.Priority=='High']
    c1,c2,c3=st.columns(3)
    with c1: note('01  ·  Check overdue invoices',f'{len(high)} unpaid records require payment follow-up in the demo ledger.')
    with c2: note('02  ·  Review document fields',f'{len(v[v.Priority=="Review"])} basic GSTIN or tax amount checks need owner review.')
    with c3: note('03  ·  Model tomorrow’s cash','Use Cash-Flow Lab to stress-test your next eight weeks before committing spending.')
    st.markdown('<div class="footnote">Illustrative records only. Not financial advice, statutory filing software, a real bank feed or an audited report.</div>',unsafe_allow_html=True)

elif page=='invoices':
    page_title('01 / RECORDS','Invoice Studio','Capture, verify, import, and export business documents in one place.')
    t1,t2,t3=st.tabs(['Invoice ledger','Add an invoice','Import a file'])
    with t1:
        c1,c2,c3=st.columns([2,1,1])
        with c1: term=st.text_input('Search invoices',placeholder='Invoice ID, client, category…')
        with c2: status=st.selectbox('Payment status',['All','Paid','Unpaid'])
        with c3: typ=st.selectbox('Transaction type',['All','Sale','Purchase'])
        view=df.copy()
        if term: view=view[view.astype(str).apply(lambda col:col.str.contains(term,case=False,regex=False)).any(axis=1)]
        if status!='All': view=view[view.status==status]
        if typ!='All': view=view[view.type==typ]
        st.dataframe(view,hide_index=True,use_container_width=True,height=345,column_config={'amount':st.column_config.NumberColumn('Invoice total',format='₹ %.2f'),'tax_amount':st.column_config.NumberColumn('Recorded tax',format='₹ %.2f')})
        st.download_button('↓ Export filtered ledger (CSV)',view.to_csv(index=False).encode(),file_name='finsaarthi_invoice_ledger.csv',mime='text/csv')
        with st.expander('Update payment status / remove an invoice'):
            if len(df):
                selected_id=st.selectbox('Select invoice ID',df.invoice_id.tolist())
                c1,c2=st.columns(2)
                with c1:
                    if st.button('Mark as Paid',use_container_width=True):
                        st.session_state.invoices.loc[st.session_state.invoices.invoice_id==selected_id,'status']='Paid'
                        st.rerun()
                with c2:
                    if st.button('Delete invoice',use_container_width=True):
                        st.session_state.invoices=st.session_state.invoices[st.session_state.invoices.invoice_id!=selected_id].copy()
                        st.rerun()
    with t2:
        st.info('New entries are stored in this Streamlit session. Tax values and GSTINs are user supplied; they are not independently verified.')
        with st.form('manual_add',clear_on_submit=True):
            c1,c2=st.columns(2)
            with c1:
                inv_id=st.text_input('Invoice ID',value='INV-'+str(uuid.uuid4())[:6].upper())
                client=st.text_input('Customer / supplier',placeholder='Business name')
                kind=st.selectbox('Type',['Sale','Purchase'])
                amount=st.number_input('Invoice gross total (₹)',min_value=0.0,value=15000.0,step=500.0)
                tax=st.number_input('Recorded tax amount (₹)',min_value=0.0,value=0.0,step=100.0)
            with c2:
                issued=st.date_input('Invoice date',value=REFERENCE_DAY)
                due=st.date_input('Payment due date',value=REFERENCE_DAY+timedelta(days=15))
                category=st.selectbox('Category',['Retail','Services','Wholesale','Supplies','Manufacturing','Other'])
                gstin=st.text_input('GSTIN (if applicable)',placeholder='15-character GSTIN')
                payment=st.selectbox('Payment status',['Unpaid','Paid'])
            memo=st.text_input('Notes',placeholder='Optional reference')
            submit=st.form_submit_button('＋ Save invoice',type='primary',use_container_width=True)
            if submit:
                if not inv_id.strip() or not client.strip(): st.error('Enter an invoice ID and business name.')
                elif inv_id in df.invoice_id.values: st.error('Invoice ID already exists. Choose a unique ID.')
                elif due<issued: st.error('Payment due date cannot be earlier than invoice date.')
                elif tax>amount: st.error('Recorded tax cannot exceed the total invoice amount.')
                else:
                    new=dict(invoice_id=inv_id.strip(),date=issued.isoformat(),due_date=due.isoformat(),customer=client.strip(),category=category,type=kind,amount=amount,tax_amount=tax,gstin=gstin.strip(),status=payment,notes=memo)
                    st.session_state.invoices=pd.concat([df,pd.DataFrame([new])],ignore_index=True)
                    st.success('Invoice added to the session ledger. Open Invoice ledger to review.')
    with t3:
        st.markdown('### Import structured invoices')
        template=pd.DataFrame([{'invoice_id':'INV-2001','date':'2026-11-01','due_date':'2026-11-20','customer':'Demo Customer','category':'Retail','type':'Sale','amount':11800,'tax_amount':1800,'gstin':'33AAAAA1234A1Z5','status':'Unpaid','notes':'Replace sample'}])
        st.download_button('↓ Download CSV template',template.to_csv(index=False).encode(),file_name='invoice_import_template.csv',mime='text/csv')
        data=st.file_uploader('Upload CSV or selectable-text PDF (max 20 MB)',type=['csv','pdf','png','jpg','jpeg'])
        if data:
            if data.name.lower().endswith('.csv'):
                try:
                    imported=pd.read_csv(data)
                    missing=[x for x in ['invoice_id','date','due_date','customer','type','amount'] if x not in imported]
                    if missing: st.error('CSV is missing required columns: '+', '.join(missing))
                    else:
                        converted=clean_invoices(imported)
                        st.dataframe(converted.head(15),hide_index=True,use_container_width=True)
                        st.warning('Imported records are unverified. Review amounts and dates before using for decisions.')
                        if st.button('Import these records',type='primary'):
                            unique=converted[~converted.invoice_id.isin(df.invoice_id)]
                            st.session_state.invoices=pd.concat([df,unique],ignore_index=True)
                            st.success(f'Imported {len(unique)} distinct invoice(s); duplicates skipped.')
                except Exception as exc: st.error(f'CSV could not be read: {exc}')
            elif data.name.lower().endswith('.pdf'):
                try:
                    parsed=extract_pdf_details(data.getvalue())
                    st.markdown('#### Suggested values from selectable PDF text')
                    st.json({k:v for k,v in parsed.items() if k!='raw_text'})
                    with st.expander('Inspect extracted raw text'):
                        st.text(parsed['raw_text'][:4500] or 'No extractable text — probably a scanned PDF.')
                    st.info('Text extraction is not OCR. Scan/image PDFs need manual entry or a separately integrated OCR service. Verify suggestions before adding an invoice.')
                except Exception as exc: st.error(f'Could not extract PDF text: {exc}')
            else:
                st.image(data,caption='Image preview — enter verified fields in Add an invoice',width=450)
                st.info('Image OCR is a future integration. This prototype does not pretend to read photo invoices automatically.')

elif page=='compliance':
    page_title('02 / WORKFLOW','Compliance Hub','Prioritise missing data and payment follow-ups. Human-reviewed checks, not automated filings.')
    i=issues(df)
    a,b,c=st.columns(3)
    a.metric('Review flags',len(i))
    b.metric('High-priority follow-ups',len(i[i.Priority=='High']))
    c.metric('Invoices checked',len(df))
    st.subheader('Invoice review queue')
    if i.empty: st.success('No basic review flags found in the current records.')
    else:
        filter_issues=st.multiselect('Issue categories',options=sorted(i.Issue.unique()),default=sorted(i.Issue.unique()))
        st.dataframe(i[i.Issue.isin(filter_issues)],use_container_width=True,hide_index=True,height=350)
        st.download_button('↓ Export review queue',i.to_csv(index=False).encode(),file_name='compliance_review_queue.csv',mime='text/csv')
    st.subheader('A practical compliance preparation checklist')
    for task in ['Collect purchase and sales invoices','Check supplier identifiers (where applicable)','Verify recorded tax amounts with source documents','Reconcile with accountant / approved filing system','Review applicable official filing dates']:
        st.checkbox(task,key='compliance_'+task)
    st.warning('FinSaarthi AI does not submit GST returns, verify legal eligibility, set official due dates, or calculate a legally authoritative tax liability. Consult the GST portal or your professional adviser for current requirements.')

elif page=='cashflow':
    page_title('03 / PREDICTIVE PLANNING','Cash-Flow Lab','Explore a transparent scenario forecast based on planned weekly receipts, costs and unpaid invoice dates.')
    c1,c2,c3=st.columns(3)
    with c1: opening=st.number_input('Opening cash balance (₹)',min_value=0,max_value=100000000,value=180000,step=10000)
    with c2: weekly_in=st.slider('Additional weekly receipts (₹)',0,250000,45000,5000)
    with c3: weekly_out=st.slider('Additional weekly costs (₹)',0,250000,53000,5000)
    horizon=st.slider('Forecast horizon (weeks)',4,12,8)
    fc=forecast(df,opening,weekly_in,weekly_out,horizon)
    col1,col2,col3=st.columns(3)
    col1.metric('Week 1 closing balance',fmt(fc.iloc[0]['Projected closing balance']))
    col2.metric('Final forecast balance',fmt(fc.iloc[-1]['Projected closing balance']))
    col3.metric('Weeks below zero',int((fc['Projected closing balance']<0).sum()))
    st.subheader('Projected available cash')
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=fc.Week,y=fc['Projected closing balance'],mode='lines+markers',line=dict(color='#0DB9A6',width=4),marker=dict(size=9,color='#0DB9A6'),fill='tozeroy',fillcolor='rgba(13,185,166,.10)',name='Projected cash',hovertemplate='₹%{y:,.0f}<extra></extra>'))
    fig.add_hline(y=0,line_dash='dot',line_color='#EF8068')
    st.plotly_chart(chart_style(fig,380),use_container_width=True)
    if (fc['Projected closing balance']<0).any(): st.error('Scenario warning: projected balance falls below zero. Review payments, timing and liquidity needs.')
    else: st.success('In this scenario, no forecast week closes below zero. Test a worse-case cost or collections assumption.')
    with st.expander('See detailed weekly calculation and download forecast',expanded=False):
        st.dataframe(fc,use_container_width=True,hide_index=True)
        st.download_button('↓ Download scenario CSV',fc.to_csv(index=False).encode(),file_name='cashflow_scenario.csv',mime='text/csv')
    note('How the forecast works','Opening balance + projected weekly receipts + outstanding customer invoices due that week − weekly costs − outstanding supplier invoices due that week. Deterministic scenario modelling; not a machine-learning prediction.')

elif page=='credit':
    page_title('04 / GROWTH READINESS','Credit Passport','Organise the materials a lender may request. This is a document checklist, not a credit score.')
    st.markdown('### Prepare your business story for a lender')
    st.write('Mark the documents currently available. The completion indicator updates immediately.')
    with st.container(border=True):
        for name,initial in st.session_state.credit_docs.items():
            st.session_state.credit_docs[name]=st.checkbox(name,value=initial,key='document_'+name)
    ready=sum(st.session_state.credit_docs.values()); count=len(st.session_state.credit_docs)
    st.progress(ready/count,text=f'{ready} of {count} document categories ready · {ready/count:.0%} completeness')
    c1,c2,c3=st.columns(3)
    c1.metric('Document completeness',f'{ready}/{count}')
    c2.metric('Demo invoices available',len(df))
    c3.metric('Open customer invoices',len(df[(df.type=='Sale')&(df.status=='Unpaid')]))
    missing=[k for k,v in st.session_state.credit_docs.items() if not v]
    if missing: st.info('Suggested next documents to prepare: '+', '.join(missing)+'.')
    else: st.success('All demo document categories marked available. Actual lender requirements vary.')
    report=f"FinSaarthi AI | Credit Document Passport\nTeam: CODE TITAN | Lead: MURALIDHAR SM\nDemo date: {REFERENCE_DAY}\nBusiness: {st.session_state.business_name}\nThis is a document completeness checklist — NOT a credit score or lender decision.\n\n"+'\n'.join(f"{'[x]' if v else '[ ]'} {k}" for k,v in st.session_state.credit_docs.items())+f"\n\nDemo total sales: {fmt(m['revenue'])}\nDemo unpaid receivables: {fmt(m['receivable'])}\n"
    st.download_button('↓ Download document passport (.txt)',report,file_name='finsaarthi_credit_passport.txt',mime='text/plain',type='primary')
    note('No loan guarantee','Credit eligibility, lending risk and financial approvals require qualified institutions, verified information and applicable regulations.')

elif page=='assistant':
    page_title('05 / HUMAN-FRIENDLY SUPPORT','Ask FinSaarthi','A working context-aware guidance demo, with an optional consent-based language-model connection.')
    col1,col2=st.columns([1.5,1])
    with col1: lang=st.selectbox('Preferred language',['English','Tamil','Hindi'])
    with col2:
        try: has_key=bool(st.secrets.get('OPENAI_API_KEY',''))
        except Exception: has_key=bool(os.getenv('OPENAI_API_KEY',''))
        st.caption('Language-model connection: ' + ('configured (optional)' if has_key else 'not configured — local assistant ready'))
    prompts=['How much money do customers owe me?','What compliance items need review?','What invoices are overdue?','How can I prepare for a business loan?']
    st.markdown('**Suggested questions**')
    columns=st.columns(2)
    chosen=None
    for j,question in enumerate(prompts):
        with columns[j%2]:
            if st.button(question,key='suggest'+str(j),use_container_width=True): chosen=question
    if has_key:
        use_external=st.checkbox('Enable external AI (sends the question and summary figures to the configured API)',value=False)
    else: use_external=False
    for item in st.session_state.chatlog:
        with st.chat_message(item['role']): st.markdown(item['text'])
    question=st.chat_input('Ask about revenue, invoices, GST readiness, cash flow…')
    if chosen: question=chosen
    if question:
        st.session_state.chatlog.append({'role':'user','text':question})
        answer=assistant(question,df,lang)
        if use_external:
            try:
                import requests
                key=st.secrets.get('OPENAI_API_KEY') if has_key else os.getenv('OPENAI_API_KEY')
                summary={'invoice_count':len(df),'sales':m['revenue'],'receivable':m['receivable'],'payable':m['payable'],'review_flags':len(issues(df))}
                instructions=("You are FinSaarthi AI, a cautious financial workflow demo. Answer in "+lang+". Be concise and clear. "
                              "All values below are synthetic demo figures; do not imply statutory compliance or credit approval. "
                              "Never invent a tax deadline, GST rule, transaction or real capability. Summary: "+str(summary))
                result=requests.post('https://api.openai.com/v1/chat/completions',headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},json={'model':'gpt-4.1-mini','messages':[{'role':'system','content':instructions},{'role':'user','content':question}],'max_tokens':350},timeout=18)
                result.raise_for_status()
                answer=result.json()['choices'][0]['message']['content']
            except Exception as exc: answer+='\n\n*The optional external service was unavailable; local guidance used.*'
        st.session_state.chatlog.append({'role':'assistant','text':answer})
        st.rerun()
    st.markdown('<div class="footnote">Offline mode uses transparent, rule-based logic — not a trained language model. Optional AI use requires explicit opt-in and an API key. Do not upload sensitive production records for this hackathon demo.</div>',unsafe_allow_html=True)

else:
    page_title('THE TEAM & THE MISSION','Built for micro-enterprises','An ambitious, explainable and demonstrable product concept by one builder.')
    st.markdown('''<div class="hero"><div class="eyebrow">TEAM CODE TITAN · SOLO PARTICIPANT</div><div class="heading">FinSaarthi AI<br>Finance should feel simple.</div><div class="sub">Problem Statement 3.1 · MSME Finance and Compliance · Submitted by MURALIDHAR SM</div></div>''',unsafe_allow_html=True)
    features=[('01','Capture','Upload invoices or enter verified figures in a traceable ledger.'),('02','Review','Spot missing invoice fields and overdue payment reminders.'),('03','Understand','Explore sales, spending and cash-flow scenarios visually.'),('04','Prepare','Organise documentation for accountant and lender conversations.'),('05','Ask','Use a local guidance assistant, with optional connected AI.'),('06','Deploy','GitHub-ready Streamlit app with reproducible synthetic data.')]
    st.markdown('<div class="feature-grid">'+''.join(f'<div class="feature"><div class="n">{n} / CAPABILITY</div><h4>{esc(title)}</h4><p>{esc(desc)}</p></div>' for n,title,desc in features)+'</div>',unsafe_allow_html=True)
    st.subheader('System design')
    st.code('Uploaded CSV / searchable PDF / manual input\n                 ↓ human review\n       Python + Pandas finance engine\n                 ↓\n    Streamlit UI + Plotly analytics\n                 ↓\n  Exportable reports + optional AI API',language='text')
    note('Prototype scope','The app demonstrates reproducible financial calculations, document workflows and user interactions. It is not connected to a live GST portal, bank, automated production OCR, or a real lending system.')
    st.markdown('**Problem to impact:** Reduce repetitive work → make records understandable → give business owners time back.')

st.markdown('<div style="border-top:1px solid #e2e9ef;margin-top:35px;padding:15px 0;color:#8190a2;font-size:11px;text-align:center">FinSaarthi AI · CODE TITAN · MURALIDHAR SM · Solo Participant · Prototype / synthetic data / no live financial integrations</div>',unsafe_allow_html=True)
