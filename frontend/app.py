import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8000"

st.title("🧠 AI Study Planner")

page = st.sidebar.radio("Navigation", ["Create Plan","Daily Tasks","Progress"])

if page == "Create Plan":

    goal = st.text_input("Learning Goal")
    days = st.number_input("Total Days", min_value=1, value=30)
    hours = st.slider("Hours per Day", 0.5, 6.0, step=0.5)
    start = st.date_input("Start Date", date.today())

    if st.button("Generate Study Plan"):

        if not goal.strip():
            st.error("Please enter a learning goal.")
        else:
            payload = {
                "goal": goal,
                "total_days": days,
                "daily_minutes": int(hours * 60),
                "start_date": str(start)
            }

            try:
                res = requests.post(f"{API_URL}/generate_plan", json=payload)

                st.write("Backend response:", res.text)

                if res.status_code == 200:
                    st.success("Plan generated!")
                else:
                    st.error("Backend error")

            except Exception as e:
                st.error(str(e))


elif page == "Daily Tasks":

    try:
        tasks = requests.get(f"{API_URL}/tasks").json()

        if len(tasks) == 0:
            st.warning("No tasks yet. Generate a plan first.")

        for t in tasks:
            checked = st.checkbox(
                f'{t["task_date"]} - {t["task_name"]} ({t["estimated_minutes"]} mins)',
                value=bool(t["is_completed"]),
                key=t["id"]
            )

            if checked != bool(t["is_completed"]):
                requests.post(
                    f"{API_URL}/update_task",
                    json={"task_id":t["id"],"is_completed":int(checked)}
                )

    except Exception as e:
        st.error(str(e))


elif page == "Progress":

    try:
        p = requests.get(f"{API_URL}/progress").json()

        st.progress(p["progress_percent"] / 100)
        st.metric("Completed", p["completed_tasks"])
        st.metric("Total Tasks", p["total_tasks"])
        st.metric("Progress %", p["progress_percent"])

    except Exception as e:
        st.error(str(e))
