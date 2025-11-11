"""
TN Spark Analytical Dashboard
==============================
A comprehensive Streamlit application for analyzing educational data from TN SPARK EMIS system.

Features:
- Interactive data filtering by district and class
- Key performance metrics visualization
- Detailed analytics on schools, chapters, and syllabus completion
- Export capabilities for processed data
- Responsive design with modern UI

Author: Gokul
Created for: TN Spark Educational Analytics
"""

# Import required libraries for data processing and visualization
import streamlit as st  # Web application framework
import pandas as pd  # Data manipulation and analysis
import plotly.express as px  # Interactive plotting library
import plotly.graph_objects as go  # Advanced plotting capabilities
from datetime import datetime  # Date and time handling
import numpy as np  # Numerical computing
from io import BytesIO  # In-memory buffers for downloads
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode  # Advanced tables
from streamlit_plotly_events import plotly_events  # Chart click interactions

# Configure Streamlit page settings for optimal user experience
st.set_page_config(
    page_title="TN Spark Analytical Dashboard",  # Browser tab title
    page_icon="📊",  # Browser tab icon
    layout="wide",  # Use full screen width
    initial_sidebar_state="expanded"  # Show sidebar by default
)

# Establish consistent Plotly styling across the app
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = px.colors.qualitative.Set2

def apply_plotly_enhancements(fig, title_font_size=18):
    """
    Apply consistent layout and interaction improvements to Plotly figures.

    Args:
        fig: A Plotly figure object
        title_font_size (int): Title font size

    Returns:
        The updated figure
    """
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=50, b=10),
        hovermode="x unified",
        title=dict(font=dict(size=title_font_size)),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")
    return fig

# Custom CSS styling for enhanced UI/UX design
st.markdown("""
    <style>
    :root {
        --primary: #6366F1; /* indigo-500 */
        --secondary: #06B6D4; /* cyan-500 */
        --accent: #10B981; /* emerald-500 */
        --text: #111827; /* gray-900 */
        --muted: #6B7280; /* gray-500 */
        --bg: #FFFFFF;
        --card: #FFFFFF;
        --border: rgba(0,0,0,0.08);
        --shadow: 0 8px 24px rgba(0,0,0,0.08);
    }

    html, body, [class*="css"] {
        font-family: 'Segoe UI', system-ui, -apple-system, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, 'Noto Sans', 'Apple Color Emoji', 'Segoe UI Emoji';
    }

    /* Main dashboard header styling */
    .main-header {
        font-size: 2.2rem;
        color: var(--text);
        text-align: center;
        margin-bottom: 24px;
        font-weight: 700;
        letter-spacing: 0.2px;
    }
    
    /* Metric card styling for key performance indicators */
    .metric-card {
        background: var(--card);
        padding: 18px 16px;
        border-radius: 14px;
        color: var(--text);
        text-align: center;
        margin: 8px;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: transform 0.2s ease;
    }
    .metric-card:hover { transform: translateY(-2px); }
    
    /* Accent line */
    .metric-card::after {
        content: '';
        display: block;
        height: 4px;
        border-radius: 4px;
        margin-top: 12px;
        background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
    }
    
    /* Metric value display styling */
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    
    /* Metric label text styling */
    .metric-label {
        font-size: 0.9rem;
        color: var(--muted);
    }
    
    /* Section title styling for content organization */
    .section-title {
        color: var(--text);
        font-size: 1.3rem;
        font-weight: 700;
        margin: 18px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid var(--border);
    }
    
    /* DataFrame table styling */
    .stDataFrame {
        border: 1px solid var(--border);
        border-radius: 10px;
        box-shadow: var(--shadow);
    }
    </style>
""", unsafe_allow_html=True)

# Helper: check if PNG export is available (kaleido installed)
def can_export_png():
    try:
        import kaleido  # noqa: F401
        return True
    except Exception:
        return False

# Data Loading and Processing Functions
# =====================================

