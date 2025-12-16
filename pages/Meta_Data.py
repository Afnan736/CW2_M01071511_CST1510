import streamlit as st
from app.db import get_connection
from app.metadata import get_db_md, add_md, update_md, delete_md
import pandas as pd

# Page configuration for Datasets Metadata dashboard
st.set_page_config(page_title='Datasets Metadata', page_icon='📊', layout='wide')

# Login check
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning('login to Access')
    st.stop()

# Connect to database and fetch metadata
conn = get_connection()
data = get_db_md(conn)

# Convert upload_date to datetime for filtering
data['upload_date'] = pd.to_datetime(data['upload_date'])

# Dashboard title and description
st.title('Datasets Metadata Dashboard')
st.markdown("""
**_This Datasets Metadata Dashboard provides a centralized view of all datasets stored in the repository, enabling users to easily 
            explore, monitor, and manage dataset information. Through interactive filters, visual charts, and summary metrics, 
            the dashboard helps users analyze dataset uploads, understand data growth patterns, and identify key contributors. 
            It also supports efficient dataset management by allowing users to add, update, and delete metadata records, ensuring a
            ccurate and up-to-date dataset information._**
""")

# Sidebar filters section
with st.sidebar:
    st.header('Filters')

    # Date filter toggle
    use_date_filter = st.checkbox('Filter by Upload Date', value=False)
    selected_date = st.date_input('Select Upload Date', value=data['upload_date'].min().date())

    # Filter dropdowns for different metadata attributes
    uploaded_by = st.selectbox('Uploaded By', ['All'] + list(data['uploaded_by'].unique()))
    rows_filter = st.selectbox('Rows Range', ['All', 'Small (<1K)', 'Medium (1K-10K)', 'Large (>10K)'])
    columns_filter = st.selectbox('Columns Range', ['All', 'Small (<10)', 'Medium (10-20)', 'Large (>20)'])
    dataset_id = st.selectbox('Dataset ID', ['All'] + list(data['dataset_id'].unique()))

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
    filtered = filtered[filtered['upload_date'].dt.date == selected_date]

# Uploader filter
if uploaded_by != 'All':
    filtered = filtered[filtered['uploaded_by'] == uploaded_by]

# Rows range filter
if rows_filter == 'Small (<1K)':
    filtered = filtered[filtered['rows'] < 1000]
elif rows_filter == 'Medium (1K-10K)':
    filtered = filtered[(filtered['rows'] >= 1000) & (filtered['rows'] <= 10000)]
elif rows_filter == 'Large (>10K)':
    filtered = filtered[filtered['rows'] > 10000]

# Columns range filter
if columns_filter == 'Small (<10)':
    filtered = filtered[filtered['columns'] < 10]
elif columns_filter == 'Medium (10-20)':
    filtered = filtered[(filtered['columns'] >= 10) & (filtered['columns'] <= 20)]
elif columns_filter == 'Large (>20)':
    filtered = filtered[filtered['columns'] > 20]

# Dataset ID filter
if dataset_id != 'All':
    filtered = filtered[filtered['dataset_id'] == dataset_id]

# Charts section - two columns layout
chart_col1, chart_col2 = st.columns(2)

# First chart: Uploader distribution (area chart)
with chart_col1:
    st.header('Uploader Distribution')
    st.area_chart(filtered['uploaded_by'].value_counts())
    st.caption("""
    _The first graph illustrates the distribution of datasets across different uploaders, providing a clear view of individual 
               contribution levels within the repository. By visualizing the number of datasets submitted by each user, the chart
                helps identify the most active contributors, highlights patterns in dataset ownership, and supports better understanding 
               of workload distribution and user engagement in dataset creation activities._
    """)

# Second chart: Dataset rows vs columns trend (line chart)
with chart_col2:
    st.header('Dataset Rows vs Columns Trend')
    st.line_chart(filtered, x='columns', y='rows')
    st.caption("""
    _The line graph depicts the relationship between the number of columns and rows in each dataset, offering insight into dataset 
               structure and complexity. By visualizing how dataset size changes as the number of columns increases, the chart helps 
               identify trends, outliers, and common patterns in dataset design, supporting better understanding of data composition and 
               scalability._
    """)

# Metrics section - key dataset statistics
st.header("Dataset Statistics Summary")
st.markdown(""" _The metrics section provides a concise overview of key dataset statistics, offering immediate insight 
            into the overall state of the repository. It displays the total number of datasets, cumulative row and column counts, 
            and the average number of rows per dataset. These indicators allow users to quickly assess dataset volume, size distribution,
             and growth trends, supporting rapid evaluation and informed decision-making._ """)

# Dataset metrics in four columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Datasets", len(filtered))
col2.metric("Total Rows", f"{filtered['rows'].sum():,}")
col3.metric("Avg Rows/Dataset", f"{filtered['rows'].mean():,.0f}" if not filtered.empty else "0")
col4.metric("Total Columns", f"{filtered['columns'].sum():,}")

# Detailed metadata table
st.header("Dataset Details")

