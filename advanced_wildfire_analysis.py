import streamlit as st
import boto3
from io import BytesIO
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="🔥 Advanced Wildfire Analysis",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #ff6b35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b35;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_wildfire_data():
    """Load wildfire data from S3"""
    try:
        # Access Streamlit secrets
        aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
        bucket_name = st.secrets["S3_BUCKET_NAME"]
        file_path = st.secrets["S3_OBJECT_KEY"]
        
        st.info("☁️ Loading wildfire data from S3...")
        
        # Connect to S3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        
        # Download the file into memory
        obj = s3.get_object(Bucket=bucket_name, Key=file_path)
        geojson_data = obj["Body"].read()
        
        # Load it using GeoPandas
        gdf = gpd.read_file(BytesIO(geojson_data))
        
        st.success(f"✅ Successfully loaded {len(gdf):,} wildfire records!")
        return gdf
        
    except Exception as e:
        st.error(f"❌ Failed to load data: {str(e)}")
        return None

def clean_and_prepare_data(gdf):
    """Clean and prepare the data for analysis"""
    if gdf is None:
        return None
    
    # Make a copy to avoid modifying original
    df = gdf.copy()
    
    # Clean column names and handle missing values
    if 'TOTALACRES' in df.columns:
        df['TOTALACRES'] = pd.to_numeric(df['TOTALACRES'], errors='coerce').fillna(0)
    
    if 'FIREYEAR' in df.columns:
        df['FIREYEAR'] = pd.to_numeric(df['FIREYEAR'], errors='coerce')
        df = df[df['FIREYEAR'].notna()]
        # Convert to integer to avoid decimal issues
        df['FIREYEAR'] = df['FIREYEAR'].astype(int)
    
    # Clean cause data
    if 'STATCAUSE' in df.columns:
        df['STATCAUSE'] = df['STATCAUSE'].fillna('Unknown')
        # Simplify cause categories
        cause_mapping = {
            'Lightning': 'Natural',
            'Equipment Use': 'Human',
            'Smoking': 'Human', 
            'Campfire': 'Human',
            'Debris Burning': 'Human',
            'Railroad': 'Human',
            'Arson': 'Human',
            'Children': 'Human',
            'Miscellaneous': 'Other',
            'Fireworks': 'Human',
            'Powerline': 'Human',
            'Unknown': 'Unknown'
        }
        df['CAUSE_CATEGORY'] = df['STATCAUSE'].map(lambda x: cause_mapping.get(x, 'Other'))
    
    # Add fire size categories
    if 'TOTALACRES' in df.columns:
        df['FIRE_SIZE_CATEGORY'] = pd.cut(
            df['TOTALACRES'],
            bins=[0, 10, 100, 1000, 10000, float('inf')],
            labels=['Small (<10)', 'Medium (10-100)', 'Large (100-1000)', 'Very Large (1000-10000)', 'Mega (>10000)']
        )
    
    return df

