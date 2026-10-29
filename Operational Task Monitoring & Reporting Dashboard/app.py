import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

from task_logger.models import Task
from task_logger.storage import TaskStorage

st.set_page_config(page_title="Compliance Task Dashboard", layout="wide", page_icon="📊")
st.title("📊 Compliance Task Dashboard")

storage = TaskStorage()

# ====================== RICH DEMO DATA ======================
if len(storage.get_all()) == 0:
    today = date.today()
    demo_tasks = [
        Task(1, str(today - timedelta(days=5)), "Clean Andron server logs", "completed", "Monthly compliance audit", str(today - timedelta(days=4))),
        Task(2, str(today - timedelta(days=3)), "Review firewall rules", "completed", "External access points", str(today - timedelta(days=2))),
        Task(3, str(today - timedelta(days=2)), "Update compliance documentation", "pending", "Policy version 2.3", None),
        Task(4, str(today - timedelta(days=1)), "Backup critical systems", "pending", "Weekly full backup", None),
        Task(5, str(today), "Audit user access logs", "pending", "Focus on privileged accounts", None),
        Task(6, str(today + timedelta(days=1)), "Patch vulnerability CVE-2026-XXXX", "pending", "High priority", None),
        Task(7, str(today - timedelta(days=4)), "Train staff on data protection", "completed", "GDPR refresher", str(today - timedelta(days=3))),
    ]
    
    for t in demo_tasks:
        storage.add_task(t)
    
    st.success("🎉 Rich demo data loaded! (7 realistic compliance tasks)")
    st.rerun()

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("➕ Add New Task")
    description = st.text_input("Task Description *", placeholder="e.g. Review firewall rules")
    task_date = st.date_input("Target Date", value=date.today())
    notes = st.text_area("Notes (optional)", height=120)
    
    if st.button("Add Task", type="primary", use_container_width=True):
        if description.strip():
            new_task = Task(
                id=storage.get_next_id(),
                date=str(task_date),
                description=description.strip(),
                status="pending",
                notes=notes.strip() if notes.strip() else None
            )
            storage.add_task(new_task)
            st.success(f"✅ Task #{new_task.id} added successfully!")
            st.rerun()
        else:
            st.error("Description is required")

# ====================== TABS ======================
tab1, tab2, tab3 = st.tabs(["📋 Tasks", "📈 Analytics", "📤 Export"])

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "pending", "completed"])
    
    tasks = storage.get_all() if status_filter == "All" else storage.get_all(status_filter)
    
    if tasks:
        df = pd.DataFrame([vars(t) for t in tasks])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.subheader("Quick Complete")
        task_id = st.number_input("Enter Task ID to complete", min_value=1, step=1)
        if st.button("✅ Mark as Completed", type="primary"):
            if storage.mark_complete(task_id):
                st.success(f"Task {task_id} marked as completed!")
                st.rerun()
            else:
                st.error("Task ID not found")
    else:
        st.info("No tasks found.")

with tab2:
    all_tasks = storage.get_all()
    if all_tasks:
        df_all = pd.DataFrame([vars(t) for t in all_tasks])
        
        col1, col2 = st.columns(2)
        with col1:
            status_counts = df_all['status'].value_counts()
            fig_pie = px.pie(
                values=status_counts.values, 
                names=status_counts.index,
                title="Task Status Overview",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            df_all['date'] = pd.to_datetime(df_all['date'])
            date_counts = df_all.groupby('date').size().reset_index(name='count')
            fig_bar = px.bar(
                date_counts, 
                x='date', 
                y='count',
                title="Tasks by Date"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Add more tasks to see analytics.")

with tab3:
    all_tasks = storage.get_all()
    if all_tasks:
        df_all = pd.DataFrame([vars(t) for t in all_tasks])
        csv = df_all.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Compliance Report",
            data=csv,
            file_name=f"compliance_tasks_{date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.info("No data to export.")

st.caption("Compliance Task Dashboard • Reused CLI Backend • Built with Streamlit")
