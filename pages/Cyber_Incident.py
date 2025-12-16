import streamlit as st
from app.db import get_connection
from app.incidence import get_cyber_incidents, add_incident, update_incident, delete_incident
import pandas as pd

# Set page title, icon and layout
st.set_page_config(page_title='Home', page_icon='💻', layout='wide')

# Login check 
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning('login to Access')
    st.stop()

# Connect to database and get incident data
conn = get_connection()
data = get_cyber_incidents(conn)

# Convert timestamp to datetime format for filtering
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Main dashboard title and description
st.title('Cyber Incidents')
st.markdown("""**_This dashboard serves as a centralized platform for monitoring, analyzing, and managing all cyber 
            incidents within the organization. It consolidates key incident information such as severity, status, category, 
            and timeline, providing stakeholders with a clear and actionable overview. By offering both visualizations and 
            detailed records, the dashboard supports informed decision making, quick prioritization of critical incidents, 
            and efficient management of security events._**""")

# Sidebar filters section
with st.sidebar:
    st.header('Filters')
    
    # Date filtering option
    use_date_filter = st.checkbox('Filter by Date', value=False, key='date_filter')
    selected_date = st.date_input('Select Date', value=data['timestamp'].min().date())
    
    # Filter dropdowns for different incident attributes
    severity = st.selectbox('Severity', ['All'] + list(data['severity'].unique()))
    status = st.selectbox('Status', ['All'] + list(data['status'].unique()))
    category = st.selectbox('Category', ['All'] + list(data['category'].unique()))
    incident_id = st.selectbox('Incident ID', ['All'] + list(data['incident_id'].unique()))
    
    # Logout button
    st.divider()
    if st.button('Log Out'):
        st.session_state['logged_in'] = False
        st.success('Logged out successfully!')
        st.rerun()

# Apply filters to data
filtered = data.copy()

# Date filter
if use_date_filter:
    filtered = filtered[filtered['timestamp'].dt.date == selected_date]

# Severity filter
if severity != 'All':
    filtered = filtered[filtered['severity'] == severity]

# Status filter
if status != 'All':
    filtered = filtered[filtered['status'] == status]

# Category filter
if category != 'All':
    filtered = filtered[filtered['category'] == category]

# Incident ID filter
if incident_id != 'All':
    filtered = filtered[filtered['incident_id'] == incident_id]

# Charts section - two columns layout
chart_col1, chart_col2 = st.columns(2)

# First chart: Severity distribution (bar chart)
with chart_col1:
    st.header('Status')
    st.bar_chart(filtered['severity'].value_counts())
    st.caption(""" _The status chart provides a clear and visually intuitive representation of how incidents are 
               distributed across different severity levels. By displaying counts for high, medium, and low severity 
               incidents, it allows users to quickly gauge the overall risk landscape. This chart is particularly useful
                for identifying urgent cases that may require immediate intervention, as well as understanding the balance
                of minor versus critical incidents. Such insights help organizations allocate resources efficiently, focus on 
               high-priority threats, and implement proactive measures to reduce potential impact._""")

# Second chart: Incident timeline (line chart)
with chart_col2:
    st.header('Timeline')
    st.line_chart(filtered, x='timestamp', y='incident_id')
    st.caption(""" _The timeline chart illustrates the occurrence of incidents over time, offering perspective on 
               cybersecurity events. Users can observe patterns such as periods of high incident frequency, recurring events,
                or spikes in specific types of incidents. By highlighting trends over days, weeks, or months, the timeline chart 
               helps security teams anticipate potential problem areas, optimize monitoring schedules, and evaluate the effectiveness 
               of mitigation strategies. This long-term view enhances situational awareness and supports strategic planning for incident 
               prevention._ """)

# Metrics section - key performance indicators
st.header("Cyber Incident Metrics")
st.markdown("""  _The metrics section provides quick insights into the current state of cyber incidents, presenting key numerical 
            summaries that highlight trends and potential risks. Metrics include the total number of incidents, the breakdown by status 
            (Open, In Progress, Closed), and distribution by severity (High, Medium, Low). Additionally, metrics indicate the number of 
            incidents that require immediate attention, enabling teams to focus on critical threats. These instant insights facilitate
             rapid assessment, allow for quick prioritization, and support operational decision making._ """)

# First row of metrics: Incident status counts
cols = st.columns(4)
cols[0].metric("Total", len(filtered))
cols[1].metric("In Progress", len(filtered[filtered['status'] == "In Progress"]))
cols[2].metric("Open", len(filtered[filtered['status'] == "Open"]))
cols[3].metric("Closed", len(filtered[filtered['status'] == "Closed"]))

# Second row of metrics: Severity and attention needed counts
cols2 = st.columns(4)
cols2[0].metric("High Severity", len(filtered[filtered['severity'] == "High"]))
cols2[1].metric("Medium Severity", len(filtered[filtered['severity'] == "Medium"]))
cols2[2].metric("Low Severity", len(filtered[filtered['severity'] == "Low"]))
cols2[3].metric("Needs Attention", len(filtered[filtered['status'].isin(["Open", "In Progress"])]))

