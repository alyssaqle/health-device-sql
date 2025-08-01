# Medical IoT Devices Dashboard

A comprehensive dashboard for monitoring medical IoT devices with compliance tracking, utilization metrics, and risk assessment.

## Features

- **Modern Dark Theme**: Professional slate color palette
- **Real-time Metrics**: KPI cards with device counts and compliance stats
- **Device Categories**: Risk scoring and utilization tracking
- **Compliance Monitoring**: PHI devices, endpoint protection, FDA recalls
- **Interactive Charts**: Plotly visualizations with donut charts and bar charts

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/alyssaqle/health-device-sql.git
cd health-device-sql
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
cd dashboard
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy using:
   - **Repository**: `your-username/health-device-sql`
   - **Branch**: `main`
   - **Main file path**: `dashboard/app.py`

## File Structure

```
health-device-sql/
├── dashboard/
│   └── app.py              # Main Streamlit application
├── data/                   # CSV data files
│   ├── devices_*.csv
│   ├── vendors_*.csv
│   ├── compliance_*.csv
│   └── ...
├── requirements.txt        # Python dependencies
└── README.md
```

## Data Sources

The dashboard uses CSV files containing:
- Medical device inventory and specifications
- Vendor information and compliance status
- Device usage patterns and utilization metrics
- FDA recall data and risk assessments

## Technologies

- **Frontend**: Streamlit with custom CSS styling
- **Data Processing**: Pandas and NumPy
- **Visualizations**: Plotly for interactive charts
- **Styling**: Modern dark theme with professional color palette
