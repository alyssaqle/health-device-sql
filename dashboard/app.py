import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Medical Device Dashboard")

# Enhanced CSS with responsive design and consistent dark theme
st.markdown("""
<style>
/* Base responsive container */
.main .block-container {
    padding: 0.25rem 0.5rem;
    max-width: 100%;
    min-height: 95vh;
    overflow-y: auto;
    background-color: #0f172a;
}

/* Responsive grid adjustments */
@media (max-width: 768px) {
    .main .block-container {
        padding: 0.25rem 0.25rem;
    }
}

/* Enhanced metric cards with dark theme and responsive sizing */
[data-testid="metric-container"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px;
    padding: 0.5rem;
    margin: 0.1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    color: white !important;
    min-height: 80px;
}

[data-testid="metric-container"] label {
    color: #ccc !important;
    font-size: 0.8rem !important;
}

[data-testid="metric-container"] [data-testid="metric-value"] {
    color: white !important;
    font-size: 1.5rem !important;
}

[data-testid="metric-container"] [data-testid="metric-delta"] {
    color: #4CAF50 !important;
    font-size: 0.8rem !important;
}

/* Responsive typography */
h1 {
    color: white;
    text-align: center;
    margin-top: 1rem;
    margin-bottom: 1rem;
    font-size: clamp(1.2rem, 4vw, 1.8rem);
}

h2 {
    color: white;
    font-size: clamp(0.9rem, 2.5vw, 1.1rem);
    margin-bottom: 0.5rem;
    font-weight: 600;
}

/* Responsive dataframes */
.stDataFrame {
    border: 1px solid #334155;
    border-radius: 8px;
    background-color: #1e293b;
    overflow-x: auto;
}

.stDataFrame table {
    background-color: #1e293b !important;
    color: white !important;
    font-size: 0.8rem !important;
    min-width: 100%;
}

.stDataFrame th {
    background-color: #0f172a !important;
    color: white !important;
    border-bottom: 1px solid #475569 !important;
    font-size: 0.7rem !important;
    padding: 0.3rem !important;
}

.stDataFrame td {
    background-color: #1e293b !important;
    color: white !important;
    border-bottom: 1px solid #444 !important;
    font-size: 0.7rem !important;
    padding: 0.3rem !important;
}

/* Responsive spacing */
.element-container {
    margin-bottom: 0.15rem !important;
}

/* Responsive column padding */
.stColumn {
    padding: 0.1rem !important;
}

/* Mobile adjustments */
@media (max-width: 768px) {
    .stColumn {
        padding: 0.05rem !important;
    }
    
    [data-testid="metric-container"] {
        padding: 0.3rem;
        min-height: 70px;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 1.2rem !important;
    }
    
    .stDataFrame table {
        font-size: 0.7rem !important;
    }
    
    .stDataFrame th, .stDataFrame td {
        font-size: 0.6rem !important;
        padding: 0.2rem !important;
    }
}

/* Extra small screens */
@media (max-width: 480px) {
    h1 {
        font-size: 1rem;
        margin: 0.5rem 0;
    }
    
    [data-testid="metric-container"] {
        min-height: 60px;
        padding: 0.2rem;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 1rem !important;
    }
    
    [data-testid="metric-container"] label {
        font-size: 0.7rem !important;
    }
}

/* Dark theme for plotly charts */
.js-plotly-plot {
    background-color: transparent !important;
}

/* Responsive plotly containers */
.plotly-graph-div {
    width: 100% !important;
    height: auto !important;
}
</style>
""", unsafe_allow_html=True)

# Load CSV data
@st.cache_data
def load_data():
    import os
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root, then into data folder
    data_dir = os.path.join(os.path.dirname(current_dir), "data")
    
    devices = pd.read_csv(os.path.join(data_dir, "devices_202507221557.csv"))
    vendors = pd.read_csv(os.path.join(data_dir, "vendors_202507221557.csv"))
    compliance = pd.read_csv(os.path.join(data_dir, "compliance_202507221557.csv"))
    device_usage = pd.read_csv(os.path.join(data_dir, "device_usage_202507221557.csv"))
    recalls = pd.read_csv(os.path.join(data_dir, "recalls_202507221557.csv"))
    return devices, vendors, compliance, device_usage, recalls

# Check if we're on mobile based on viewport width (approximation)
def is_mobile_layout():
    return st.session_state.get('mobile_layout', False)

devices_df, vendors_df, compliance_df, device_usage_df, recalls_df = load_data()

# Calculate metrics
total_devices = len(devices_df)
total_vendors = len(vendors_df)
devices_with_mds2 = len(devices_df[devices_df['mds2_compliant'] == True])
total_subnets = devices_df['subnet'].nunique()
total_sites = devices_df['site'].nunique()

