import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Solar Energy Dashboard",
    page_icon="🌞",
    layout="wide"
)

# Title and description
st.title("🌞 Solar Energy Analysis Dashboard")
st.markdown("**Interactive visualization of solar potential across Benin, Sierra Leone, and Togo**")
st.markdown("---")

# Sidebar for controls
st.sidebar.header("Dashboard Controls")

# Country selection
countries = ["Benin", "Sierra Leone", "Togo"]
selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare:",
    countries,
    default=["Benin", "Sierra Leone"]
)

# Metric selection
metric = st.sidebar.selectbox(
    "Select Solar Metric:",
    ["GHI", "DNI", "DHI", "Tamb", "RH", "WS"]
)

# Date range (simplified)
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Select multiple countries for comparison")

# Load data function
@st.cache_data
def load_data(country):
    try:
        df = pd.read_csv(f"data/{country.lower().replace(' ', '_')}_clean.csv")
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except:
        return None

# Main dashboard content
if not selected_countries:
    st.warning("Please select at least one country from the sidebar.")
else:
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Solar Metrics", "🌡️ Weather Correlation", "📈 Country Comparison"])
    
    with tab1:
        st.header("Solar Radiation Analysis")
        
        # Display data for each selected country
        for country in selected_countries:
            df = load_data(country)
            if df is not None:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        f"Average {metric} - {country}",
                        f"{df[metric].mean():.1f}",
                        f"Max: {df[metric].max():.1f}"
                    )
                
                with col2:
                    st.metric(
                        f"Standard Deviation - {country}",
                        f"{df[metric].std():.1f}"
                    )
                
                with col3:
                    st.metric(
                        f"Data Quality - {country}",
                        f"{(1 - df[metric].isna().sum() / len(df)) * 100:.1f}%",
                        "Complete"
                    )
        
        # Time series chart
        st.subheader(f"{metric} Over Time")
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for country in selected_countries:
            df = load_data(country)
            if df is not None:
                # Sample data for performance (first 1000 points)
                sample_df = df.head(1000)
                ax.plot(sample_df['Timestamp'], sample_df[metric], label=country, linewidth=1)
        
        ax.set_xlabel("Timestamp")
        ax.set_ylabel(f"{metric} Value")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with tab2:
        st.header("Weather Correlations")
        
        if len(selected_countries) > 0:
            country = selected_countries[0]  # Show correlation for first selected country
            df = load_data(country)
            
            if df is not None:
                # Correlation heatmap
                corr_cols = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS', 'BP']
                corr_data = df[corr_cols].corr()
                
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, ax=ax)
                ax.set_title(f"Correlation Matrix - {country}")
                st.pyplot(fig)
                
                # Scatter plot
                st.subheader(f"GHI vs Temperature - {country}")
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.scatter(df['Tamb'], df['GHI'], alpha=0.5, s=1)
                ax.set_xlabel("Temperature (°C)")
                ax.set_ylabel("GHI (W/m²)")
                ax.set_title(f"GHI vs Temperature Correlation: {df['GHI'].corr(df['Tamb']):.3f}")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
    
    with tab3:
        st.header("Cross-Country Comparison")
        
        if len(selected_countries) >= 2:
            # Boxplot comparison
            st.subheader(f"{metric} Distribution Comparison")
            fig, ax = plt.subplots(figsize=(10, 6))
            
            box_data = []
            labels = []
            for country in selected_countries:
                df = load_data(country)
                if df is not None:
                    box_data.append(df[metric].dropna())
                    labels.append(country)
            
            ax.boxplot(box_data, labels=labels, patch_artist=True)
            ax.set_ylabel(f"{metric} Value")
            ax.set_title(f"{metric} Distribution Across Selected Countries")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # Summary table
            st.subheader("Statistical Summary")
            summary_data = []
            for country in selected_countries:
                df = load_data(country)
                if df is not None:
                    summary_data.append({
                        'Country': country,
                        'Mean': df[metric].mean(),
                        'Median': df[metric].median(),
                        'Std Dev': df[metric].std(),
                        'Max': df[metric].max(),
                        'Min': df[metric].min()
                    })
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df.style.format({
                'Mean': '{:.2f}',
                'Median': '{:.2f}',
                'Std Dev': '{:.2f}',
                'Max': '{:.2f}',
                'Min': '{:.2f}'
            }))

# Footer
st.markdown("---")
st.markdown("**🌍 Solar Energy Analysis** | *10 Academy Week 0 Challenge*")
st.markdown("*Data Source: Solar Radiation Measurement Data*")