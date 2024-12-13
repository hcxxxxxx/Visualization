# 世界地图

import plotly.graph_objects as go
import streamlit as st

def chart_01(df, pcolor):
    fig = go.Figure()
    
    # 准备国家代码映射
    country_code_mapping = {
        'United States': 'USA',
        'China': 'CHN',
        'UK': 'GBR',
        'Germany': 'DEU',
        'Brazil': 'BRA',
        'India': 'IND',
        'Japan': 'JPN',
        'Singapore': 'SGP',
        'Canada': 'CAN',
        'Netherlands': 'NLD',
        'Portugal': 'PRT',
        'Australia': 'AUS',
        'Israel': 'ISR',
        'Austria': 'AUT',
        'Croatia': 'HRV',
        'Kenya': 'KEN',
        'Cyprus': 'CYP',
        'Italy': 'ITA'
    }

    # 获取国家统计数据（直接使用已有的 country 列）
    country_counts = df['country'].value_counts()
    country_counts = country_counts[~country_counts.index.isin(['Other', 'Unknown'])]

    # 准备热力图数据
    locations = []
    z_values = []
    for country, count in country_counts.items():
        if country in country_code_mapping:
            locations.append(country_code_mapping[country])
            z_values.append(count)
        
    # 添加基础地图层，使用热力图色
    fig.add_trace(go.Choropleth(
        locations=locations,
        z=z_values,
        locationmode='ISO-3',
        colorscale=[
            [0, 'rgba(122,103,240,0)'],
            [0.2, 'rgba(122,103,240,0.2)'],
            [0.4, 'rgba(122,103,240,0.4)'],
            [0.6, 'rgba(122,103,240,0.6)'],
            [0.8, 'rgba(122,103,240,0.8)'],
            [1, 'rgba(122,103,240,1)']
        ],
        colorbar=dict(
            title='用户数量',
            thickness=15,        # 减小宽度
            len=0.5,            # 减小长度
            x=0.9,                # 调整水平位置
            y=0.5,              # 调整垂直位置
            yanchor='middle',   # 垂直对齐方式
            titleside='right',  # 标题位置
            titlefont=dict(color='white', size=12, family='Arial'),
            tickfont=dict(color='white', size=12, family='Arial'),
            ticks='outside',     # 刻度线位置
            tickcolor='white',
        ),
        showscale=True,
        marker=dict(
            line=dict(
                color='rgb(180,180,180)',
                width=0.5
            )
        )
    ))
        
    # 添加用户位置标记
    valid_locations = df[df['loc'].notna()]
    fig.add_trace(go.Scattergeo(
        lon=valid_locations['longitude'],
        lat=valid_locations['latitude'],
        mode='markers',
        marker=dict(
            size=8,
            color='red',
            opacity=0.7,
            line=dict(
                color='rgb(40,40,40)',
                width=0.5
            )
        ),
        hovertext=valid_locations['name'] + '<br>' + valid_locations['loc'],
        name='Top200 Github用户'
    ))
        
    fig.update_layout(
        # title='Top 200 GitHub用户地理分布',
        title=dict(
            text='Top 200 GitHub用户地理分布',
            x=0.5,  # 标题水平居中
            y=0.93,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=dict(color='white', size=28, family='Arial')  # 设置标题字体大小
        ),
        showlegend=True,
        height=650,
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor,
        legend=dict(
            y=0,
            x=0.9,
            yanchor='top',
            xanchor='left',
            font=dict(color='white', size=12, family='Arial')),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular',
            coastlinecolor='rgb(180,180,180)',
            showocean=True,
            oceancolor='rgb(239, 243, 255)',
            showcountries=True,
            countrycolor='rgb(180,180,180)',
            showlakes=True,
            lakecolor='rgb(239, 243, 255)',
            showrivers=False
        ),
        # paper_bgcolor='black',
        plot_bgcolor='rgba(17,17,17,0)'
    )
        
    st.plotly_chart(fig, use_container_width=True)