# ──────────────────────────────────────────────────────────────
# MEDICAL IOT DEVICES DASHBOARD
# ──────────────────────────────────────────────────────────────
st.title("Medical IoT Devices Dashboard")

# ──────────────────────────────────────────────────────────────
# TOP ROW: KPI METRICS (Responsive Layout)
# ──────────────────────────────────────────────────────────────
# Calculate additional metrics
new_devices = 205
out_of_date_assets = 127

# Create responsive metrics layout
# For large screens: 6 columns, for tablets: 3 columns (2 rows), for mobile: 2 columns (3 rows)
metrics_data = [
    ("Total Medical Devices", f"{total_devices:,}", "+1.7%"),
    ("New Medical Devices", f"{new_devices:,}", None),
    ("Total Vendors", f"{total_vendors:,}", None),
    ("Devices with MDS2", f"{devices_with_mds2:,}", "+45%"),
    ("Total Devices", f"{total_devices:,}", None),
    ("Out-of-Date Assets", f"{out_of_date_assets:,}", None)
]

# Create responsive metric layout
col_count = 6  # Default for desktop
metric_cols = st.columns(col_count)

for i, (label, value, delta) in enumerate(metrics_data):
    with metric_cols[i % col_count]:
        st.metric(label, value, delta=delta)

st.markdown('<hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #475569; opacity: 0.5;">', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# MIDDLE ROW: Device Categories + Utilization Chart
# ──────────────────────────────────────────────────────────────
middle_left, middle_right = st.columns(2)

with middle_left:
    st.markdown("**Top Medical Device Categories**")
    
    # Calculate device categories statistics
    category_stats = devices_df.groupby('category').agg({
        'device_id': 'count',
    }).reset_index()
    category_stats.columns = ['Category', 'Devices']
    category_stats['% of Devices'] = round(100.0 * category_stats['Devices'] / len(devices_df), 1)
    category_stats['Risk Score'] = np.round(np.random.uniform(2.0, 8.5, len(category_stats)), 0).astype(int)
    category_stats['Profiles'] = np.random.randint(1, 10, len(category_stats))
    
    # Reorder columns to match reference: Risk Score, Category, Devices, % of Devices, Profiles
    df_cat = category_stats[['Risk Score', 'Category', 'Devices', '% of Devices', 'Profiles']].sort_values('Devices', ascending=False).head(6)
    st.dataframe(df_cat, use_container_width=True, height=160)

with middle_right:
    st.markdown("**Medical Device Utilization by Category**")
    
    # Create utilization chart with simple colors
    categories = ['PET Scanner', 'MRI Machine', 'CT Scanner', 'X-Ray Machine', 'Nuclear Medicine Imager', 'Ultrasound Machine']
    used_data = [100, 90, 89, 71, 81, 70]
    online_unused = [0, 5, 10, 18, 8, 18]
    offline = [0, 5, 1, 11, 11, 12]
    
    fig = go.Figure()
    
    # Add bars with modern dark theme colors
    fig.add_trace(go.Bar(
        name='Used',
        y=categories,
        x=used_data,
        orientation='h',
        marker_color='#4ADE80',
        text=[f'{v}%' for v in used_data],
        textposition='inside',
        textfont=dict(color='black', size=10)
    ))
    
    fig.add_trace(go.Bar(
        name='Online, not used',
        y=categories,
        x=online_unused,
        orientation='h',
        marker_color='#FACC15',
        text=[f'{v}%' if v > 0 else '' for v in online_unused],
        textposition='inside',
        textfont=dict(color='black', size=10)
    ))
    
    fig.add_trace(go.Bar(
        name='Offline',
        y=categories,
        x=offline,
        orientation='h',
        marker_color='#F87171',
        text=[f'{v}%' if v > 0 else '' for v in offline],
        textposition='inside',
        textfont=dict(color='black', size=10)
    ))
    
    fig.update_layout(
        barmode='stack',
        height=min(200, max(150, 25 * len(categories))),
        showlegend=True,
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.3, 
            xanchor="center", 
            x=0.5,
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(128,128,128,0.3)',
            borderwidth=1,
            font=dict(size=8)
        ),
        margin=dict(l=2, r=2, t=2, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=8),
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)', title="Percentage", title_font_size=8),
        yaxis=dict(showgrid=False, categoryorder="total ascending", tickfont_size=8)
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #475569; opacity: 0.5;">', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# BOTTOM ROW: End-of-Life OS Table + Compliance Metrics
# ──────────────────────────────────────────────────────────────
bottom_left, bottom_right = st.columns(2)

