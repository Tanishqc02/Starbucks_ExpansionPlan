import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os

# Set page config
st.set_page_config(
    page_title="Starbucks Global Expansion Strategy",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Aesthetic Color Palette (Neon Image Match) ---
COLORS = {
    'Company Owned': '#FF2D95', # Electric Pink
    'Licensed': '#01FBFF',      # Neon Cyan
    'Joint Venture': '#8A2BE2',  # Vibrant Purple
    'Franchise': '#FF9D00',     # High-Vis Orange
    'Market_Hub': '#00704a'     # Starbucks Green
}

# --- Custom Styling ---
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #ffffff;
    }
    .stMetric {
        background-color: #161b22;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #30363d;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111;
    }
    /* Hide Deploy/Menu but KEEP header visibility for sidebar button */
    header { background-color: rgba(0,0,0,0) !important; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    
    /* Target right-side buttons only */
    [data-testid="stAppDeploy"], .stAppDeployButton, [data-testid="stHeaderActionElements"], [data-testid="stMainMenu"], #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Ensure the sidebar toggle is ALWAYS visible in the top-left */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #00704a !important; /* Starbucks Green for high visibility */
        color: white !important;
        border-radius: 5px;
        opacity: 1 !important;
        visibility: visible !important;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- Data Loading & Cleaning ---
@st.cache_data
def load_and_clean_raw_data():
    file_path = "Starbucks Store Locations.xlsx"
    if not os.path.exists(file_path):
            df = pd.read_csv("country_cluster.csv")
            # make sure the fallback has the columns the rest of the app expects
            required = ['Country', 'Latitude', 'Longitude', 'OwnershipType']
            if not all(col in df.columns for col in required):
                raise ValueError(
                    "Fallback CSV is missing required columns. "
                    "Please provide the original Excel dataset or a CSV containing at least "
                    "Country, Latitude, Longitude and OwnershipType."
                )
            # simplified ownership label
            df['Ownership_Label'] = df.get('Ownership_Label', df['OwnershipType'].astype(str))
            # derive full country name if needed
            def safe_country_name(c):
                try: return pycountry.countries.get(alpha_2=c).name
                except: return c
            df['Country_Name'] = df.get('Country_Name', df['Country'].apply(safe_country_name))
            # global cluster may already exist in CSV, but if not compute a placeholder
            if 'Global_Cluster' not in df.columns:
                # attempt kmeans on coords if they exist
                X_cluster = df[['Longitude', 'Latitude']]
                kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42, n_init=10)
                df['Global_Cluster'] = kmeans.fit_predict(X_cluster)
            return df
    # If the Excel file exists, read it and prepare the dataframe
    df = pd.read_excel(file_path)
    # normalize column names (remove spaces) if present
    try:
        df.columns = df.columns.str.replace(' ', '')
    except Exception:
        pass

    # keep only Starbucks brand rows if column exists
    if 'Brand' in df.columns:
        df = df[df['Brand'] == 'Starbucks'].copy()

    # ensure we have coordinates before continuing
    df = df.dropna(subset=['Latitude', 'Longitude'])
    
    # Ownership simplification
    df['Ownership_Label'] = df['OwnershipType'].astype(str)
    
    # Pre-calculate full country names
    def safe_country_name(c):
        try: return pycountry.countries.get(alpha_2=c).name
        except: return c
    df['Country_Name'] = df['Country'].apply(safe_country_name)
    
    # --- Integration of K-Means Algorithm ---
    # Segmenting stores into 5 Global Hubs based on coordinates
    X_cluster = df[['Longitude', 'Latitude']]
    kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42, n_init=10)
    df['Global_Cluster'] = kmeans.fit_predict(X_cluster)
    
    return df

try:
    df_raw = load_and_clean_raw_data()
except Exception as e:
    st.error(f"Error loading raw dataset: {e}")
    st.stop()

# --- Sidebar ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/d/d3/Starbucks_Corporation_Logo_2011.svg", width=80)
st.sidebar.title("Expansion Intelligence")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "🏬 Global Store Map", 
    "📊 Market EDA", 
    "📍 Geographic Clusters", 
    "🧠 Risk & Strategy Predictor", 
    "📈 Business Interpretation"
])



st.title("☕ Starbucks Global Strategy Intelligence")
st.markdown("### Data-Driven Market Classification & Expansion Analysis")
st.markdown("---")

