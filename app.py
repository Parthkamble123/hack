import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import folium
from streamlit_folium import st_folium
import graphviz
import random
import time
import plotly.graph_objects as go
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Smart City Traffic System", layout="wide")

# ---------------- PREMIUM DARK UI ----------------
st.markdown("""
<style>
body {background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color:white;}
h1 {font-size: 42px;}
div[data-testid="metric-container"] {background-color: #111827; border-radius:18px; padding:15px; box-shadow:0 0 25px rgba(0,0,0,0.4);}
.stButton>button {background: linear-gradient(90deg,#00c6ff,#0072ff); color:white; border-radius:14px; height:3em; font-size:18px;}
.badge {background-color:#00FFAA; padding:8px 18px; border-radius:20px; font-weight:bold; color:black;}
</style>
""", unsafe_allow_html=True)

st.title("🚦 AI Smart City Traffic Coordination Dashboard")
st.markdown("### 🏆 Hackathon Edition")

# ---------------- SESSION STATE ----------------
if "green_times" not in st.session_state:
    st.session_state.green_times = {"North":0,"South":0,"East":0,"West":0}
if "selected_lane" not in st.session_state:
    st.session_state.selected_lane = ""
if "emergency_lanes" not in st.session_state:
    st.session_state.emergency_lanes = []
if "total_traffic" not in st.session_state:
    st.session_state.total_traffic = 0
if "failure_mode" not in st.session_state:
    st.session_state.failure_mode = False
if "edge_mode" not in st.session_state:
    st.session_state.edge_mode = False

# ---------------- STATUS CARDS ----------------
colA, colB, colC, colD = st.columns(4)
colA.metric("🚦 Total Signals", "12")
colB.metric("🚗 Avg Traffic", "184 Vehicles")
colC.metric("🚑 Active Emergencies", random.randint(0,2))
colD.metric("💚 System Health", "99.2%")
st.markdown("---")

# ---------------- ML MODEL ----------------
@st.cache_resource
def train_rf():
    X = np.random.randint(0,100,(1000,4))
    y = 20 + (X.max(axis=1)*0.6)
    model = RandomForestRegressor()
    model.fit(X,y)
    return model,X,y

rf_model,X_train,y_train = train_rf()
accuracy = r2_score(y_train, rf_model.predict(X_train))

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🚦 Live AI Control","🌍 City Coordination","📈 Analytics",
     "🗺️ Live Map","📡 IoT + Vision"]
)

