import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIG ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bank Fraud Detection EDA",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #e74c3c 0%, #8e44ad 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .section-header {
        color: #e74c3c;
        font-weight: 700;
        font-size: 1.4rem;
        border-left: 4px solid #e74c3c;
        padding-left: 10px;
        margin: 1rem 0;
    }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #e74c3c44;
        border-radius: 10px;
        padding: 12px;
    }
    div[data-testid="metric-container"] label {
        color: #a0aec0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('bank_fraud.csv')
    df['fraud_type'] = df['fraud_type'].fillna('Not Fraud')
    df['freq_bucket'] = pd.cut(df['transaction_freq_monthly'],
        bins=[0, 10, 20, 30, 50, 100],
        labels=['1-10', '11-20', '21-30', '31-50', '51+'])
    df['time_bucket'] = pd.cut(df['time_since_last_txn_hrs'],
        bins=[0, 1, 6, 24, 72, df['time_since_last_txn_hrs'].max()+1],
        labels=['<1hr', '1-6hrs', '6-24hrs', '1-3days', '>3days'])
    return df

df = load_data()
overall_fraud_rate = df['is_fraud'].mean() * 100

# ── SIDEBAR ──────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank.png", width=80)
    st.title("🔍 Filters")
    st.markdown("---")

    countries = ["All"] + sorted(df['country'].unique().tolist())
    sel_country = st.selectbox("Country", countries)

    payment_methods = ["All"] + sorted(df['payment_method'].unique().tolist())
    sel_payment = st.selectbox("Payment Method", payment_methods)

    device_types = ["All"] + sorted(df['device_type'].unique().tolist())
    sel_device = st.selectbox("Device Type", device_types)

    merchant_cats = ["All"] + sorted(df['merchant_category'].unique().tolist())
    sel_merchant = st.selectbox("Merchant Category", merchant_cats)

    fraud_filter = st.radio("Transaction Type", ["All", "Fraud Only", "Legitimate Only"])

    amt_min, amt_max = float(df['transaction_amount'].min()), float(df['transaction_amount'].max())
    sel_amt = st.slider("Transaction Amount Range",
                        amt_min, amt_max, (amt_min, amt_max), step=10.0)

    st.markdown("---")
    st.markdown("**Built with ❤️ using Streamlit**")
    st.markdown("[GitHub](https://github.com) | [LinkedIn](https://linkedin.com)")

# ── APPLY FILTERS ────────────────────────────────────────────────────
fdf = df.copy()
if sel_country != "All":
    fdf = fdf[fdf['country'] == sel_country]
if sel_payment != "All":
    fdf = fdf[fdf['payment_method'] == sel_payment]
if sel_device != "All":
    fdf = fdf[fdf['device_type'] == sel_device]
if sel_merchant != "All":
    fdf = fdf[fdf['merchant_category'] == sel_merchant]
if fraud_filter == "Fraud Only":
    fdf = fdf[fdf['is_fraud'] == 1]
elif fraud_filter == "Legitimate Only":
    fdf = fdf[fdf['is_fraud'] == 0]
fdf = fdf[(fdf['transaction_amount'] >= sel_amt[0]) & (fdf['transaction_amount'] <= sel_amt[1])]

# ── HEADER ───────────────────────────────────────────────────────────
st.markdown('<p class="main-header">🏦 Bank Fraud Detection — EDA Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    f"<p style='text-align:center; color:#718096; font-size:1.1rem;'>"
    f"Analysing <b>{fdf.shape[0]:,}</b> of <b>{df.shape[0]:,}</b> transactions</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ── KPI METRICS ──────────────────────────────────────────────────────
fraud_count = fdf['is_fraud'].sum()
fraud_rate  = fdf['is_fraud'].mean() * 100 if len(fdf) > 0 else 0
avg_amt     = fdf['transaction_amount'].mean()
fraud_amt   = fdf[fdf['is_fraud']==1]['transaction_amount'].mean() if fraud_count > 0 else 0
intl_fraud  = fdf[fdf['is_international']==1]['is_fraud'].mean()*100 if len(fdf[fdf['is_international']==1]) > 0 else 0
night_fraud = fdf[fdf['is_night_transaction']==1]['is_fraud'].mean()*100 if len(fdf[fdf['is_night_transaction']==1]) > 0 else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("📊 Transactions", f"{fdf.shape[0]:,}")
c2.metric("🚨 Fraud Count", f"{fraud_count:,}")
c3.metric("⚠️ Fraud Rate", f"{fraud_rate:.2f}%")
c4.metric("💰 Avg Amount", f"${avg_amt:,.2f}")
c5.metric("🌍 Intl Fraud Rate", f"{intl_fraud:.2f}%")
c6.metric("🌙 Night Fraud Rate", f"{night_fraud:.2f}%")

st.markdown("---")

# ── TABS ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🚨 Fraud Overview",
    "💰 Transaction Amount",
    "⏰ Time Patterns",
    "💳 Payment & Device",
    "🏪 Merchant Category",
    "👤 Customer Profile",
    "🔥 Correlations"
])

