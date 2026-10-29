# Operational Task Monitoring & Reporting Dashboard

## Features
- ✅ Add tasks via clean sidebar form
- ✅ Filterable data table
- ✅ Real-time analytics (pie chart + bar chart)
- ✅ CSV export for compliance records
- ✅ Dark modern UI with Streamlit

## Screenshots

**1. Main Dashboard**
![Main Dashboard](https://github.com/kofimanu2403/compliance-task-dashboard/blob/main/screenshot-1-overview.png)

**2. Adding New Tasks**
![Add Task](https://github.com/kofimanu2403/compliance-task-dashboard/blob/main/screenshot-2-add-task.png)

**3. Analytics View**
![Analytics](https://github.com/kofimanu2403/compliance-task-dashboard/blob/main/screenshot-3-analytics.png)

## Quick Start

```bash
cd compliance-task-dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Tech Stack
- **Streamlit** — Interactive web UI
- **Pandas + Plotly** — Data processing & charts
- Reused `Task` model & storage from the CLI project