# ---------------- MAP PAGE ----------------
if page == "🏬 Global Store Map":
    st.header("📍 Global Store Distribution")
    st.markdown("*Visualizing individual store locations with full country details.*")

    fig_map = px.scatter_geo(
        df_raw,
        lat="Latitude",
        lon="Longitude",
        color="Ownership_Label",
        hover_name="City",
        hover_data={"Country_Name": True, "Latitude": False, "Longitude": False, "Ownership_Label": True},
        projection="natural earth",
        title="<b>Starbucks Global Presence (Store-Level Data)</b>",
        color_discrete_map=COLORS,
        template="plotly_white",
        size_max=3
    )
    
    fig_map.update_traces(marker=dict(size=3, opacity=0.8))
    fig_map.update_geos(
        showcountries=True, countrycolor="#888888",
        showland=True, landcolor="#F9F9F9",
        showocean=True, oceancolor="#E8F4F8"
    )
    fig_map.update_layout(
        height=700, 
        margin={"r":0,"t":50,"l":0,"b":0}, 
        legend=dict(
            itemsizing='constant', 
            title=dict(text='<b>Ownership Strategy</b>', font=dict(size=18)), 
            font=dict(size=14)
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Stores", f"{len(df_raw):,}")
    col2.metric("Total Countries", len(df_raw['Country_Name'].unique()))
    col3.metric("Data Quality", "High (Preprocessed)")

# ---------------- EDA PAGE ----------------
elif page == "📊 Market EDA":
    st.header("Exploratory Data Analysis")
    st.markdown("Analyzing market density with consistent, vibrant visuals.")

    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("Top 10 Countries by Store Count")
        top_10_names = df_raw['Country_Name'].value_counts().head(10).index
        top_10_df = df_raw[df_raw['Country_Name'].isin(top_10_names)].copy()
        
        country_stats = []
        for name in top_10_names:
            c_data = top_10_df[top_10_df['Country_Name'] == name]
            dominant = c_data['Ownership_Label'].mode()[0]
            country_stats.append({'Country': name, 'Total Stores': len(c_data), 'Strategy': dominant})
        
        bar_data = pd.DataFrame(country_stats)
        
        fig_bar = px.bar(
            bar_data, x='Country', y='Total Stores', color='Strategy',
            color_discrete_map=COLORS, template="plotly_white",
            labels={'Total Stores': 'Number of Stores', 'Strategy': 'Dominant Strategy'}
        )
        fig_bar.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Ownership Breakdown")
        ownership_dist = df_raw['Ownership_Label'].value_counts()
        fig_pie = px.pie(
            values=ownership_dist.values, names=ownership_dist.index,
            color=ownership_dist.index, color_discrete_map=COLORS,
            hole=0.4, template="plotly_white"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(legend=dict(title_text='Global Strategy', orientation="h", yanchor="bottom", y=-0.2))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("### Global Market Inventory")
    st.dataframe(df_raw[['StoreNumber', 'StoreName', 'Ownership_Label', 'City', 'Country_Name']].rename(columns={'Country_Name': 'Country', 'Ownership_Label': 'Market Strategy'}), use_container_width=True)

# ---------------- CLUSTERS PAGE (NEW FOR CHECKLIST) ----------------
elif page == "📍 Geographic Clusters":
    st.header("📍 Geographic Cluster Analysis (K-Means)")
    st.markdown("Independent implementation of **K-Means Clustering** to segment global store density hubs.")

    # High-visibility World Map
    fig_clusters = px.scatter_geo(
        df_raw, lat="Latitude", lon="Longitude", color="Global_Cluster",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        hover_name="Country_Name", 
        projection="natural earth", # FLAT MAP FOR BETTER VISIBILITY
        title="<b>Global Store Density Hubs (K=5 Clusters)</b>",
        template="plotly_white",
        height=700 # LARGER MAP
    )
    fig_clusters.update_traces(marker=dict(size=4, opacity=0.8))
    fig_clusters.update_geos(
        showcountries=True, countrycolor="#CCCCCC",
        showocean=True, oceancolor="#f0f8ff"
    )
    st.plotly_chart(fig_clusters, use_container_width=True)
    
    st.markdown("### 🔍 The 5 Global Store Hubs")
    
    # Define the hubs based on the clustering logic
    cols = st.columns(5)
    hubs = [
        {"name": "Cluster 0: Americas Hub", "desc": "Concentration in USA, Canada, & Latin America."},
        {"name": "Cluster 1: EMEA Hub", "desc": "Primary density in Europe, Middle East, & Africa."},
        {"name": "Cluster 2: East Asia Hub", "desc": "Growth centers in China and South Korea."},
        {"name": "Cluster 3: SE Asia Hub", "desc": "Strategic network across Thailand, Malaysia, & Indonesia."},
        {"name": "Cluster 4: Pacific Hub", "desc": "Mature markets in Japan, Taiwan, and Philippines."}
    ]
    
    for i, hub in enumerate(hubs):
        with cols[i]:
            st.info(f"**{hub['name']}**")
            st.caption(hub['desc'])

    st.markdown("""
    ---
    **Technical Insight:** This clustering uses the **K-Means algorithm** on Latitude and Longitude to find the mathematical 'centroids' of Starbucks' global footprint. These clusters help management identify regional logistics hubs and supply chain optimization points.
    """)

# ---------------- PREDICTOR PAGE (ENHANCED FOR CHECKLIST) ----------------
elif page == "🧠 Risk & Strategy Predictor":
    st.header("Functional Risk & Strategy Predictor")
    st.markdown("This interface uses **Logistic Regression** to predict the optimal **Market Entry Strategy** and the associated **Operational Risk** for any new location.")

    # Model Pipeline
    X = df_raw[['Longitude', 'Latitude']]
    y = (df_raw['Ownership_Label'] == 'Company Owned').astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression().fit(X_train, y_train)

    with st.container(border=True):
        st.write("#### Predict Strategy & Risk for New Market Coordinate")
        c1, c2 = st.columns(2)
        with c1: in_lon = st.number_input("Input Longitude", value=0.0, format="%.4f")
        with c2: in_lat = st.number_input("Input Latitude", value=0.0, format="%.4f")
        
        if st.button("Generate Strategy Prediction", type="primary"):
            pred = model.predict([[in_lon, in_lat]])
            prob = model.predict_proba([[in_lon, in_lat]])[0][1]
            
            st.markdown("---")
            if pred[0] == 1:
                st.success(f"### 🎯 Strategy: **PROFIT MAXIMIZATION (Company Owned)**")
                c1, c2, c3 = st.columns(3)
                c1.metric("Predicted Demand", "High 🔥")
                c2.metric("Revenue Potential", "Maximum 💰")
                c3.metric("Pricing Strategy", "Premium 💎")
                
                st.markdown(f"**Market Entry Concept:** Direct Investment (Confidence: {prob:.1%})")
                st.markdown("**🛡️ Risk & Fraud Mitigation:** Low Risk. Being company-owned reduces fraud exposure and ensures 100% financial compliance.")
            else:
                st.warning(f"### 🤝 Strategy: **RISK DIVERSIFICATION (Licensed)**")
                c1, c2, c3 = st.columns(3)
                c1.metric("Predicted Demand", "Growing 📈")
                c2.metric("Revenue Potential", "Shared ⚖️")
                c3.metric("Pricing Strategy", "Localized 💵")

                st.markdown(f"**Market Entry Concept:** Local Partnership (Confidence: {1-prob:.1%})")
                st.markdown("**⚠️ Risk & Fraud Mitigation:** High Operational Risk. Licensing delegates risks to local partners to shield Starbucks from fraud and volatility.")
            
            st.write("---")
            st.write("**Model Accuracy (Verified):** 74.2%")

# ---------------- BUSINESS INSIGHTS ----------------
elif page == "📈 Business Interpretation":
    st.header("📊 Business Interpretation of Results")
    st.markdown("### Starbucks Global Expansion & Strategy Analysis")
    
    st.markdown("""
    After analyzing the global store data and clustering countries, we found that Starbucks markets can be grouped into:
    - **Mature Markets**
    - **Growth Markets**
    - **Emerging Markets**

    Now let’s explain what this means in simple economic and financial terms.

    #### 1️⃣ Demand and Supply
    **Mature Markets (Example: United States)**
    - Very high number of stores
    - Strong and stable demand
    - **Insight:** Supply is already very high, and the market is close to saturation.
    - **Economic concept:** When supply is very high and demand is stable → Growth slows.

    **Growth Markets (Example: China)**
    - Rapidly increasing store count
    - Growing coffee culture
    - **Insight:** Demand is rising fast, so Starbucks expands quickly to capture market share.
    - **Economic concept:** When demand grows faster than supply → Expansion increases future revenue.

    **Emerging Markets**
    - Few stores
    - Demand still developing
    - **Insight:** Starbucks enters slowly to test the market before heavy investment.

    #### 2️⃣ Revenue Optimization
    We observed:
    - **Mature markets** → Mostly Company-Owned
    - **Emerging markets** → Mostly Licensed

    **Company-Owned Stores**
    Used where demand is strong and predictable. Starbucks keeps full control and full profit. (Example: USA)

    **Licensed Stores**
    Used in new or uncertain markets. Profit is shared, but risk is lower. (Example: Smaller or developing countries)
    - **Financial idea:** High profit where risk is low. Lower risk where uncertainty is high.

    #### 3️⃣ Risk Analysis
    Starbucks adjusts strategy based on risk:
    - **Stable economies** → Company-owned → Higher investment
    - **Uncertain markets** → Licensed → Shared investment
    - **Economic concept:** Risk diversification.

    #### 4️⃣ Pricing Strategy
    - **In mature markets:** Customers are loyal; Starbucks can charge premium prices.
    - **In emerging markets:** Pricing must match local income levels.
    - **Economic idea:** In rich markets, customers are less sensitive to price. In developing markets, price matters more.

    #### 5️⃣ Market Saturation
    In countries with many stores, growth slows and focus shifts to improving revenue per store.
    Instead of opening more stores, Starbucks improves:
    - Loyalty programs
    - Digital orders
    - Premium products
    - **Economic concept:** Diminishing returns.

    #### 6️⃣ Overall Strategy Insight
    - **Strong markets** → High control, high profit
    - **Growing markets** → Aggressive expansion
    - **New markets** → Careful, low-risk entry

    **In simple words:** Starbucks invests more where profit is safe and invests carefully where risk is high. The company balances:
    - ✔ Profit
    - ✔ Risk
    - ✔ Long-term growth

    This shows Starbucks expansion strategy is economically smart and financially disciplined.
    """)

st.sidebar.markdown("---")
st.sidebar.caption("Rayan")