# ── TAB 1: FRAUD OVERVIEW ────────────────────────────────────────────
with tab1:
    st.markdown('<p class="section-header">Fraud Overview</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        legit = len(fdf) - fraud_count
        fig = px.pie(values=[legit, fraud_count],
                     names=['Legitimate', 'Fraudulent'],
                     color_discrete_map={'Legitimate':'#2ecc71','Fraudulent':'#e74c3c'},
                     title='Fraud vs Legitimate Transactions', hole=0.45)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fraud_types = fdf[fdf['is_fraud']==1]['fraud_type'].value_counts().reset_index()
        fraud_types.columns = ['Fraud Type', 'Count']
        fraud_types = fraud_types[fraud_types['Fraud Type'] != 'Not Fraud']
        fig2 = px.bar(fraud_types, x='Count', y='Fraud Type', orientation='h',
                      color='Count', color_continuous_scale='reds',
                      title='Fraud Type Distribution')
        fig2.update_layout(coloraxis_showscale=False, height=400,
                           yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)

    # Fraud rate by country
    country_fraud = fdf.groupby('country')['is_fraud'].mean().reset_index()
    country_fraud.columns = ['Country', 'Fraud Rate']
    country_fraud['Fraud Rate'] = country_fraud['Fraud Rate'] * 100
    country_fraud = country_fraud.sort_values('Fraud Rate', ascending=False)
    fig3 = px.bar(country_fraud, x='Country', y='Fraud Rate',
                  color='Fraud Rate', color_continuous_scale='reds',
                  title='Fraud Rate by Country (%)',
                  text='Fraud Rate')
    fig3.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig3.update_layout(coloraxis_showscale=False, height=400)
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 2: TRANSACTION AMOUNT ────────────────────────────────────────
with tab2:
    st.markdown('<p class="section-header">Transaction Amount Analysis</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=fdf[fdf['is_fraud']==0]['transaction_amount'],
                                   name='Legitimate', opacity=0.6,
                                   marker_color='#2ecc71', nbinsx=50))
        fig.add_trace(go.Histogram(x=fdf[fdf['is_fraud']==1]['transaction_amount'],
                                   name='Fraudulent', opacity=0.6,
                                   marker_color='#e74c3c', nbinsx=50))
        fig.update_layout(barmode='overlay', title='Amount Distribution: Fraud vs Legit',
                          xaxis_title='Transaction Amount', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.box(fdf, x='is_fraud', y='transaction_amount',
                      color='is_fraud',
                      color_discrete_map={0:'#2ecc71', 1:'#e74c3c'},
                      title='Amount Boxplot: Legit (0) vs Fraud (1)',
                      labels={'transaction_amount':'Amount','is_fraud':'Is Fraud'})
        fig2.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig2, use_container_width=True)

    # Avg amount by merchant
    mc_amt = fdf.groupby(['merchant_category','is_fraud'])['transaction_amount'].mean().reset_index()
    mc_amt['Type'] = mc_amt['is_fraud'].map({0:'Legitimate', 1:'Fraudulent'})
    fig3 = px.bar(mc_amt, x='merchant_category', y='transaction_amount',
                  color='Type',
                  color_discrete_map={'Legitimate':'#2ecc71','Fraudulent':'#e74c3c'},
                  barmode='group',
                  title='Avg Transaction Amount by Merchant Category',
                  labels={'transaction_amount':'Avg Amount','merchant_category':'Merchant'})
    fig3.update_xaxes(tickangle=45)
    fig3.update_layout(height=420)
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 3: TIME PATTERNS ─────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-header">Time-Based Fraud Patterns</p>', unsafe_allow_html=True)

    # Fraud rate by hour
    hour_fraud = fdf.groupby('hour_of_day')['is_fraud'].mean().reset_index()
    hour_fraud.columns = ['Hour', 'Fraud Rate']
    hour_fraud['Fraud Rate'] = hour_fraud['Fraud Rate'] * 100
    fig = px.line(hour_fraud, x='Hour', y='Fraud Rate', markers=True,
                  color_discrete_sequence=['#e74c3c'],
                  title='Fraud Rate by Hour of Day (%)',
                  labels={'Fraud Rate':'Fraud Rate (%)','Hour':'Hour of Day'})
    fig.add_hline(y=overall_fraud_rate, line_dash='dash',
                  line_color='gray', annotation_text=f'Overall: {overall_fraud_rate:.2f}%')
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        wk = fdf.groupby('is_weekend')['is_fraud'].mean().reset_index()
        wk['Label'] = wk['is_weekend'].map({0:'Weekday', 1:'Weekend'})
        wk['Fraud Rate'] = wk['is_fraud'] * 100
        fig2 = px.bar(wk, x='Label', y='Fraud Rate',
                      color='Label',
                      color_discrete_map={'Weekday':'#3498db','Weekend':'#e74c3c'},
                      title='Fraud Rate: Weekday vs Weekend (%)',
                      text='Fraud Rate')
        fig2.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig2.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        nt = fdf.groupby('is_night_transaction')['is_fraud'].mean().reset_index()
        nt['Label'] = nt['is_night_transaction'].map({0:'Day', 1:'Night'})
        nt['Fraud Rate'] = nt['is_fraud'] * 100
        fig3 = px.bar(nt, x='Label', y='Fraud Rate',
                      color='Label',
                      color_discrete_map={'Day':'#f39c12','Night':'#8e44ad'},
                      title='Fraud Rate: Day vs Night (%)',
                      text='Fraud Rate')
        fig3.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig3.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig3, use_container_width=True)