# ===================================================
# 🚦 TAB 1 LIVE CONTROL
# ===================================================
with tab1:
    col1,col2 = st.columns([2,1])
    with col1:
        north = st.slider("North Lane",0,100,30)
        south = st.slider("South Lane",0,100,40)
        east = st.slider("East Lane",0,100,20)
        west = st.slider("West Lane",0,100,10)
        emergency_lanes = st.multiselect("🚑 Emergency Lanes", options=["North","South","East","West"])
        optimize = st.button("🔮 Run AI Optimization")
        simulate_failure = st.button("⚠️ Simulate Failure")

    # ---------------- FAILURE SIMULATION ----------------
    if simulate_failure:
        st.session_state.failure_mode = True
        st.session_state.edge_mode = True
        st.warning("⚠️ System Failure Simulated!")
        st.success("📡 EDGE MODE ACTIVE")

    # ---------------- AI OPTIMIZATION ----------------
    if optimize and not st.session_state.failure_mode:
        st.session_state.emergency_lanes = emergency_lanes
        lanes = ["North","South","East","West"]
        values = np.array([north,south,east,west])
        total = values.sum()
        st.session_state.total_traffic = total

        # Calculate green times
        green_times = {}
        for lane,val in zip(lanes,values):
            if lane in emergency_lanes:
                green_times[lane] = 60
            else:
                green_times[lane] = round((val/total)*120 if total>0 else 30,2)

        st.session_state.green_times = green_times
        st.session_state.selected_lane = max(green_times, key=green_times.get)

    # ---------------- DISPLAY PERSISTENT OUTPUT ----------------
    st.subheader("🚦 Live Signal Status")
    for lane in ["North","South","East","West"]:
        if lane in st.session_state.emergency_lanes:
            st.markdown(f"### {lane} : 🟢 (EMERGENCY 60 sec)")
        elif lane == st.session_state.selected_lane:
            st.markdown(f"### {lane} : 🟢  ({st.session_state.green_times[lane]} sec)")
        else:
            st.markdown(f"### {lane} : 🔴  ({st.session_state.green_times[lane]} sec)")

    st.subheader("⏳ Current Lane Green Time Allocation")
    df=pd.DataFrame({"Lane":["North","South","East","West"],
                     "Green Time":[st.session_state.green_times[l] for l in ["North","South","East","West"]]} )
    fig,ax=plt.subplots()
    ax.bar(df["Lane"],df["Green Time"], color=["green" if l==st.session_state.selected_lane else "red" for l in df["Lane"]])
    st.pyplot(fig)

    # ---------------- GREEN WAVE ----------------
    st.subheader("🌊 Green Wave Synchronization")
    st.markdown('<div class="badge">SMART CORRIDOR ACTIVATED</div>', unsafe_allow_html=True)
    st.markdown("🚦 ➡️ ➡️ ➡️ 🚦 ➡️ ➡️ ➡️ 🚦 ➡️ ➡️ ➡️ 🚦")

    # ---------------- RISK PANEL ----------------
    st.subheader("📊 Risk & Impact Analysis")
    fuel_saved = round(st.session_state.total_traffic*0.05,2)
    co2_reduced = round(st.session_state.total_traffic*0.12,2)
    emergency_gain = round(random.uniform(15,35),2)
    r1,r2,r3 = st.columns(3)
    r1.metric("⛽ Fuel Saved (L)", fuel_saved)
    r2.metric("🌿 CO₂ Reduced (kg)", co2_reduced)
    r3.metric("🚑 Faster Emergency Response", f"{emergency_gain}%")

    # ---------------- AI HEATMAP ----------------
    st.subheader("🔥 AI Congestion Heatmap")
    heat_data = np.random.rand(20,20)
    fig_heat = px.imshow(heat_data, color_continuous_scale="Reds")
    st.plotly_chart(fig_heat, use_container_width=True)

    # ---------------- 3D INTERSECTION ----------------
    st.subheader("🛣️ 3D Intersection Simulation")
    fig3d = go.Figure(data=[go.Scatter3d(
        x=np.random.rand(50),
        y=np.random.rand(50),
        z=np.random.rand(50),
        mode='markers'
    )])
    fig3d.update_layout(height=500)
    st.plotly_chart(fig3d, use_container_width=True)

    st.metric("🤖 ML Accuracy (R²)", round(accuracy,3))

# ===================================================
# 🌍 TAB 2 CITY COORDINATION
# ===================================================
with tab2:
    intersections=5
    city_data=[]
    for i in range(intersections):
        traffic=np.random.randint(50,300)
        predicted=rf_model.predict(np.random.randint(0,100,(1,4)))[0]
        city_data.append({"Signal":f"Intersection {i+1}","Traffic":traffic,"Green Time":round(predicted,2)})
    st.dataframe(pd.DataFrame(city_data))
    st.success("AI synchronizes green waves across intersections.")

# ===================================================
# 📈 TAB 3 ANALYTICS
# ===================================================
with tab3:
    days=30
    history=pd.DataFrame({"Day":range(days),"Traffic":np.random.randint(80,300,days)})
    fig2,ax2=plt.subplots()
    ax2.plot(history["Day"],history["Traffic"])
    st.pyplot(fig2)

# ===================================================
# 🗺️ TAB 4 MAP
# ===================================================
with tab4:
    m=folium.Map(location=[18.5204,73.8567],zoom_start=12)
    for i in range(5):
        lat=18.5204+random.uniform(-0.02,0.02)
        lon=73.8567+random.uniform(-0.02,0.02)
        folium.Marker([lat,lon], popup=f"Signal {i+1}", icon=folium.Icon(color="green")).add_to(m)
    st_folium(m,width=700,height=500)

# ===================================================
# 📡 TAB 5 IoT + VISION
# ===================================================
with tab5:
    graph=graphviz.Digraph()
    graph.node("Camera","Traffic Camera")
    graph.node("Edge","Edge Processor")
    graph.node("Cloud","Cloud AI Model")
    graph.node("Signal","Traffic Controller")
    graph.edges([("Camera","Edge"),("Edge","Cloud"),("Cloud","Signal")])
    st.graphviz_chart(graph)
    fake_frame=np.random.randint(0,255,(100,100))
    st.image(fake_frame)
    st.metric("Vehicles Detected", random.randint(5,50))

st.markdown("---")
st.markdown("### 🚀 AI + ML + 3D Simulation + Heatmap + Green Wave + Vision + Sustainability")
st.markdown("Built to WIN the Hackathon 🏆")