@st.cache_data  # Cache data to improve performance on repeated runs
def load_data():
    """
    Load CSV data from the TN SPARK report file.
    
    Returns:
        pd.DataFrame: Loaded data or None if file not found/error occurs
    """
    try:
        # Attempt to read the CSV file
        df = pd.read_csv('TN SPARK Overall reportReport (8).csv')
        st.success(f"✅ Successfully loaded {len(df):,} records from CSV file")
        return df
    except FileNotFoundError:
        # Handle file not found error
        st.error("❌ CSV file not found. Please ensure 'TN SPARK Overall reportReport (8).csv' is in the same directory.")
        return None
    except Exception as e:
        # Handle any other loading errors
        st.error(f"❌ Error loading CSV: {str(e)}")
        return None

@st.cache_data  # Cache preprocessing to avoid redundant operations
def preprocess_data(df):
    """
    Preprocess the loaded data for analysis.
    
    Args:
        df (pd.DataFrame): Raw data from CSV
        
    Returns:
        pd.DataFrame: Cleaned and processed data
    """
    # Convert date columns to datetime format for proper analysis
    if 'schedule_date' in df.columns:
        df['schedule_date'] = pd.to_datetime(df['schedule_date'], errors='coerce')
        st.info(f"📅 Converted schedule_date column to datetime format")
    
    if 'activity_date' in df.columns:
        df['activity_date'] = pd.to_datetime(df['activity_date'], errors='coerce')
        st.info(f"📅 Converted activity_date column to datetime format")
    
    # Clean and convert completion percentage to numeric format
    if 'completion_percentage' in df.columns:
        df['completion_percentage'] = pd.to_numeric(df['completion_percentage'], errors='coerce')
        st.info(f"📊 Converted completion_percentage column to numeric format")
    
    return df

# Main Dashboard Application
# ==========================

# Load and preprocess data
df = load_data()  # Attempt to load CSV data