st.dataframe(filtered)
st.markdown("""
_The dataset metadata table presents a comprehensive and structured overview of all datasets available in the repository. 
            It includes detailed attributes such as dataset ID, dataset name, number of rows and columns, uploader information, 
            and upload date, enabling users to thoroughly review each dataset. This table serves as a central reference point for 
            validating trends observed in the charts and metrics, tracking dataset history, and ensuring metadata accuracy. Additionally, 
            it supports effective dataset governance by allowing users to add, update, and delete records, helping maintain consistency,
             reliability, and up-to-date information across the data repository._
""")

# Dataset management section - CRUD operations
st.header("Manage Datasets Metadata")
action = st.selectbox(
    "Select Action",
    ["Add Dataset", "Update Dataset", "Delete Dataset"]
)

# ADD DATASET functionality
if action == "Add Dataset":
    st.subheader("Add Dataset")
    st.markdown(""" _The Add Dataset feature allows users to register new datasets into the repository by entering essential 
                metadata such as dataset ID, name, size attributes, uploader details, and upload date. This structured input process
                 ensures consistency and completeness of metadata, supporting accurate tracking and seamless integration of new datasets 
                into the system._  """)

    # Input form in three columns
    col1, col2, col3 = st.columns(3)
    with col1:
        dataset_id = st.number_input("Dataset ID", min_value=1, step=1)
        name = st.text_input("Dataset Name")

    with col2:
        rows = st.number_input("Rows", min_value=1, step=1)
        columns = st.number_input("Columns", min_value=1, step=1)

    with col3:
        uploaded_by = st.text_input("Uploaded By")
        upload_date = st.date_input("Upload Date")

    # Add button
    if st.button("Add"):
        add_md(conn, dataset_id, name, rows, columns, uploaded_by, str(upload_date))
        st.success("Dataset has been added")
        st.rerun()

# UPDATE DATASET functionality
elif action == "Update Dataset":
    st.subheader("Update Dataset")
    st.markdown(""" _The Update Dataset functionality enables users to modify existing dataset metadata when changes occur. 
                By selecting a dataset and updating its attributes, users can ensure that information such as dataset size, uploader 
                details, and upload dates remain current. This capability helps maintain data accuracy and supports effective metadata 
                governance over time._ """)

    # Check if there are datasets to update
    if filtered.empty:
        st.info("No datasets available.")
    else:
        # Select dataset to update
        dataset_id = st.selectbox("Select Dataset", filtered['dataset_id'])
        dataset = filtered[filtered['dataset_id'] == dataset_id].iloc[0]

        # Update form in three columns
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Dataset Name", dataset['name'])

        with col2:
            rows = st.number_input("Rows", min_value=1, value=int(dataset['rows']))
            columns = st.number_input("Columns", min_value=1, value=int(dataset['columns']))

        with col3:
            uploaded_by = st.text_input("Uploaded By", dataset['uploaded_by'])
            upload_date = st.date_input("Upload Date", dataset['upload_date'].date())

        # Update button
        if st.button("Update"):
            update_md(conn, dataset_id, name, rows, columns, uploaded_by, str(upload_date))
            st.success("Dataset Updated")
            st.rerun()

# DELETE DATASET functionality
elif action == "Delete Dataset":
    st.subheader("Delete Dataset")
    st.markdown(""" _The Delete Dataset option allows users to safely remove outdated or unnecessary dataset records 
                from the repository. By presenting dataset details and requiring confirmation before deletion, this feature 
                helps prevent accidental data loss while ensuring that the metadata repository remains clean, relevant, and 
                well-maintained._
                """)

    # Check if there are datasets to delete
    if filtered.empty:
        st.info("No datasets available.")
    else:
        # Select dataset to delete
        dataset_id = st.selectbox("Select Dataset to Delete", filtered['dataset_id'])
        
        if dataset_id:
            dataset = filtered[filtered['dataset_id'] == dataset_id].iloc[0]
            
            # Display dataset details and confirmation
            st.warning(f"Delete Dataset #{dataset_id}?")
            st.write(f"**Name:** {dataset['name']}")
            st.write(f"**Rows:** {dataset['rows']:,} | **Columns:** {dataset['columns']}")
            st.write(f"**Uploaded By:** {dataset['uploaded_by']}")
            
            # Confirmation checkbox
            if st.checkbox("Confirm Delete"):
                if st.button("Delete Dataset"):
                    delete_md(conn, dataset_id)
                    st.success("Dataset Deleted!")
                    st.rerun()

# Summary section (collapsible)
with st.expander("Summary"):
    st.write("""
    _The Datasets Metadata Dashboard provides a centralized and interactive platform for exploring and managing dataset 
             information within the repository. By integrating dynamic filters, visual charts, summary metrics, and a detailed
              metadata table, the dashboard enables users to analyze dataset uploads, understand contributor activity, and evaluate
              dataset structure and growth. The uploader distribution and rows-versus-columns visualizations offer meaningful insights 
             into dataset ownership and complexity, while the metrics provide a concise overview of overall dataset statistics._

_In conclusion, this dashboard enhances dataset governance by ensuring accurate, consistent, and up-to-date metadata management.
              The ability to add, update, and delete dataset records directly through the interface streamlines administrative 
             tasks and improves data transparency. By presenting metadata in a clear and structured manner, the dashboard supports
              informed decision-making, efficient resource planning, and effective management of organizational data assets._
    """)