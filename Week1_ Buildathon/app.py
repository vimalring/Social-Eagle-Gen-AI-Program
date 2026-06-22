import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Employee Leave Management",
    page_icon="🏖️",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
# 🏖️ Employee Leave Management System

Welcome back! Manage employee leaves, approvals, and reports.
""")

# --------------------------------------------------
# Sidebar Menu
# --------------------------------------------------

st.sidebar.title("🏖️ Leave Management")

menu = st.sidebar.radio(
    "",
    [
        "📊 Dashboard",
        "📝 Apply Leave",
        "📋 Leave History",
        "👨‍💼 Manager Dashboard"
    ]
)

# --------------------------------------------------
# Dashboard
# --------------------------------------------------

if menu == "📊 Dashboard":

    st.header("📊 Employee Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📋 Total Leaves", "10")

    with col2:
        st.metric("✅ Approved", "7")

    with col3:
        st.metric("⏳ Pending", "2")

    with col4:
        st.metric("❌ Rejected", "1")

    st.markdown("---")

    data = {
        "Status": [
            "Approved",
            "Pending",
            "Rejected"
        ],
        "Count": [
            7,
            2,
            1
        ]
    }

    fig = px.pie(
        data,
        names="Status",
        values="Count",
        title="Leave Status Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Apply Leave
# --------------------------------------------------

elif menu == "📝 Apply Leave":

    st.header("📝 Apply Leave")

    try:

        response = requests.get(
            "http://127.0.0.1:8000/employees"
        )

        employees = response.json()

        employee_options = []

        for emp in employees:

            employee_options.append(
                f"{emp['employee_id']} - {emp['name']}"
            )

        selected_employee = st.selectbox(
            "Select Employee",
            employee_options
        )

        st.info(
            f"Selected Employee: {selected_employee}"
        )

        employee_id = selected_employee.split(" - ")[0]

    except Exception as e:

        st.error(
            f"Unable to Load Employees: {e}"
        )

        st.stop()

    with st.container():

        st.subheader("Leave Request Form")

        leave_type = st.selectbox(
            "Leave Type",
            [
                "Casual Leave",
                "Sick Leave",
                "Earned Leave"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Start Date"
            )

        with col2:
            end_date = st.date_input(
                "End Date"
            )

        reason = st.text_area(
            "Reason",
            height=120
        )

    if st.button("Apply Leave"):

        payload = {
            "employee_id": employee_id,
            "leave_type": leave_type,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "reason": reason
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/leave",
                json=payload
            )

            if response.status_code == 200:

                st.success(
                    "Leave Applied Successfully ✅"
                )

            else:

                st.error(
                    f"Failed to Apply Leave ❌ Status Code: {response.status_code}"
                )

        except Exception as e:

            st.error(
                f"API Connection Error: {e}"
            )

# --------------------------------------------------
# Leave History
# --------------------------------------------------

elif menu == "📋 Leave History":

    st.header("📋 Leave History")

    employee_id = st.text_input(
        "Enter Employee ID"
    )

    if st.button("View Leave History"):

        try:

            response = requests.get(
                f"http://127.0.0.1:8000/leave-history/{employee_id}"
            )

            if response.status_code == 200:

                leave_history = response.json()

                if len(leave_history) > 0:

                    df = pd.DataFrame(
                        leave_history
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No Leave History Found"
                    )

            else:

                st.error(
                    "Unable to Fetch Leave History"
                )

        except Exception as e:

            st.error(
                f"API Connection Error: {e}"
            )

# --------------------------------------------------
# Manager Dashboard
# --------------------------------------------------

elif menu == "👨‍💼 Manager Dashboard":

    st.header("👨‍💼 Manager Dashboard")

    try:

        response = requests.get(
            "http://127.0.0.1:8000/pending-leaves"
        )

        leaves = response.json()

        st.info(
            f"Pending Requests: {len(leaves)}"
        )

        if len(leaves) == 0:

            st.success(
                "No Pending Leave Requests"
            )

        else:

            for leave in leaves:

                with st.expander(
                    f"{leave['employee_id']} - {leave['leave_type']}"
                ):

                    st.write(
                        f"Reason: {leave['reason']}"
                    )

                    st.write(
                        f"Status: {leave['status']}"
                    )

                    col1, col2 = st.columns(2)

                    if col1.button(
                        f"Approve {leave['id']}"
                    ):

                        requests.put(
                            f"http://127.0.0.1:8000/approve-leave/{leave['id']}"
                        )

                        st.success(
                            "Leave Approved ✅"
                        )

                        st.rerun()

                    if col2.button(
                        f"Reject {leave['id']}"
                    ):

                        requests.put(
                            f"http://127.0.0.1:8000/reject-leave/{leave['id']}"
                        )

                        st.error(
                            "Leave Rejected ❌"
                        )

                        st.rerun()

    except Exception as e:

        st.error(
            f"API Connection Error: {e}"
        )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Employee Leave Management System | Built using Streamlit + FastAPI + SQLite"
)