if df is not None:  # Proceed only if data loading was successful
    # Preprocess the loaded data for analysis
    df = preprocess_data(df)
    
    # Display main dashboard header with custom styling
    st.markdown('<div class="main-header">TN Spark Analytical Dashboard</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--muted); font-size: 1.05rem;'>Educational Management Information System Analytics</p>", unsafe_allow_html=True)
    
    # Sidebar Configuration
    # =====================
    st.sidebar.header("📊 Dashboard Controls")
    st.sidebar.markdown("---")

    # Daily Report Upload
    st.sidebar.subheader("📤 Upload Daily Reports")
    st.sidebar.caption("Upload one or multiple CSV files to update today's dashboard.")
    uploaded_files = st.sidebar.file_uploader(
        "Select daily report CSV files",
        type=["csv"],
        accept_multiple_files=True,
        help="Drag & drop or browse to upload. Multiple files supported."
    )

    apply_mode = st.sidebar.radio(
        "Apply uploads as",
        ["Replace dataset", "Append to dataset"],
        help="Choose whether to replace the existing data or append to it."
    )

    def _read_csv_with_fallback(file_obj):
        try:
            return pd.read_csv(file_obj)
        except UnicodeDecodeError:
            try:
                file_obj.seek(0)
                return pd.read_csv(file_obj, encoding="latin1")
            except Exception as e:
                st.warning(f"Failed to read uploaded file: {e}")
                return None

    def _concat_with_union(dfs):
        if not dfs:
            return None
        all_cols = list({col for df_ in dfs for col in df_.columns})
        dfs_aligned = [df_.reindex(columns=all_cols) for df_ in dfs]
        return pd.concat(dfs_aligned, ignore_index=True)

    uploaded_df = None
    if uploaded_files:
        parsed = []
        for f in uploaded_files:
            df_u = _read_csv_with_fallback(f)
            if df_u is not None:
                parsed.append(df_u)
        if parsed:
            uploaded_df = _concat_with_union(parsed)
            st.success(f"✅ Processed {len(parsed)} uploaded file(s), total rows: {len(uploaded_df):,}")
        else:
            st.warning("No valid CSVs processed from uploads.")

    # Integrate uploaded data
    if uploaded_df is not None:
        if apply_mode == "Append to dataset" and df is not None:
            df = _concat_with_union([df, uploaded_df])
            st.info(f"📎 Appended uploads. Combined rows: {len(df):,}")
        else:
            df = uploaded_df
            st.info(f"🔁 Replaced dataset with uploads. Rows: {len(df):,}")
        # Reapply preprocessing on the newly formed dataset
        df = preprocess_data(df)
        st.sidebar.success("Dashboard updated with uploaded data.")
    
    st.sidebar.markdown("---")
    
    # District-based filtering for regional analysis
    if 'district_name' in df.columns:
        # Get unique districts and add "All" option
        districts = ['All'] + sorted(df['district_name'].dropna().unique().tolist())
        selected_district = st.sidebar.selectbox("Select District", districts, 
                                                help="Filter data by specific district")
    else:
        selected_district = 'All'  # Default to show all districts
    
    # Class-based filtering for grade-level analysis
    if 'class_id' in df.columns:
        # Get unique classes and add "All" option
        classes = ['All'] + sorted(df['class_id'].dropna().unique().tolist())
        selected_class = st.sidebar.selectbox("Select Class", classes,
                                            help="Filter data by specific class/grade")
    else:
        selected_class = 'All'  # Default to show all classes
    
    # Apply filters to create subset for analysis
    filtered_df = df.copy()  # Start with full dataset
    if selected_district != 'All':
        # Filter by selected district
        filtered_df = filtered_df[filtered_df['district_name'] == selected_district]
    if selected_class != 'All':
        # Filter by selected class
        filtered_df = filtered_df[filtered_df['class_id'] == selected_class]
    
    # Show filter summary & data source
    st.sidebar.markdown("---")
    st.sidebar.metric("Filtered Records", f"{len(filtered_df):,}")
    st.sidebar.metric("Total Records", f"{len(df):,}")
    data_source = "Uploaded files" if uploaded_df is not None else "Default CSV"
    st.sidebar.caption(f"Data Source: {data_source}")
    
    # Tabs for intuitive navigation
    tab_overview, tab_schools, tab_chapters, tab_syllabus, tab_more = st.tabs([
        "Overview", "Schools", "Chapters", "Syllabus", "More"
    ])

    # Overview Tab: KPIs and Data Quality
    with tab_overview:
        st.markdown("### 📈 Key Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_schools = filtered_df['school_name'].nunique() if 'school_name' in filtered_df.columns else 0
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{total_schools}</div>
                <div class='metric-label'>Schools with EMIS Entry</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            total_teachers = filtered_df['staff_id'].nunique() if 'staff_id' in filtered_df.columns else 0
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{total_teachers}</div>
                <div class='metric-label'>Active Teachers</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            total_classes = filtered_df['class_id'].nunique() if 'class_id' in filtered_df.columns else 0
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{total_classes}</div>
                <div class='metric-label'>Classes Covered</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            avg_completion = filtered_df['completion_percentage'].mean() if 'completion_percentage' in filtered_df.columns else 0
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{avg_completion:.1f}%</div>
                <div class='metric-label'>Average Completion</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        with st.expander("📋 Data Quality Summary"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Data Overview:**")
                st.write(f"Total Records: {len(filtered_df):,}")
                st.write(f"Total Columns: {len(filtered_df.columns)}")
                st.write(f"Missing Values: {filtered_df.isnull().sum().sum():,}")
                st.write(f"Duplicate Rows: {filtered_df.duplicated().sum():,}")
            with col2:
                st.markdown("**Column Information:**")
                column_info = pd.DataFrame({
                    'Column': filtered_df.columns,
                    'Data Type': filtered_df.dtypes.astype(str).values,
                    'Non-Null Count': filtered_df.count().values,
                    'Missing %': (filtered_df.isnull().sum() / len(filtered_df) * 100).round(2).values
                })
                st.dataframe(column_info, width='stretch')

            csv_processed = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Processed Data",
                data=csv_processed,
                file_name="processed_emis_data.csv",
                mime="text/csv"
            )

    # Schools Tab
    with tab_schools:
        st.markdown("### 🏫 Schools that started EMIS Entry")
        if 'school_name' in filtered_df.columns:
            schools_data = filtered_df.groupby([
                'school_name', 'district_name', 'block_name', 'udise_code', 'category'
            ]).size().reset_index(name='count')
            schools_data = schools_data.drop('count', axis=1)
            st.dataframe(schools_data, width='stretch')

            csv_schools = schools_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Schools Data",
                data=csv_schools,
                file_name="schools_emis_entry.csv",
                mime="text/csv",
                help="Download the schools data as CSV file"
            )
        else:
            st.warning("⚠️ School name column not found in the dataset.")

    # Chapters Tab
    with tab_chapters:
        st.markdown("### 📚 Chapters Completed per School and Section")
        required_chapter_cols = ['school_name', 'class_id', 'class_section', 'Completed_topic', 'completion_percentage']
        if all(col in filtered_df.columns for col in required_chapter_cols):
            chapters_data = filtered_df.groupby(['school_name', 'class_id', 'class_section']).agg({
                'Completed_topic': lambda x: (x != '0').sum(),
                'completion_percentage': 'max'
            }).reset_index()
            chapters_data.columns = ['School Name', 'Class', 'Section', 'Chapters Completed', 'Completion %']
            # Enhanced table using AG Grid
            gb_ch = GridOptionsBuilder.from_dataframe(chapters_data)
            gb_ch.configure_default_column(resizable=True, sortable=True, filter=True)
            gb_ch.configure_pagination(paginationAutoPageSize=True)
            gb_ch.configure_column('School Name', pinned=True)
            AgGrid(chapters_data, gridOptions=gb_ch.build(), height=260, theme='alpine')

            top_chapters = chapters_data.sort_values(by='Chapters Completed', ascending=False).head(20)
            fig_chapters = px.bar(
                top_chapters,
                x='Chapters Completed',
                y='School Name',
                color='Class',
                orientation='h',
                text='Chapters Completed',
                title='Top 20 Schools by Chapters Completed',
                height=480,
                labels={'Chapters Completed': 'Number of Chapters', 'School Name': 'School'}
            )
            fig_chapters.update_traces(textposition='outside')
            fig_chapters = apply_plotly_enhancements(fig_chapters)
            st.plotly_chart(fig_chapters, use_container_width=True)

            # Click-to-filter on chart
            selected_points = plotly_events(fig_chapters, click_event=True, hover_event=False, select_event=False, key="chapters_click", override_height=480)
            if selected_points:
                sel_school = selected_points[0].get('y')
                st.info(f"🔎 Filtering table for: {sel_school}")
                if sel_school:
                    filtered_sel = chapters_data[chapters_data['School Name'] == sel_school]
                    AgGrid(filtered_sel, gridOptions=GridOptionsBuilder.from_dataframe(filtered_sel).build(), height=200, theme='alpine')

            # Export chart as PNG (graceful fallback if kaleido missing)
            if can_export_png():
                buf = BytesIO()
                fig_chapters.write_image(buf, format='png', width=1200, height=600, scale=2)
                st.download_button("🖼️ Download chart (PNG)", buf.getvalue(), file_name="top_chapters.png", mime="image/png")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Chapters Completed", f"{chapters_data['Chapters Completed'].sum():,}")
            with col2:
                st.metric("Average Completion Rate", f"{chapters_data['Completion %'].mean():.1f}%")
        else:
            missing_cols = [col for col in required_chapter_cols if col not in filtered_df.columns]
            st.warning(f"⚠️ Required columns for chapter analysis not found: {', '.join(missing_cols)}")

    # Syllabus Tab
    with tab_syllabus:
        st.markdown("### 📊 Syllabus Completion by Level")
        if 'class_id' in filtered_df.columns and 'completion_percentage' in filtered_df.columns:
            syllabus_data = filtered_df.groupby('class_id').agg({
                'completion_percentage': ['max', 'mean'],
                'activity_date': 'max'
            }).reset_index()
            syllabus_data.columns = ['Class', 'Max Completion %', 'Avg Completion %', 'Last Activity Date']
            # Replace DataFrame viewer with AG Grid
            gb_syl = GridOptionsBuilder.from_dataframe(syllabus_data)
            gb_syl.configure_default_column(resizable=True, sortable=True, filter=True)
            gb_syl.configure_pagination(paginationAutoPageSize=True)
            gb_syl.configure_side_bar()
            gb_syl.configure_column('Class', pinned=True)
            AgGrid(syllabus_data, gridOptions=gb_syl.build(), height=260, theme='alpine')

            fig_syllabus = px.area(
                syllabus_data,
                x='Class',
                y=['Max Completion %', 'Avg Completion %'],
                title='Completion Percentage Trends by Class (Stacked Area)',
                height=420,
                labels={'value': 'Completion Percentage', 'variable': 'Metric Type'}
            )
            fig_syllabus.update_layout(
                xaxis_title="Class",
                yaxis_title="Completion Percentage",
                legend_title="Completion Type"
            )
            fig_syllabus = apply_plotly_enhancements(fig_syllabus)
            st.plotly_chart(fig_syllabus, use_container_width=True)

            # Click-to-filter on syllabus chart by Class
            syl_sel = plotly_events(fig_syllabus, click_event=True, hover_event=False, select_event=False, key="syl_click", override_height=420)
            if syl_sel:
                target_class = syl_sel[0].get('x')
                if target_class is not None:
                    st.info(f"🔎 Filtering syllabus table to Class {target_class}")
                    sub = filtered_df[filtered_df['class_id'] == target_class]
                    if not sub.empty:
                        AgGrid(sub, gridOptions=GridOptionsBuilder.from_dataframe(sub).build(), height=220, theme='alpine')

            # Export chart as PNG
            if can_export_png():
                buf_syl = BytesIO()
                fig_syllabus.write_image(buf_syl, format='png', width=1200, height=600, scale=2)
                st.download_button("🖼️ Download syllabus chart (PNG)", buf_syl.getvalue(), file_name="syllabus_completion.png", mime="image/png")

            col1, col2, col3 = st.columns(3)
            with col1:
                best_class = syllabus_data.loc[syllabus_data['Max Completion %'].idxmax(), 'Class']
                st.metric("Best Performing Class", f"Class {best_class}")
            with col2:
                avg_max_completion = syllabus_data['Max Completion %'].mean()
                st.metric("Average Max Completion", f"{avg_max_completion:.1f}%")
            with col3:
                total_classes = len(syllabus_data)
                st.metric("Total Classes", f"{total_classes}")
        else:
            missing_cols = []
            if 'class_id' not in filtered_df.columns:
                missing_cols.append('class_id')
            if 'completion_percentage' not in filtered_df.columns:
                missing_cols.append('completion_percentage')
            st.warning(f"⚠️ Required columns for syllabus completion analysis not found: {', '.join(missing_cols)}")

    # More Analytics Tab
    with tab_more:
        st.markdown("### 📈 Additional Analytics")
        col1, col2 = st.columns(2)

        with col1:
            if 'district_name' in filtered_df.columns and 'completion_percentage' in filtered_df.columns:
                district_completion = (
                    filtered_df.groupby('district_name')['completion_percentage']
                    .mean()
                    .sort_values(ascending=False)
                    .head(10)
                )
                fig_district = px.bar(
                    y=district_completion.index,
                    x=district_completion.values,
                    orientation='h',
                    title='Top 10 Districts by Average Completion',
                    labels={'x': 'Average Completion %', 'y': 'District'},
                    height=420
                )
                fig_district = apply_plotly_enhancements(fig_district)
                st.plotly_chart(fig_district, use_container_width=True)

                # Click-to-filter: show district-specific snapshot
                sel_district = plotly_events(fig_district, click_event=True, hover_event=False, select_event=False, key="district_click", override_height=420)
                if sel_district:
                    dname = sel_district[0].get('y')
                    st.info(f"🔎 Filtering to district: {dname}")
                    if dname:
                        dtable = filtered_df[filtered_df['district_name'] == dname]
                        gb = GridOptionsBuilder.from_dataframe(dtable)
                        gb.configure_default_column(resizable=True, sortable=True, filter=True)
                        gb.configure_pagination(paginationAutoPageSize=True)
                        gb.configure_column('school_name', pinned=True)
                        AgGrid(dtable, gridOptions=gb.build(), height=240, theme='alpine')

                # Export chart as PNG
                if can_export_png():
                    bufd = BytesIO()
                    fig_district.write_image(bufd, format='png', width=1200, height=600, scale=2)
                    st.download_button("🖼️ Download district chart (PNG)", bufd.getvalue(), file_name="district_completion.png", mime="image/png")

        with col2:
            if 'attedance_status' in filtered_df.columns:
                attendance_counts = filtered_df['attedance_status'].value_counts()
                fig_attendance = px.pie(
                    values=attendance_counts.values,
                    names=attendance_counts.index,
                    hole=0.4,
                    title='Teacher Attendance Status Distribution',
                    height=420
                )
                fig_attendance.update_traces(textinfo='percent+label', pull=[0.02]*len(attendance_counts))
                fig_attendance = apply_plotly_enhancements(fig_attendance)
                st.plotly_chart(fig_attendance, use_container_width=True)

        # Trends Over Time
        st.markdown("### ⏱️ Trends Over Time")
        if 'activity_date' in filtered_df.columns and 'completion_percentage' in filtered_df.columns:
            @st.cache_data(show_spinner=False)
            def compute_completion_trend(df):
                ts = (
                    df.dropna(subset=['activity_date', 'completion_percentage'])
                      .groupby('activity_date')['completion_percentage']
                      .mean()
                      .sort_index()
                )
                trend = ts.to_frame('avg_completion')
                trend['rolling_7d'] = trend['avg_completion'].rolling(7, min_periods=1).mean()
                return trend.reset_index()

            trend_df = compute_completion_trend(filtered_df)
            render_trend = st.toggle("Show completion trend", value=True)
            if render_trend and not trend_df.empty:
                fig_trend = px.line(
                    trend_df,
                    x='activity_date',
                    y=['avg_completion', 'rolling_7d'],
                    labels={'value': 'Completion %', 'variable': 'Series'},
                    title='Daily Completion % and 7-day Moving Average',
                    height=420
                )
                fig_trend = apply_plotly_enhancements(fig_trend)
                st.plotly_chart(fig_trend, use_container_width=True)
                if can_export_png():
                    buf_tr = BytesIO()
                    fig_trend.write_image(buf_tr, format='png', width=1200, height=600, scale=2)
                    st.download_button("🖼️ Download trend chart (PNG)", buf_tr.getvalue(), file_name="completion_trend.png", mime="image/png")

        # Alerts & Watchlists
        st.markdown("### 🔥 Alerts & Watchlists")
        if 'school_name' in filtered_df.columns and 'activity_date' in filtered_df.columns:
            @st.cache_data(show_spinner=False)
            def compute_alerts(df, days_without_activity=7):
                latest_by_school = df.groupby('school_name')['activity_date'].max().reset_index(name='last_activity')
                cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=days_without_activity)
                stale = latest_by_school[latest_by_school['last_activity'] < cutoff]
                declines = []
                if 'class_id' in df.columns and 'completion_percentage' in df.columns:
                    recent_cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=7)
                    prev_cutoff = recent_cutoff - pd.Timedelta(days=7)
                    recent = df[(df['activity_date'] >= recent_cutoff) & (df['activity_date'] <= pd.Timestamp.today().normalize())]
                    prev = df[(df['activity_date'] >= prev_cutoff) & (df['activity_date'] < recent_cutoff)]
                    r = recent.groupby('class_id')['completion_percentage'].mean()
                    p = prev.groupby('class_id')['completion_percentage'].mean()
                    comp = pd.DataFrame({'recent': r, 'prev': p}).dropna()
                    comp['delta'] = comp['recent'] - comp['prev']
                    declines = comp.nsmallest(5, 'delta').reset_index()
                return stale, declines

            stale_schools, declining_classes = compute_alerts(filtered_df)
            if not stale_schools.empty:
                st.warning(f"Schools with no activity in last 7 days: {len(stale_schools)}")
                AgGrid(stale_schools, gridOptions=GridOptionsBuilder.from_dataframe(stale_schools).build(), height=200, theme='alpine')
            else:
                st.success("All schools show recent activity in the selected range.")

            if isinstance(declining_classes, pd.DataFrame) and not declining_classes.empty:
                st.warning("Top classes with declining completion vs previous week")
                AgGrid(declining_classes.rename(columns={'class_id':'Class'}), gridOptions=GridOptionsBuilder.from_dataframe(declining_classes).build(), height=200, theme='alpine')
            else:
                st.info("No significant declines detected for classes in the selected window.")

        # Heatmap: Completion by Month and School
        st.markdown("### 🗺️ Heatmap: Completion by Month and School")
        if 'school_name' in filtered_df.columns and 'activity_date' in filtered_df.columns and 'completion_percentage' in filtered_df.columns:
            @st.cache_data(show_spinner=False)
            def compute_heatmap(df):
                df2 = df.copy()
                df2['month'] = df2['activity_date'].dt.to_period('M').astype(str)
                pivot = (
                    df2.groupby(['school_name', 'month'])['completion_percentage']
                       .mean()
                       .reset_index()
                )
                mat = pivot.pivot(index='school_name', columns='month', values='completion_percentage')
                return mat

            mat = compute_heatmap(filtered_df)
            render_heatmap = st.toggle("Show heatmap", value=True)
            if render_heatmap and not mat.empty:
                fig_hm = px.imshow(
                    mat,
                    labels=dict(x="Month", y="School", color="Completion %"),
                    aspect='auto',
                    title='Average Completion % by School and Month',
                    color_continuous_scale='Viridis',
                    height=520
                )
                fig_hm = apply_plotly_enhancements(fig_hm)
                st.plotly_chart(fig_hm, use_container_width=True)
                if can_export_png():
                    buf_hm = BytesIO()
                    fig_hm.write_image(buf_hm, format='png', width=1200, height=600, scale=2)
                    st.download_button("🖼️ Download heatmap (PNG)", buf_hm.getvalue(), file_name="completion_heatmap.png", mime="image/png")

