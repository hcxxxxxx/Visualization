import streamlit as st
import pandas as pd
import json
from charts import (
    chart_01,
    chart_02,
    chart_03,
    chart_04,
    chart_05,
    chart_06,
    chart_07,
    chart_08,
    chart_09,
    chart_10,
    chart_11
)

# 设置页面配置
st.set_page_config(layout="wide", page_title="Github Top 200 用户数据分析")

# 设置页面背景颜色
page_bg_color = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #222222;
}

[data-testid="stHeader"] {
    background-color: #333333;
}

[data-testid="stToolbar"] {
    right: 2rem;
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

pcolor = 'rgba(255,255,255,0.1)'
title_font = dict(color='white', size=20, family='Arial')
tick_font = dict(color='white', size=16, family='Arial')


# 读取数据
@st.cache_data
def load_data():
    with open('person_data_top200.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    # 处理 followers 数据
    def convert_followers(value):
        if isinstance(value, str):
            if 'k' in value.lower():
                return float(value.lower().replace('k', '')) * 1000
            elif 'm' in value.lower():
                return float(value.lower().replace('m', '')) * 1000000
        return float(value)
    
    df['followers_count'] = df['followers'].apply(convert_followers)
    
    # 处理日期
    df['join_date'] = pd.to_datetime(df['join_date'])
    df['join_year'] = df['join_date'].dt.year
    
    # 创建地理位置映射字典
    location_coords = {
        # 美国城市和地区
        'United States': (37.0902, -95.7129),
        'San Francisco': (37.7749, -122.4194),
        'New York': (40.7128, -74.0060),
        'Portland': (45.5155, -122.6789),
        'Seattle': (47.6062, -122.3321),
        'California': (36.7783, -119.4179),
        'Mountain View': (37.3861, -122.0839),
        'Pittsburgh': (40.4406, -79.9959),
        'Salt Lake City': (40.7608, -111.8910),
        'Little Rock': (34.7465, -92.2896),
        'Austin': (30.2672, -97.7431),
        'Cambridge': (42.3736, -71.1097),
        'Virginia': (37.4316, -78.6569),
        'Washington': (47.7511, -120.7401),
        'Phoenix': (33.4484, -112.0740),
        'Anaheim': (33.8366, -117.9143),
        'Palo Alto': (37.4419, -122.1430),
        'Southern Oregon': (42.8865, -122.8156),
        'Texas': (31.9686, -99.9018),

        # 中国城市和地区
        'China': (35.8617, 104.1954),
        'Beijing': (39.9042, 116.4074),
        'Shanghai': (31.2304, 121.4737),
        'Hangzhou': (30.2741, 120.1551),
        'Wuxi': (31.4916, 120.3119),
        'Chongqing': (29.4316, 106.9123),
        'Hefei': (31.8206, 117.2272),

        # 欧洲城市和国家
        'London': (51.5074, -0.1278),
        'Germany': (51.1657, 10.4515),
        'Berlin': (52.5200, 13.4050),
        'Austria': (47.5162, 14.5501),
        'Portugal': (39.3999, -8.2245),
        'Barcelona': (41.3851, 2.1734),
        'Paris': (48.8566, 2.3522),

        # 亚洲其他地区
        'Singapore': (1.3521, 103.8198),
        'Japan': (36.2048, 138.2529),
        'India': (20.5937, 78.9629),
        'Bangalore': (12.9716, 77.5946),
        'Taiwan': (23.6978, 120.9605),
        'Dubai': (25.2048, 55.2708),
        'Korea': (35.9078, 127.7669),

        # 其他国家和地区
        'Brazil': (-14.2350, -51.9253),
        'Rio de Janeiro': (-22.9068, -43.1729),
        'Santa Catarina': (-27.2423, -50.2189),
        'São Paulo': (-23.5505, -46.6333),
        'Croatia': (45.1000, 15.2000),
        'Australia': (-25.2744, 133.7751),
        'New Zealand': (-40.9006, 174.8860),
        'Canada': (56.1304, -106.3468),
        'Ontario': (51.2538, -85.3232),
        'Hamilton': (43.2557, -79.8711),
        'Kenya': (0.0236, 37.9062),
        'Nairobi': (-1.2921, 36.8219),
        'Cyprus': (35.1264, 33.4299),
        'Israel': (31.0461, 34.8516),
        'Scotland': (56.4907, -4.2026),
        'Ireland': (53.1424, -7.6921),
        'Netherlands': (52.1326, 5.2913),
        'Amsterdam': (52.3676, 4.9041),
        'Italy': (41.8719, 12.5674),
        'Catania': (37.5079, 15.0830),
        'Bath': (51.3758, -2.3599),
        'Lisbon': (38.7223, -9.1393),
        'Oslo': (59.9139, 10.7522),
        'Stockholm': (59.3293, 18.0686),
        'Helsinki': (60.1699, 24.9384),
        'Copenhagen': (55.6761, 12.5683),
        'Brussels': (50.8503, 4.3517),
        'Vienna': (48.2082, 16.3738),
        'Prague': (50.0755, 14.4378),
        'Warsaw': (52.2297, 21.0122),
        'Budapest': (47.4979, 19.0402),
        'Buenos Aires': (-34.6037, -58.3816),
        'Mexico City': (19.4326, -99.1332),
        'Santiago': (-33.4489, -70.6693)
    }
    
    def get_coordinates(location):
        if pd.isna(location):
            return None, None
        
        # 遍历位置映射字典查找匹配
        for key, coords in location_coords.items():
            if key.lower() in str(location).lower():
                return coords
        
        return None, None
    
    # 获取经纬度
    df['latitude'], df['longitude'] = zip(*df['loc'].apply(get_coordinates))
    
    # 创建国家映射字典
    country_mapping = {
        'United States': ['USA', 'United States', 'California', 'San Francisco', 'New York', 'Portland', 
                         'Seattle', 'Mountain View', 'Pittsburgh', 'Salt Lake City', 'Little Rock', 
                         'Austin', 'Cambridge', 'Virginia', 'Washington', 'Phoenix', 'Anaheim', 
                         'Palo Alto', 'Southern Oregon', 'Texas'],
        'China': ['China', 'Beijing', 'Shanghai', 'Hangzhou', 'Wuxi', 'Chongqing', 'Hefei'],
        'UK': ['United Kingdom', 'London', 'Bath', 'Scotland'],
        'Germany': ['Germany', 'Berlin'],
        'Brazil': ['Brazil', 'Rio de Janeiro', 'Santa Catarina', 'São Paulo'],
        'India': ['India', 'Bangalore'],
        'Japan': ['Japan'],
        'Singapore': ['Singapore'],
        'Canada': ['Canada', 'Ontario', 'Hamilton'],
        'Netherlands': ['Netherlands', 'Amsterdam'],
        'Portugal': ['Portugal', 'Lisbon'],
        'Australia': ['Australia'],
        'Israel': ['Israel'],
        'Taiwan': ['Taiwan'],
        'Austria': ['Austria', 'Vienna'],
        'Croatia': ['Croatia'],
        'Kenya': ['Kenya', 'Nairobi'],
        'Cyprus': ['Cyprus'],
        'Italy': ['Italy', 'Catania']
    }

    def get_country(location):
        if pd.isna(location):
            return 'Unknown'
        location = str(location).lower()
        for country, cities in country_mapping.items():
            if any(city.lower() in location for city in cities):
                return country
        return 'Other'
    
    # 获取国家信息
    df['country'] = df['loc'].apply(get_country)
    
    return df

df = load_data()

# 标题
# st.title("Github Top 200 用户数据分析")
custom_title = """
<div style="text-align: center; color: white; font-size: 60px; font-weight: bold;">
    Github Top 200 用户数据分析
</div>
"""
st.markdown(custom_title, unsafe_allow_html=True)

chart_01.chart_01(df, pcolor, title_font, tick_font)
    

# 创建两列布局
col1, col2 = st.columns(2)
with col1:
    chart_02.chart_02(df, pcolor, title_font, tick_font)
with col2:
    chart_03.chart_03(df, pcolor, title_font, tick_font)
    #chart_04.chart_04(df, pcolor, title_font, tick_font)
    chart_05.chart_05(df, pcolor, title_font, tick_font)


col5, col6 = st.columns(2)
with col5:
    chart_06.chart_06(df, pcolor, title_font, tick_font)
with col6:
    chart_07.chart_07(df, pcolor, title_font, tick_font)


col7, col8 = st.columns(2)
with col7:
    chart_08.chart_08(df, pcolor, title_font, tick_font)
with col8:
    chart_09.chart_09(df, pcolor, title_font, tick_font)


col9, col10 = st.columns(2)
with col9:
    chart_10.chart_10(df, pcolor, title_font, tick_font)
with col10:
    chart_11.chart_11(df, pcolor, title_font, tick_font)


# legend: 图例
# grid: 网格
# title: 标题
# xaxis: x轴
# yaxis: y轴
# paper_bgcolor: 背景颜色
# plot_bgcolor: 图表背景颜色
# xaxis_title: x轴标题
# yaxis_title: y轴标题
# xaxis_title: x轴标题
# yaxis_title: y轴标题
