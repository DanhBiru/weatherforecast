import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import json

# --- Chỉnh chế độ hiển thị ---
st.set_page_config(layout="wide")
# --- Đọc dữ liệu từ file Excel ---
@st.cache_data

def load_data():
    df = pd.read_excel("forecast (1).xlsx", engine="openpyxl")
    df["time"] = pd.to_datetime(df["time"])
    return df

df = load_data()

# --- UI

# st.title("Biểu đồ chất lượng không khí theo tỉnh thành")
# st.write("Chọn một tỉnh/thành để xem biểu đồ PM2.5 và AQI trong 6 ngày")
# st.write(f"biểu đồ PM2.5 và AQI trong 6 ngày tại {selected_province}")

# some useful constants 
OPACITY = 0.9
OUTLINE_WIDTH = 0
LINE_WIDTH = 3
MARGIN = 5

PM25_SCALE = [12.0, 35.5, 55.5, 150.5, 250.5, 350.5]
AQI_SCALE = [50, 100, 150, 200, 300, 400]
SCALE_EN = ["Good", "Moderate", "Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy", "Hazardous"]
# SCALE_VI = ["Tốt", "Trung bình", "Không tốt cho nhóm người nhạy cảm", "Không lành mạnh", "Rất không lành mạnh", "Nguy hiểm"]
SCALE_PALETTE = ["#9cd84e", "#f9cf39", "#f89049", "#f89049", "#9f70b5", "#a06a7b"]

# --- Vẽ 2 biểu đồ
province_list = sorted(df["VARNAME_1"].unique())
selected_province = st.selectbox("Chọn tỉnh/thành:", province_list)
filtered_df = df[df["VARNAME_1"] == selected_province].sort_values("time")

from_date = min(filtered_df["time"])
to_date = max(filtered_df["time"]) #can be overwrite later if needed

fig1 = go.Figure()
fig2 = go.Figure()

# -- Biểu đồ PM2.5
fig1.add_trace(go.Scatter(
    x=filtered_df["time"], 
    y=filtered_df["PM25"],
    mode="lines+markers", 
    name="PM2.5",
    line=dict(width=LINE_WIDTH)
))

pm_min = filtered_df["PM25"].min()
pm_max = filtered_df["PM25"].max()

low_pm = max(0, pm_min - MARGIN)
high_pm = pm_max + MARGIN 

shapes_PM25=[
    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(0, low_pm), y1=min(PM25_SCALE[0], high_pm),
        fillcolor=SCALE_PALETTE[0], opacity=OPACITY, line_width=OUTLINE_WIDTH, 
        layer="below") if low_pm < PM25_SCALE[0] else None,

    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(PM25_SCALE[0], low_pm), y1=min(PM25_SCALE[1], high_pm),
        fillcolor=SCALE_PALETTE[1], opacity=OPACITY, line_width=OUTLINE_WIDTH, 
        layer="below") if high_pm >= PM25_SCALE[0] and low_pm < PM25_SCALE[1] else None,

    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(PM25_SCALE[1], low_pm), y1=min(PM25_SCALE[2], high_pm),
        fillcolor=SCALE_PALETTE[2], opacity=OPACITY, line_width=OUTLINE_WIDTH,
        layer="below") if high_pm >= PM25_SCALE[1] and low_pm < PM25_SCALE[2] else None,

    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(PM25_SCALE[2], low_pm), y1=min(PM25_SCALE[3], high_pm),
        fillcolor=SCALE_PALETTE[3], opacity=OPACITY, line_width=OUTLINE_WIDTH,
        layer="below") if high_pm >= PM25_SCALE[2] and low_pm < PM25_SCALE[3] else None,
        
    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(PM25_SCALE[3], low_pm), y1=min(PM25_SCALE[4], high_pm),
        fillcolor=SCALE_PALETTE[4], opacity=OPACITY, line_width=OUTLINE_WIDTH,
        layer="below") if high_pm >= PM25_SCALE[3] and low_pm < PM25_SCALE[4] else None,
]

shapes_PM25= [s for s in shapes_PM25 if s is not None]

fig1.update_layout(
    shapes=shapes_PM25,
    title=f"PM2.5 (28/6 - 6/7)",
    xaxis_title="Ngày",
    yaxis_title="PM2.5",
    # legend_title="Loại chỉ số",
    height=500
)

# -- Biểu đồ AQI
fig2.add_trace(go.Scatter(
    x=filtered_df["time"], y=filtered_df["AQI"],
    mode="lines+markers", name="AQI", line=dict(width=LINE_WIDTH)
))

aqi_min = filtered_df["AQI"].min()
aqi_max = filtered_df["AQI"].max()

low_aqi = max(0, aqi_min - MARGIN)
high_aqi = aqi_max + MARGIN 