# ── TAB 4: PAYMENT & DEVICE ──────────────────────────────────────────
with tab4:
    st.markdown('<p class="section-header">Payment Method & Device Type</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        pm = fdf.groupby('payment_method')['is_fraud'].mean().reset_index()
        pm.columns = ['Payment Method', 'Fraud Rate']
        pm['Fraud Rate'] = pm['Fraud Rate'] * 100
        pm = pm.sort_values('Fraud Rate', ascending=False)
        fig = px.bar(pm, x='Payment Method', y='Fraud Rate',
                     color='Fraud Rate', color_continuous_scale='reds',
                     title='Fraud Rate by Payment Method (%)',
                     text='Fraud Rate')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.add_hline(y=overall_fraud_rate, line_dash='dash', line_color='gray')
        fig.update_layout(coloraxis_showscale=False, height=420, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        dt = fdf.groupby('device_type')['is_fraud'].mean().reset_index()
        dt.columns = ['Device Type', 'Fraud Rate']
        dt['Fraud Rate'] = dt['Fraud Rate'] * 100
        dt = dt.sort_values('Fraud Rate', ascending=False)
        fig2 = px.bar(dt, x='Device Type', y='Fraud Rate',
                      color='Fraud Rate', color_continuous_scale='purples',
                      title='Fraud Rate by Device Type (%)',
                      text='Fraud Rate')
        fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig2.add_hline(y=overall_fraud_rate, line_dash='dash', line_color='gray')
        fig2.update_layout(coloraxis_showscale=False, height=420, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Payment method volume
    pm_vol = fdf.groupby(['payment_method','is_fraud']).size().reset_index(name='Count')
    pm_vol['Type'] = pm_vol['is_fraud'].map({0:'Legitimate', 1:'Fraudulent'})
    fig3 = px.bar(pm_vol, x='payment_method', y='Count', color='Type',
                  color_discrete_map={'Legitimate':'#2ecc71','Fraudulent':'#e74c3c'},
                  barmode='stack',
                  title='Transaction Volume by Payment Method',
                  labels={'payment_method':'Payment Method'})
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 5: MERCHANT CATEGORY ─────────────────────────────────────────
with tab5:
    st.markdown('<p class="section-header">Merchant Category Analysis</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mc = fdf.groupby('merchant_category')['is_fraud'].mean().reset_index()
        mc.columns = ['Merchant', 'Fraud Rate']
        mc['Fraud Rate'] = mc['Fraud Rate'] * 100
        mc = mc.sort_values('Fraud Rate', ascending=False)
        fig = px.bar(mc, x='Fraud Rate', y='Merchant', orientation='h',
                     color='Fraud Rate', color_continuous_scale='reds',
                     title='Fraud Rate by Merchant Category (%)')
        fig.add_vline(x=overall_fraud_rate, line_dash='dash', line_color='gray')
        fig.update_layout(coloraxis_showscale=False, height=500,
                          yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        mc_vol = fdf[fdf['is_fraud']==1]['merchant_category'].value_counts().reset_index()
        mc_vol.columns = ['Merchant', 'Fraud Count']
        fig2 = px.bar(mc_vol, x='Fraud Count', y='Merchant', orientation='h',
                      color='Fraud Count', color_continuous_scale='oranges',
                      title='Fraud Volume by Merchant Category')
        fig2.update_layout(coloraxis_showscale=False, height=500,
                           yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)

# ── TAB 6: CUSTOMER PROFILE ──────────────────────────────────────────
with tab6:
    st.markdown('<p class="section-header">Customer Profile Analysis</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=fdf[fdf['is_fraud']==0]['customer_age'],
                                   name='Legitimate', opacity=0.6,
                                   marker_color='#2ecc71', nbinsx=40))
        fig.add_trace(go.Histogram(x=fdf[fdf['is_fraud']==1]['customer_age'],
                                   name='Fraudulent', opacity=0.6,
                                   marker_color='#e74c3c', nbinsx=40))
        fig.update_layout(barmode='overlay', title='Customer Age Distribution',
                          xaxis_title='Age', height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(x=fdf[fdf['is_fraud']==0]['credit_score'],
                                    name='Legitimate', opacity=0.6,
                                    marker_color='#2ecc71', nbinsx=40))
        fig2.add_trace(go.Histogram(x=fdf[fdf['is_fraud']==1]['credit_score'],
                                    name='Fraudulent', opacity=0.6,
                                    marker_color='#e74c3c', nbinsx=40))
        fig2.update_layout(barmode='overlay', title='Credit Score Distribution',
                           xaxis_title='Credit Score', height=380)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        failed = fdf.groupby('failed_attempts')['is_fraud'].mean().reset_index()
        failed.columns = ['Failed Attempts', 'Fraud Rate']
        failed['Fraud Rate'] = failed['Fraud Rate'] * 100
        fig3 = px.bar(failed, x='Failed Attempts', y='Fraud Rate',
                      color='Fraud Rate', color_continuous_scale='reds',
                      title='Fraud Rate by Failed Attempts (%)',
                      text='Fraud Rate')
        fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig3.update_layout(coloraxis_showscale=False, height=380)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        intl = fdf.groupby('is_international')['is_fraud'].mean().reset_index()
        intl['Label'] = intl['is_international'].map({0:'Domestic', 1:'International'})
        intl['Fraud Rate'] = intl['is_fraud'] * 100
        fig4 = px.bar(intl, x='Label', y='Fraud Rate',
                      color='Label',
                      color_discrete_map={'Domestic':'#3498db','International':'#e74c3c'},
                      title='Fraud Rate: Domestic vs International (%)',
                      text='Fraud Rate')
        fig4.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig4.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig4, use_container_width=True)

# ── TAB 7: CORRELATIONS ──────────────────────────────────────────────
with tab7:
    st.markdown('<p class="section-header">Correlation Analysis</p>', unsafe_allow_html=True)

    num_cols = ['transaction_amount', 'customer_age', 'credit_score',
                'account_age_years', 'account_balance', 'distance_from_home_km',
                'time_since_last_txn_hrs', 'failed_attempts', 'is_fraud']

    # Sample for performance
    sample = fdf[num_cols].sample(min(50000, len(fdf)), random_state=42)
    corr = sample.corr()

    fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1,
                    title='Correlation Heatmap — Numerical Features')
    fig.update_layout(height=550)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("X Axis", num_cols, index=6)
    with col2:
        y_col = st.selectbox("Y Axis", num_cols, index=0)

    scatter_sample = fdf.sample(min(5000, len(fdf)), random_state=42)
    scatter_sample['Fraud'] = scatter_sample['is_fraud'].map({0:'Legitimate', 1:'Fraudulent'})
    fig2 = px.scatter(scatter_sample, x=x_col, y=y_col, color='Fraud',
                      color_discrete_map={'Legitimate':'#2ecc71','Fraudulent':'#e74c3c'},
                      opacity=0.5,
                      title=f'{x_col} vs {y_col} (5K sample)')
    fig2.update_layout(height=450)
    st.plotly_chart(fig2, use_container_width=True)

# ── RAW DATA ─────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Sample Data (500 rows)"):
    show_cols = ['transaction_id','customer_id','transaction_date','country',
                 'merchant_category','payment_method','device_type',
                 'transaction_amount','is_fraud','fraud_type']
    st.dataframe(fdf[show_cols].head(500), use_container_width=True)
    csv = fdf[show_cols].head(5000).to_csv(index=False)
    st.download_button("⬇️ Download Sample CSV (5K rows)", data=csv,
                       file_name="bank_fraud_sample.csv", mime="text/csv")
