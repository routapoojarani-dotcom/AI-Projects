# Agile Task & Resource Tracker

An end-to-end, lightweight Agile task management and resource distribution dashboard built to eliminate engineering bottlenecks, track team velocity, and streamline sprint operations based on Google Project Management principles.

---

## Key Features

* Dynamic Kanban Board: Interactive task management separated into To Do, In Progress, and Done stages.
* Real-time Agile Analytics: Visual charts tracking task status distribution, estimated vs. logged hours, and completed sprint metrics.
* Resource Bottleneck Identification: Workload breakdown per developer/assignee to prevent burnout and uneven task allocation.
* Full Task CRUD Lifecycle: Easily add, edit status, log additional hours, or remove tasks on the fly.
* Persistent Storage: Built-in lightweight SQLite database engine with zero external configuration needed.

---

## Project Management Framework Documentation

### 1. Project Charter
* Project Name: Agile Resource & Task Tracker
* Project Sponsor: Engineering Operations Team
* Objective: Provide visual progress tracking and resource allocation metrics to reduce sprint blockers by 30%.
* In-Scope: Task creation, priority management, Kanban board, hour logging, workload analytics, deployment setup.
* Out-of-Scope: Third-party OAuth authentication, Slack/Jira webhook integration (Planned for v2.0).

### 2. User Stories
* As a Scrum Master, I want to view resource workload distribution so that I can identify burnouts and team bottlenecks early in the sprint.
* As a Developer, I want to log my work hours and change task states so that the team board reflects real-time progress.
* As a Product Owner, I want a high-level summary of total vs completed tasks so that I can measure release readiness and team velocity.

### 3. Risk Matrix
| Risk Event | Impact | Severity | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| Resource Over-allocation | High | High | Medium | Review workload bar charts during daily standups. |
| SQLite Database Lockouts | Medium | Low | Low | Migrate database layer to Supabase PostgreSQL for enterprise scale. |
| Data Loss on Server Restart | High | Medium | Low | Persistent volume storage mounting or cloud database integration. |

---

## System Architecture & Tech Stack

* Frontend Framework: Streamlit (Custom Web UI)
* Data Manipulation & Visualization: Pandas, Plotly Express
* Database Engine: SQLite3
* Language & Runtime: Python 3.10+
* Deployment Platform: Streamlit Community Cloud / Render

---