# Detailed incident data table
st.header("Cyber Incident Details")
st.dataframe(filtered)
st.markdown(""" _The cyber incident table presents a comprehensive and detailed record of all incidents captured in the system. 
            Each entry includes essential information such as the incident ID, timestamp, severity, category, current status, 
            and a brief description of the event. Users can review individual incidents, verify information reflected in charts 
            and metrics, and track updates or changes over time. The table acts as a central reference for detailed analysis, 
             decision-making, and reporting, providing transparency and supporting accurate management of security events._ """)

# Incident management section (Add, Update, Delete)
st.header("Manage Cyber Incidents")

# Action selector
action = st.selectbox(
    "Select Action",
    ["Add Incident", "Update Incident", "Delete Incident"]
)

# ADD INCIDENT functionality
if action == "Add Incident":
    st.subheader("Add Incident")
    st.markdown(""" _The Add Incident functionality enables users to create new incident records directly within the dashboard,
                 ensuring that all relevant details are captured accurately. By specifying the incident ID, severity, category, status, 
                and description, users contribute to maintaining a comprehensive and up-to-date database. This feature helps organizations 
                ensure no incidents are overlooked, supports timely response, and allows for consistent documentation of security events.
                 Real time addition of incidents keeps the dashboard dynamic and reflective of the current cybersecurity environment._ """)

    # Input form in two columns
    col1, col2 = st.columns(2)
    with col1:
        incident_id = st.number_input("Incident ID", min_value=2000, step=1)
        severity = st.selectbox("Severity", data['severity'].unique())
        category = st.selectbox("Category", data['category'].unique())

    with col2:
        status = st.selectbox("Status", data['status'].unique())
        description = st.text_input("Description")

    # Add button
    if st.button("Add"):
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_incident(conn, incident_id, timestamp, severity, category, status, description)
        st.success("Incident Added")
        st.rerun()

# UPDATE INCIDENT functionality
elif action == "Update Incident":
    st.subheader("Update Incident")
    st.markdown(""" _The Update Incident feature allows users to modify existing records, including severity, status, category, or 
                description, keeping the dataset accurate and relevant. By updating incident information in real time, users ensure
                 that the current status of incidents is correctly reflected in both metrics and visualizations. This capability supports 
                continuous monitoring, helps teams track incident resolution progress, and provides a reliable foundation for reporting 
                and analysis. Accurate updates also assist in understanding incident trends and making informed operational and strategic 
                decisions. _ """)

    # Check if there are incidents to update
    if filtered.empty:
        st.info("No incidents available.")
    else:
        # Select incident to update
        incident_id = st.selectbox("Select Incident", filtered['incident_id'])
        incident = filtered[filtered['incident_id'] == incident_id].iloc[0]

        # Update form in two columns
        col1, col2 = st.columns(2)
        with col1:
            severity = st.selectbox("Severity", data['severity'].unique())
            category = st.selectbox("Category", data['category'].unique())

        with col2:
            status = st.selectbox("Status", data['status'].unique())
            description = st.text_input("Description", incident['description'])

        # Update button
        if st.button("Update"):
            update_incident(conn, incident_id, severity, category, status, description)
            st.success("Incident Updated")
            st.rerun()

# DELETE INCIDENT functionality
elif action == "Delete Incident":
    st.subheader("Delete Incident")
    st.markdown(""" _The Delete Incident functionality enables users to remove incidents that are resolved, duplicated, or no longer
                 relevant, helping maintain a clean and accurate dataset. By removing outdated or irrelevant entries, the system ensures
                 that metrics, charts, and tables reflect only active and meaningful data. This reduces clutter, prevents misinterpretation, 
                and enhances the clarity of visual and numerical insights. Proper data hygiene also supports reliable reporting, better 
                resource allocation, and efficient incident management._ """)

    # Check if there are incidents to delete
    if filtered.empty:
        st.info("No incidents available.")
    else:
        # Select incident to delete
        incident_id = st.selectbox("Select Incident", filtered['incident_id'])

        # Delete button
        if st.button("Delete"):
            delete_incident(conn, incident_id)
            st.success("Incident Deleted")
            st.rerun()

# Summary section (collapsible)
with st.expander("Summary"):
    st.write(
        """
         _This dashboard integrates visualizations, metrics, and detailed incident tables to provide a holistic view of the 
         organization’s cybersecurity landscape. Interactive filters allow users to explore incidents by severity, status, category, 
         or date, enabling targeted analysis of trends and patterns. The combination of charts, metrics, and detailed records supports 
         operational monitoring, quick assessment of high risk events, and effective incident management. By providing both overview and 
         granular detail, the dashboard ensures that users have the tools they need to make informed decisions, allocate resources 
         efficiently, and maintain an up-to-date understanding of the security environment._

         _Overall, this dashboard serves as an effective and user-friendly tool for monitoring, analyzing, and managing cyber incidents. 
         By combining detailed tables, visual insights, interactive metrics, and real time incident management capabilities, it empowers 
         stakeholders to respond proactively to emerging threats. The system facilitates prioritization of critical incidents, enhances 
         situational awareness, and strengthens organizational resilience against cyber risks. In essence, the dashboard provides a 
         comprehensive and actionable view of cybersecurity activity, supporting both day-to-day operations and strategic decision making._
        """)