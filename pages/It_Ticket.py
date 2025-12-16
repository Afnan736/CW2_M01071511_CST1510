import streamlit as st
from app.db import get_connection
from app.ticket import get_it_tickets, add_ticket, update_ticket, delete_ticket
import pandas as pd

# Page configuration for IT Tickets dashboard
st.set_page_config(page_title='IT Tickets', page_icon='🎫', layout='wide')

# Login check 
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning('login to Access')
    st.stop()

# Connect to database and fetch IT tickets data
conn = get_connection()
data = get_it_tickets(conn)

# Convert created_at timestamp to datetime format for filtering
data['created_at'] = pd.to_datetime(data['created_at'])

# Dashboard title and description
st.title('IT Ticket Dashboard')
st.markdown("""
**_This IT Ticket Dashboard provides a centralized platform for monitoring, tracking, and managing IT support requests within 
            an organization. By consolidating ticket information such as priority, status, assigned personnel, resolution time, 
            and creation date, the dashboard enables stakeholders to quickly assess workload, identify critical issues, and optimize 
            resource allocation. With interactive filters, visual analytics, detailed metrics, and a comprehensive ticket table, users 
            can gain both a high-level overview and in-depth insights into IT support operations, improving efficiency and decision-making._**
""")

# Sidebar filters section
with st.sidebar:
    st.header('Filters')

    # Date filter toggle
    use_date_filter = st.checkbox('Filter by Date', value=False)
    selected_date = st.date_input('Select Date', value=data['created_at'].min().date())

    # Filter dropdowns for different ticket attributes
    priority = st.selectbox('Priority', ['All'] + list(data['priority'].unique()))
    status = st.selectbox('Status', ['All'] + list(data['status'].unique()))
    assigned = st.selectbox('Assigned To', ['All'] + list(data['assigned_to'].unique()))
    resolution = st.selectbox('Resolution Time Hours', ['All'] + list(data['resolution_time_hours'].unique()))

    # Logout button
    st.divider()
    if st.button('Log Out'):
        st.session_state['logged_in'] = False
        st.success('Logged out successfully!')
        st.rerun()

# Apply filters to data based on user selections
filtered = data.copy()

# Date filter
if use_date_filter:
    filtered = filtered[filtered['created_at'].dt.date == selected_date]

# Priority filter
if priority != 'All':
    filtered = filtered[filtered['priority'] == priority]

# Status filter
if status != 'All':
    filtered = filtered[filtered['status'] == status]

# Assigned to filter
if assigned != 'All':
    filtered = filtered[filtered['assigned_to'] == assigned]

# Resolution time filter
if resolution != 'All':
    filtered = filtered[filtered['resolution_time_hours'] == resolution]

# Charts section - two columns layout
chart_col1, chart_col2 = st.columns(2)

# First chart: Priority distribution (area chart)
with chart_col1:
    st.header('Priority Distribution')
    st.area_chart(filtered['priority'].value_counts())
    st.caption("""
    _The Priority Distribution area chart displays the volume of tickets across different priority levels, highlighting patterns 
               and workload distribution over time. By visualizing ticket accumulation in an area format, the chart helps users 
               identify periods with high ticket activity, understand which priority levels demand the most attention, and monitor
                trends in IT support demand. This visualization supports better planning, prioritization, and allocation of resources
                to ensure timely resolution of critical issues._
    """)

# Second chart: Ticket timeline (scatter chart)
with chart_col2:
    st.header('Ticket Timeline')
    st.scatter_chart(filtered, x='created_at', y='resolution_time_hours')
    st.caption("""
    _The Ticket Timeline scatter chart illustrates the creation of tickets over time alongside their resolution hours. 
               This visualization provides insights into trends such as peak periods, recurring issues, and variations in 
               resolution effort. By tracking ticket activity over time, users can identify patterns in workload, evaluate 
               response efficiency, and make informed decisions regarding staffing and operational improvements._
    """)

# Statistics Metrics section
st.header("Statistics Metrics")
st.markdown(""" _The Statistics Metrics section offers a concise overview of IT ticket activity, giving users immediate insight 
            into operational performance. It highlights essential measures such as total ticket count, distribution by status 
            (Open, In Progress, Resolved), average and maximum resolution times, number of high-priority tickets, and the total
             unique assignees handling tickets. These metrics help teams quickly understand workload patterns, spot potential 
            delays or bottlenecks, and make informed decisions to address critical issues efficiently._""")

# First row of metrics: Ticket status counts
cols = st.columns(4)
cols[0].metric("Total Tickets", len(filtered))
cols[1].metric("Open", len(filtered[filtered['status'] == 'Open']))
cols[2].metric("In Progress", len(filtered[filtered['status'] == 'In Progress']))
cols[3].metric("Resolved", len(filtered[filtered['status'] == 'Resolved']))

# Second row of metrics: Resolution times and priority analysis
cols2 = st.columns(4)
cols2[0].metric("Avg Resolution Hours", f"{filtered['resolution_time_hours'].mean():.1f}" if not filtered.empty else "0")
cols2[1].metric("Max Resolution Hours", f"{filtered['resolution_time_hours'].max():.1f}" if not filtered.empty else "0")
cols2[2].metric("High Priority", len(filtered[filtered.get('priority') == 'High']))
cols2[3].metric("Unique Assignees", filtered['assigned_to'].nunique() if not filtered.empty else 0)