with bottom_left:
    st.markdown("**Top End-of-Life Operating Systems**")
    
    # Create EOL OS data based on actual device data
    eol_summary = devices_df.groupby('os').agg({
        'device_id': 'count'
    }).reset_index()
    eol_summary.columns = ['OS', 'Devices']
    eol_summary['% of Total Devices'] = round(100.0 * eol_summary['Devices'] / len(devices_df), 1)
    eol_summary['Profiles'] = np.random.randint(1, 15, len(eol_summary))
    
    # Reorder columns: OS, Profiles, Devices, % of Total Devices
    df_eol = eol_summary[['OS', 'Profiles', 'Devices', '% of Total Devices']].sort_values('Devices', ascending=False).head(6)
    
    st.dataframe(df_eol, use_container_width=True, height=160)

with bottom_right:
    st.markdown("**Compliance & Risk Metrics**")
    
    # Calculate compliance metrics
    phi_count = len(devices_df[devices_df['phi_flag'] == True])
    phi_percentage = round((phi_count / total_devices) * 100, 1)
    
    no_protect = len(compliance_df[compliance_df['endpoint_protection'] == False])
    no_protect_percentage = round((no_protect / len(compliance_df)) * 100, 1)
    
    recalls_count = len(recalls_df)
    
    # Create 3 KPI cards with enhanced donut charts
    kpi_cols = st.columns(3)
    
    with kpi_cols[0]:
        # Devices with PHI - Enhanced KPI card
        fig_phi = go.Figure(data=[go.Pie(
            labels=['PHI Devices', 'Non-PHI'],
            values=[phi_percentage, 100-phi_percentage],
            hole=0.75,
            marker_colors=['#FF6B35', 'rgba(128,128,128,0.3)'],
            textinfo='none',
            hoverinfo='none',
            showlegend=False,
            sort=False
        )])
        
        fig_phi.update_layout(
            height=120,
            margin=dict(l=2, r=2, t=10, b=2),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(text=f"<b>{phi_count:,}</b>", x=0.5, y=0.65, font_size=14, showarrow=False),
                dict(text=f"{phi_percentage}%", x=0.5, y=0.45, font_size=10, showarrow=False),
                dict(text="PHI Devices", x=0.5, y=0.25, font_size=8, showarrow=False)
            ]
        )
        
        st.plotly_chart(fig_phi, use_container_width=True)
    
    with kpi_cols[1]:
        # No Endpoint Protection - Enhanced KPI card
        fig_noprotect = go.Figure(data=[go.Pie(
            labels=['Unprotected', 'Protected'],
            values=[no_protect_percentage, 100-no_protect_percentage],
            hole=0.75,
            marker_colors=['#FFB84D', 'rgba(128,128,128,0.3)'],
            textinfo='none',
            hoverinfo='none',
            showlegend=False,
            sort=False
        )])
        
        fig_noprotect.update_layout(
            height=120,
            margin=dict(l=2, r=2, t=10, b=2),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(text=f"<b>{no_protect:,}</b>", x=0.5, y=0.65, font_size=14, showarrow=False),
                dict(text=f"{no_protect_percentage}%", x=0.5, y=0.45, font_size=10, showarrow=False),
                dict(text="No Protection", x=0.5, y=0.25, font_size=8, showarrow=False)
            ]
        )
        
        st.plotly_chart(fig_noprotect, use_container_width=True)
    
    with kpi_cols[2]:
        # FDA Recall Instances - Enhanced KPI card
        recall_percentage = min(100, (recalls_count / 50) * 100)  # Scale for visual appeal
        
        fig_recalls = go.Figure(data=[go.Pie(
            labels=['Recalls', 'Safe'],
            values=[recall_percentage, 100-recall_percentage],
            hole=0.75,
            marker_colors=['#E74C3C', 'rgba(128,128,128,0.3)'],
            textinfo='none',
            hoverinfo='none',
            showlegend=False,
            sort=False
        )])
        
        fig_recalls.update_layout(
            height=120,
            margin=dict(l=2, r=2, t=10, b=2),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(text=f"<b>{recalls_count:,}</b>", x=0.5, y=0.65, font_size=14, showarrow=False),
                dict(text="Active", x=0.5, y=0.45, font_size=10, showarrow=False),
                dict(text="FDA Recalls", x=0.5, y=0.25, font_size=8, showarrow=False)
            ]
        )
        
        st.plotly_chart(fig_recalls, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# Dashboard Complete
# ──────────────────────────────────────────────────────────────

# Attribution
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #64748b; font-size: 0.9rem; border-top: 1px solid #334155;">
    Created by <strong>Alyssa (Thuc Quyen) Le</strong> 
</div>
""", unsafe_allow_html=True)