shapes_AQI=[
    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(0, low_aqi), y1=min(AQI_SCALE[0], high_aqi),
        fillcolor=SCALE_PALETTE[0], opacity=OPACITY, line_width=OUTLINE_WIDTH,
        layer="below") if low_aqi < AQI_SCALE[0] else None,

    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(AQI_SCALE[0], low_aqi), y1=min(AQI_SCALE[1], high_aqi),
        fillcolor=SCALE_PALETTE[1], opacity=OPACITY, line_width=OUTLINE_WIDTH,
        layer="below") if high_aqi >= AQI_SCALE[0] and low_aqi < AQI_SCALE[1] else None,

    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(AQI_SCALE[1], low_aqi), y1=min(AQI_SCALE[2], high_aqi),
        fillcolor=SCALE_PALETTE[2], opacity=OPACITY, line_width=OUTLINE_WIDTH,
        layer="below") if high_aqi >= AQI_SCALE[1] and low_aqi < AQI_SCALE[2] else None,

    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(AQI_SCALE[2], low_aqi), y1=min(AQI_SCALE[3], high_aqi),
        fillcolor=SCALE_PALETTE[4], opacity=OPACITY, line_width=OUTLINE_WIDTH,
        layer="below") if high_aqi >= AQI_SCALE[2] and low_aqi < AQI_SCALE[3] else None,
        
    dict(type="rect", xref="x", yref="y",
        x0=from_date, x1=to_date,
        y0=max(AQI_SCALE[3], low_aqi), y1=min(AQI_SCALE[4], high_aqi),
        fillcolor=SCALE_PALETTE[4], opacity=OPACITY, line_width=OUTLINE_WIDTH,
        layer="below") if high_aqi >= AQI_SCALE[3] and low_aqi < AQI_SCALE[4] else None,
]

shapes_AQI= [s for s in shapes_AQI if s is not None]

fig2.update_layout(
    shapes=shapes_AQI,
    title=f"AQI (28/6 - 6/7)",
    xaxis_title="Ngày",
    yaxis_title="AQI",
    # legend_title="Loại chỉ số",
    height=500
)

# --- Nhúng map ---
date_list = pd.date_range(start=from_date, end=to_date, freq='D').sort_values(ascending=False)
selected_date = st.selectbox("Ngày:", date_list, index=0)
index_list = ["AQI", "PM25"]
selected_index = st.selectbox("Loại chỉ số:", index_list, index=0)

df_selected_date = df[df['time'].dt.date == selected_date.date()]

with open("VNnew34.json") as f:
    geojson_data = json.load(f)

fig = px.choropleth_mapbox(
    df_selected_date,
    geojson=geojson_data,
    locations="VARNAME_1",  # Cột mã trong df để map với geojson
    featureidkey="properties.NAME_1",  # phải khớp với key trong geojson
    color=selected_index,       # Hoặc "AQI"
    color_continuous_scale="YlOrRd",
    range_color=(0, 150),
    mapbox_style="carto-positron",
    zoom=4.5,
    center={"lat": 16.5, "lon": 106},
    opacity=0.7,
)

# df_set = set(df["VARNAME_1"])
# # geo_set = set(f["properties"]["TinhThanh"] for f in geojson_data["features"])
# geo_set = set(f["properties"]["NAME_1"] for f in geojson_data["features"])
# print("🟢 Match:", df_set & geo_set)
# print("🔴 Không match:", geo_set - df_set)
# print("🔴 Không match:", df_set - geo_set)

fig.update_layout(
    coloraxis_colorbar=dict(
        title="PM2.5",
        thickness=10,        # thu nhỏ bề ngang
        len=0.5,             # thu nhỏ chiều cao
        x=0.95,              # dịch sang phải
        y=0.5,               # canh giữa theo chiều dọc
        xanchor='left'
    ),
    margin={"r": 10, "t": 10, "l": 10, "b": 10},
    geo=dict(
        fitbounds="locations",
        visible=False
    )
)

# --- Pages for embedding
page = st.query_params.get("page", "main")
if page == "map":
    st.set_page_config(layout="wide")
    st.title("Bản đồ chất lượng không khí")
    st.plotly_chart(fig, use_container_width=True)

elif page == "chart":
    st.title("Biểu đồ PM2.5")
    st.plotly_chart(fig1, use_container_width=True)

else:
    st.title("📊 Dự báo chất lượng không khí")
    st.markdown("Chọn nội dung muốn xem:")
    st.markdown("- [➡️ Xem bản đồ](?page=map)")
    st.markdown("- [📈 Xem biểu đồ](?page=chart)")

# --- Load UI

# with open("style.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# with st.container():
#     st.markdown('<div class="map-container">', unsafe_allow_html=True)
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown('</div>', unsafe_allow_html=True)

# with st.container():
#     st.markdown('<div class="overlay-box">', unsafe_allow_html=True)

#     selected_province = st.selectbox("Chọn tỉnh thành", sorted(df["VARNAME_1"].unique()))
#     df_filtered = df[df["VARNAME_1"] == selected_province]

#     fig_line = px.line(df_filtered, x="time", y=["PM25", "AQI"], markers=True)
#     st.plotly_chart(fig_line, use_container_width=True)

#     st.markdown('</div>', unsafe_allow_html=True)

# st.plotly_chart(fig1, use_container_width=True)
# st.plotly_chart(fig2, use_container_width=True)
# st.plotly_chart(fig, use_container_width=True)

#legend


# st.markdown(
#     """
#     <div class="legend" style='font-size:16px'>
#         <span class="legend_note-1">  </span> Good  
#         <span class="legend_note-2">  </span> Moderate  
#         <span class="legend_note-3">  </span> Unhealthy for Sensitive Group  
#         <span class="legend_note-4">  </span> Unhealthy  
#         <span class="legend_note-5">  </span> Very Unhealthy  
#         <span class="legend_note-6">  </span> Hazardous  
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# fig1.write_html("pm25_chart.html", include_plotlyjs='cdn')
# fig2.write_html("aqi_chart.html", include_plotlyjs='cdn')
# fig.write_html("map.html", include_plotlyjs='cdn')


# st.plotly_chart(fig, use_container_width=True)