# Detailed ticket data table
st.header("IT Ticket Details")

st.dataframe(filtered)
st.markdown("""
_The IT Ticket Details table presents a structured and comprehensive record of all support tickets. Each entry includes ticket ID,
             creation date, priority, description, status, assigned personnel, and resolution hours. Users can examine individual 
            tickets, verify information reflected in charts and metrics, and track progress over time. This table serves as a central 
            reference for detailed analysis, ensuring accurate record-keeping and supporting effective ticket management._
""")

# Ticket Management Section - CRUD operations
st.header("Ticket Management")

# Action selector for ticket operations
action = st.selectbox("Select Action", ["Add Ticket", "Update Ticket", "Delete Ticket"])

# ADD TICKET functionality
if action == "Add Ticket":
    st.subheader("Add Ticket")
    st.markdown(""" _The Add Ticket feature allows users to create new IT tickets directly within the dashboard. By entering 
                details such as ticket ID, priority, description, status, assigned personnel, and resolution hours, users ensure
                 that all relevant information is captured accurately. This feature helps maintain an up-to-date ticket database,
                 ensures no issues are overlooked, and supports efficient tracking and reporting of IT support activities._""")

    # Input form in two columns
    col1, col2 = st.columns(2)
    with col1:
        ticket_id = st.number_input("Ticket ID", min_value=3000)
        priority = st.selectbox("Priority", data['priority'].unique())
        description = st.text_input("Description")

    with col2:
        status = st.selectbox("Status", data['status'].unique())
        assigned = st.selectbox("Assigned To", data['assigned_to'].unique())
        resolution = st.number_input("Resolution Hours", min_value=0)

    # Add button
    if st.button("Add"):
        from datetime import datetime
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_ticket(conn, ticket_id, created_at, priority, description, status, assigned, resolution)
        st.success("Ticket Added")
        st.rerun()

# UPDATE TICKET functionality
elif action == "Update Ticket":
    st.subheader("Update Ticket")
    st.markdown(""" _The Update Ticket functionality enables users to modify existing ticket records, including priority, 
                description, status, assigned personnel, and resolution hours. By keeping ticket data current and reflective
                 of real-time developments, this feature ensures accurate reporting, facilitates monitoring of ticket progress,
                 and supports better decision-making. It also helps track the resolution process and maintain an organized IT support 
                workflow._""")

    # Check if there are tickets to update
    if filtered.empty:
        st.info("No tickets available.")
    else:
        # Select ticket to update
        ticket_id = st.selectbox("Select Ticket", filtered['ticket_id'])
        ticket = filtered[filtered['ticket_id'] == ticket_id].iloc[0]

        # Update form in two columns
        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox("Priority", data['priority'].unique())
            description = st.text_input("Description", ticket['description'])

        with col2:
            status = st.selectbox("Status", data['status'].unique())
            assigned = st.selectbox("Assigned To", data['assigned_to'].unique())
            resolution = st.number_input("Resolution Hours", value=int(ticket['resolution_time_hours']))

        # Update button
        if st.button("Update"):
            update_ticket(conn, ticket_id, ticket['created_at'], priority, description, status, assigned, resolution)
            st.success("Ticket Updated")
            st.rerun()

# DELETE TICKET functionality
elif action == "Delete Ticket":
    st.subheader("Delete Ticket")
    st.markdown(""" _The Delete Ticket option allows users to remove tickets that are resolved, irrelevant, or duplicated, helping 
                maintain a clean and accurate dataset. By eliminating outdated entries, the dashboard ensures that metrics, charts,
                 and tables reflect only relevant and actionable tickets. This capability enhances data quality, prevents misinterpretation 
                of ticket statistics, and supports efficient IT operations management._""")

    # Check if there are tickets to delete
    if filtered.empty:
        st.info("No tickets available.")
    else:
        # Select ticket to delete
        ticket_id = st.selectbox("Select Ticket", filtered['ticket_id'])

        # Delete button
        if st.button("Delete"):
            delete_ticket(conn, ticket_id)
            st.success("Ticket Deleted")
            st.rerun()

# Summary section (collapsible)
with st.expander("Summary"):
    st.write("""
    _The IT Ticket Dashboard integrates visualizations, metrics, and a detailed ticket table to provide a comprehensive overview 
             of IT support activities. Interactive filters allow focused exploration by priority, status, assigned personnel,
              resolution time, or date, enabling targeted analysis. The dashboard highlights trends, workload distribution, and 
             operational patterns, while providing tools for managing tickets efficiently. By combining actionable insights with 
             CRUD operations, the dashboard streamlines ticket handling, improves workflow visibility, and supports informed 
             decision making._

    _Overall, this IT Ticket Dashboard serves as an effective tool for managing and analyzing IT support operations. By combining
              visual insights, detailed records, metrics, and real-time ticket management capabilities, it empowers stakeholders to 
             respond promptly to critical issues, prioritize workload effectively, and improve operational efficiency. The dashboard
              enhances visibility into IT support processes, strengthens resource planning, and contributes to a more organized and 
             proactive IT service environment._
    """)