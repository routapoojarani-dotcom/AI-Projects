import streamlit as st
import pandas as pd
import plotly.express as px
import database as db

st.set_page_config(page_title="Agile Task & Resource Tracker", layout="wide")

db.init_db()

st.title("Agile Task & Resource Tracker")
st.markdown("---")

st.sidebar.header("➕ Create New Task")
with st.sidebar.form("task_form", clear_on_submit=True):
    title = st.text_input("Task Title")
    assignee = st.text_input("Assignee Name")
    status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    est_hours = st.number_input("Estimated Hours", min_value=0.5, value=4.0, step=0.5)
    submit = st.form_submit_button("Add Task")

if submit:
    if title.strip() and assignee.strip():
        db.add_task(title.strip(), assignee.strip(), status, priority, est_hours)
        st.sidebar.success(f"Task '{title}' added!")
        st.rerun()
    else:
        st.sidebar.error("Title and Assignee are required.")

raw_tasks = db.get_all_tasks()
columns = ["ID", "Title", "Assignee", "Status", "Priority", "Estimated Hours", "Logged Hours", "Created At", "Updated At"]
df = pd.DataFrame(raw_tasks, columns=columns) if raw_tasks else pd.DataFrame(columns=columns)

tab1, tab2, tab3 = st.tabs(["📋 Kanban Board View", "📊 Agile Analytics", "⚙️ Manage & Delete Tasks"])

with tab1:
    st.subheader("Interactive Kanban Board")
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📝 To Do")
            todo_df = df[df["Status"] == "To Do"]
            for idx, row in todo_df.iterrows():
                with st.expander(f"**{row['Title']}** ({row['Priority']})"):
                    st.write(f"👤 **Assignee:** {row['Assignee']}")
                    st.write(f"⏱️ **Est. Hours:** {row['Estimated Hours']}")
                    
        with col2:
            st.markdown("### ⚙️ In Progress")
            prog_df = df[df["Status"] == "In Progress"]
            for idx, row in prog_df.iterrows():
                with st.expander(f"**{row['Title']}** ({row['Priority']})"):
                    st.write(f"👤 **Assignee:** {row['Assignee']}")
                    st.write(f"⏱️ **Progress:** {row['Logged Hours']} / {row['Estimated Hours']} hrs")

        with col3:
            st.markdown("### ✅ Done")
            done_df = df[df["Status"] == "Done"]
            for idx, row in done_df.iterrows():
                with st.expander(f"**{row['Title']}**"):
                    st.write(f"👤 **Assignee:** {row['Assignee']}")
                    st.write(f"⏱️ **Total Logged:** {row['Logged Hours']} hrs")
    else:
        st.info("No tasks available. Add tasks using the sidebar to get started.")

with tab2:
    st.subheader("Velocity & Bottleneck Metrics")
    if not df.empty:
        m1, m2, m3, m4 = st.columns(4)
        total_tasks = len(df)
        completed_tasks = len(df[df["Status"] == "Done"])
        total_est = df["Estimated Hours"].sum()
        total_logged = df["Logged Hours"].sum()

        m1.metric("Total Tasks", total_tasks)
        m2.metric("Completed Tasks", completed_tasks)
        m3.metric("Est. Hours", f"{total_est:.1f}h")
        m4.metric("Logged Hours", f"{total_logged:.1f}h")

        st.markdown("---")
        col_a, col_b = st.columns(2)
        
        with col_a:
            fig_status = px.pie(df, names="Status", title="Task Distribution by Status", hole=0.4)
            st.plotly_chart(fig_status, use_container_width=True)
            
        with col_b:
            workload = df.groupby(["Assignee", "Status"])["ID"].count().reset_index()
            fig_workload = px.bar(workload, x="Assignee", y="ID", color="Status", title="Team Workload Distribution (Bottlenecks)")
            st.plotly_chart(fig_workload, use_container_width=True)
    else:
        st.info("Analytics will display once you add tasks.")

with tab3:
    st.subheader("Update or Remove Tasks")
    if not df.empty:
        st.dataframe(df[["ID", "Title", "Assignee", "Status", "Priority", "Estimated Hours", "Logged Hours"]], use_container_width=True)
        st.markdown("---")
        
        col_u, col_d = st.columns(2)
        
        with col_u:
            st.markdown("#### Update Task Progress")
            task_to_update = st.selectbox("Select Task", df["ID"].tolist(), format_func=lambda x: f"ID {x}: {df[df['ID']==x]['Title'].values[0]}")
            new_status = st.selectbox("New Status", ["To Do", "In Progress", "Done"])
            add_hours = st.number_input("Log Additional Hours", min_value=0.0, value=1.0, step=0.5)
            
            if st.button("Apply Update"):
                db.update_task_status(task_to_update, new_status, add_hours)
                st.success("Task updated successfully!")
                st.rerun()
                
        with col_d:
            st.markdown("#### Delete Task")
            task_to_delete = st.selectbox("Select Task to Remove", df["ID"].tolist(), format_func=lambda x: f"ID {x}: {df[df['ID']==x]['Title'].values[0]}", key="del_select")
            if st.button("Delete Task", type="primary"):
                db.delete_task(task_to_delete)
                st.warning("Task deleted successfully!")
                st.rerun()
    else:
        st.info("No tasks to manage.")