def show_advanced_overview(df):
    """Show advanced overview with powerful insights"""
    st.markdown('<h1 class="main-header">🔥 Advanced Wildfire Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    if df is None:
        st.error("No data available for analysis")
        return
    
    # Key metrics with more detail
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Fires", f"{len(df):,}")
        if 'FIREYEAR' in df.columns:
            st.caption(f"Years: {df['FIREYEAR'].min():.0f} - {df['FIREYEAR'].max():.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if 'TOTALACRES' in df.columns:
            total_acres = df['TOTALACRES'].sum()
            avg_acres = df['TOTALACRES'].mean()
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Acres Burned", f"{total_acres:,.0f}")
            st.caption(f"Avg: {avg_acres:.1f} acres/fire")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        if 'STATENAME' in df.columns:
            states = df['STATENAME'].nunique()
            top_state = df['STATENAME'].value_counts().index[0] if len(df) > 0 else "N/A"
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("States Affected", states)
            st.caption(f"Most fires: {top_state}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        if 'STATCAUSE' in df.columns:
            top_cause = df['STATCAUSE'].value_counts().index[0] if len(df) > 0 else "N/A"
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Top Cause", top_cause)
            st.caption(f"Most common fire cause")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced insights
    st.markdown("## 📊 Advanced Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("### 🔥 **Fire Severity Analysis**")
        if 'TOTALACRES' in df.columns:
            large_fires = df[df['TOTALACRES'] > 1000]
            mega_fires = df[df['TOTALACRES'] > 10000]
            st.write(f"• **Large fires (>1000 acres):** {len(large_fires):,} ({len(large_fires)/len(df)*100:.1f}%)")
            st.write(f"• **Mega fires (>10000 acres):** {len(mega_fires):,} ({len(mega_fires)/len(df)*100:.1f}%)")
            st.write(f"• **Largest fire:** {df['TOTALACRES'].max():,.0f} acres")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("### 📅 **Temporal Trends**")
        if 'FIREYEAR' in df.columns:
            recent_year = df['FIREYEAR'].max()
            recent_fires = len(df[df['FIREYEAR'] == recent_year])
            avg_per_year = len(df) / (df['FIREYEAR'].max() - df['FIREYEAR'].min() + 1)
            st.write(f"• **Most recent year:** {recent_year}")
            st.write(f"• **Fires in {recent_year}:** {recent_fires:,}")
            st.write(f"• **Average per year:** {avg_per_year:.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Trend analysis
    if 'FIREYEAR' in df.columns and 'TOTALACRES' in df.columns:
        st.markdown("### 📈 Fire Trends Over Time")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Yearly fire counts
            yearly_fires = df['FIREYEAR'].value_counts().sort_index()
            fig = px.line(
                x=yearly_fires.index,
                y=yearly_fires.values,
                title="Wildfires per Year",
                labels={'x': 'Year', 'y': 'Number of Fires'}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Yearly total acres
            yearly_acres = df.groupby('FIREYEAR')['TOTALACRES'].sum()
            fig = px.line(
                x=yearly_acres.index,
                y=yearly_acres.values,
                title="Total Acres Burned per Year",
                labels={'x': 'Year', 'y': 'Total Acres'}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

def show_advanced_causes_analysis(df):
    """Show advanced fire causes analysis"""
    st.markdown("## 🔥 Advanced Fire Causes Analysis")
    
    if df is None or 'STATCAUSE' not in df.columns:
        st.warning("Fire cause data not available")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Fire Causes Distribution")
        
        # Create pie chart for fire causes
        cause_counts = df['STATCAUSE'].value_counts().head(10)
        
        fig = px.pie(
            values=cause_counts.values,
            names=cause_counts.index,
            title="Top 10 Fire Causes",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Cause Categories")
        
        if 'CAUSE_CATEGORY' in df.columns:
            category_counts = df['CAUSE_CATEGORY'].value_counts()
            
            fig = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Fire Causes by Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    # Advanced cause analysis
    st.markdown("### 🔍 Detailed Cause Analysis")
    
    if 'STATCAUSE' in df.columns and 'TOTALACRES' in df.columns:
        cause_analysis = df.groupby('STATCAUSE').agg({
            'TOTALACRES': ['count', 'sum', 'mean', 'max'],
            'FIREYEAR': 'nunique' if 'FIREYEAR' in df.columns else 'count'
        }).round(2)
        
        cause_analysis.columns = ['Fire Count', 'Total Acres', 'Avg Acres', 'Largest Fire', 'Years Active']
        cause_analysis = cause_analysis.sort_values('Fire Count', ascending=False)
        
        st.dataframe(cause_analysis.head(15))
        
        # Cause vs size analysis
        st.markdown("### 📊 Cause vs Fire Size Analysis")
        
        if 'FIRE_SIZE_CATEGORY' in df.columns:
            cause_size = pd.crosstab(df['STATCAUSE'], df['FIRE_SIZE_CATEGORY'])
            fig = px.imshow(
                cause_size,
                title="Fire Causes vs Size Categories",
                labels=dict(x="Fire Size", y="Cause", color="Number of Fires")
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def show_advanced_spatial_analysis(df):
    """Show advanced spatial analysis with better visualization"""
    st.markdown("## 🗺️ Advanced Spatial Analysis")
    
    if df is None:
        st.warning("No data available for spatial analysis")
        return
    
    # Map controls
    st.markdown("### 🎛️ Map Controls")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sample_size = st.slider("Sample Size", 100, 10000, 5000, help="Number of points to show on map")
    
    with col2:
        size_filter = st.selectbox(
            "Filter by Fire Size",
            ["All Fires", "Small (<10 acres)", "Medium (10-100)", "Large (100-1000)", "Very Large (1000-10000)", "Mega (>10000)"]
        )
    
    with col3:
        # Fix year filter - convert to integer properly
        if 'FIREYEAR' in df.columns:
            available_years = sorted(df['FIREYEAR'].unique())
            year_options = ["All Years"] + [str(int(year)) for year in available_years]
            year_filter = st.selectbox("Filter by Year", year_options)
        else:
            year_filter = "All Years"
    
    # Apply filters
    filtered_df = df.copy()
    
    if size_filter != "All Fires" and 'FIRE_SIZE_CATEGORY' in filtered_df.columns:
        size_mapping = {
            "Small (<10 acres)": "Small (<10)",
            "Medium (10-100)": "Medium (10-100)",
            "Large (100-1000)": "Large (100-1000)",
            "Very Large (1000-10000)": "Very Large (1000-10000)",
            "Mega (>10000)": "Mega (>10000)"
        }
        filtered_df = filtered_df[filtered_df['FIRE_SIZE_CATEGORY'] == size_mapping[size_filter]]
    
    if year_filter != "All Years" and 'FIREYEAR' in filtered_df.columns:
        try:
            year_int = int(year_filter)
            filtered_df = filtered_df[filtered_df['FIREYEAR'] == year_int]
        except ValueError:
            st.error(f"Invalid year format: {year_filter}")
    
    # Sample the data for better performance
    if len(filtered_df) > sample_size:
        filtered_df = filtered_df.sample(n=sample_size, random_state=42)
    
    st.info(f"Showing {len(filtered_df):,} fires on the map")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Interactive Fire Map")
        
        if 'TOTALACRES' in filtered_df.columns:
            # Create size categories for better visualization
            filtered_df['SIZE_CATEGORY'] = pd.cut(
                filtered_df['TOTALACRES'],
                bins=[0, 10, 100, 1000, 10000, float('inf')],
                labels=['Small (<10)', 'Medium (10-100)', 'Large (100-1000)', 'Very Large (1000-10000)', 'Mega (>10000)']
            )
            
            # Extract coordinates
            filtered_df['LAT'] = filtered_df.geometry.y
            filtered_df['LON'] = filtered_df.geometry.x
            
            fig = px.scatter_map(
                filtered_df,
                lat='LAT',
                lon='LON',
                color='SIZE_CATEGORY',
                size='TOTALACRES',
                hover_data=['FIREYEAR', 'TOTALACRES', 'STATCAUSE'] if all(col in filtered_df.columns for col in ['FIREYEAR', 'STATCAUSE']) else ['TOTALACRES'],
                title=f"Wildfire Locations ({len(filtered_df):,} fires)",
                map_style="open-street-map",
                zoom=3
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Geographic Distribution")
        
        if 'STATENAME' in filtered_df.columns:
            state_fires = filtered_df['STATENAME'].value_counts().head(15)
            
            fig = px.bar(
                x=state_fires.values,
                y=state_fires.index,
                orientation='h',
                title="Top 15 States by Fire Count",
                labels={'x': 'Number of Fires', 'y': 'State'}
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    # Additional spatial insights
    st.markdown("### 🔍 Spatial Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("### 📍 **Geographic Coverage**")
        if 'STATENAME' in filtered_df.columns:
            states_covered = filtered_df['STATENAME'].nunique()
            st.write(f"• **States with fires:** {states_covered}")
            st.write(f"• **Most affected state:** {filtered_df['STATENAME'].value_counts().index[0]}")
            st.write(f"• **Geographic spread:** Nationwide coverage")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("### 🎯 **Spatial Patterns**")
        if 'TOTALACRES' in filtered_df.columns:
            avg_size = filtered_df['TOTALACRES'].mean()
            largest_fire = filtered_df['TOTALACRES'].max()
            st.write(f"• **Average fire size:** {avg_size:.1f} acres")
            st.write(f"• **Largest fire in sample:** {largest_fire:,.0f} acres")
            st.write(f"• **Spatial clustering:** Visible in map")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Load data
    gdf = load_wildfire_data()
    
    if gdf is None:
        st.error("Failed to load data. Please check your S3 configuration.")
        return
    
    # Clean and prepare data
    df = clean_and_prepare_data(gdf)
    
    if df is None:
        st.error("Failed to process data.")
        return
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Choose Analysis Section",
        ["Advanced Overview", "Advanced Causes Analysis", "Advanced Spatial Analysis"]
    )
    
    # Display selected page
    if page == "Advanced Overview":
        show_advanced_overview(df)
    elif page == "Advanced Causes Analysis":
        show_advanced_causes_analysis(df)
    elif page == "Advanced Spatial Analysis":
        show_advanced_spatial_analysis(df)

if __name__ == "__main__":
    main() 