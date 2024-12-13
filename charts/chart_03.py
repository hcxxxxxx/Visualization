# 用户国家分布

import plotly.graph_objects as go
import streamlit as st
import pandas as pd
def chart_03(df, pcolor, title_font, tick_font):
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

    # 统计国家分布（排除 Other 和 Unknown）
    df['country'] = df['loc'].apply(get_country)
    country_counts = df['country'].value_counts()
    country_counts = country_counts[~country_counts.index.isin(['Other', 'Unknown'])]
    
    # 创建柱状图
    fig_countries = go.Figure()
    fig_countries.add_trace(go.Bar(
        x=country_counts.index,
        y=country_counts.values,
        marker_color='#3480b8'  # 使用与之前图表相调的颜色
    ))
    
    fig_countries.update_layout(
        # title='GitHub Top 200 用户国家分布',
        title=dict(
            text='GitHub Top 200 用户国家分布',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=title_font  # 设置标题字体大小
        ),
        xaxis_title=dict(text='国家', font=tick_font),
        yaxis_title=dict(text='用户数量', font=tick_font),
        xaxis_tickangle=-45,  # 倾斜x轴标签防叠
        xaxis_tickfont=tick_font,
        yaxis_tickfont=tick_font,
        height=400,  # 控制图表高度
        # margin=dict(t=50, b=50),  # 调整边距
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor,
        plot_bgcolor='rgba(17,17,17,0)',
        showlegend=False
    )
    
    # 添加网格线
    fig_countries.update_xaxes(showgrid=False)
    fig_countries.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)'
    )
    
    st.plotly_chart(fig_countries, use_container_width=True)