else:
    # Error handling for data loading failure
    # ======================================
    st.error("❌ Unable to load data. Please check if the CSV file exists and is accessible.")
    
    # Provide helpful troubleshooting information
    with st.expander("🔧 Troubleshooting Guide"):
        st.markdown("""
        **Possible Solutions:**
        1. **Check File Location**: Ensure 'TN SPARK Overall reportReport (8).csv' is in the same directory as this script
        2. **File Permissions**: Verify you have read permissions for the CSV file
        3. **File Format**: Ensure the file is a valid CSV format
        4. **Encoding**: Try specifying encoding if the file contains special characters
        
        **Expected File Structure:**
        The CSV should contain columns such as:
        - school_name, district_name, block_name, udise_code
        - class_id, class_section, completion_percentage
        - Completed_topic, activity_date, staff_id
        """)
    
    # Show current directory contents for debugging
    st.info("📁 Current Directory Contents:")
    try:
        import os
        files = os.listdir('.')
        csv_files = [f for f in files if f.endswith('.csv')]
        if csv_files:
            st.write("Found CSV files:", csv_files)
        else:
            st.write("No CSV files found in current directory")
    except Exception as e:
        st.write("Unable to list directory contents:", str(e))

# Application Footer
# ==================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem;'>TN Spark Analytical Dashboard | Built with Streamlit | Educational Management Information System Analytics</p>", unsafe_allow_html=True)

# Performance and debugging information (hidden by default)
if st.checkbox("🔍 Show Debug Information"):
    st.markdown("### Debug Information")
    st.write("Streamlit Version:", st.__version__)
    st.write("Pandas Version:", pd.__version__)
    st.write("Python Version:", "3.x")
    st.write("Memory Usage:", "Optimized with caching")
    st.write("Last Updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))