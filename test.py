import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import pycountry
import numpy as np

# 设置页面配置
st.set_page_config(layout="wide", page_title="Github Top 200 用户分析")

# 设置页面背景颜色
page_bg_color = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #eeeeee;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

[data-testid="stToolbar"] {
    right: 2rem;
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

pcolor = '#ffffff'

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
st.title("Github Top 200 用户数据分析")

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    # 对数据进行升序排序
    df_sorted = df.sort_values('followers_count', ascending=True).reset_index(drop=True)
    
    # Chart1: 水平双向柱状图
    fig1 = go.Figure()

    # 添加 Contributions 数据
    fig1.add_trace(go.Bar(
        y=df_sorted['name'],
        x=df_sorted['contributions_in_2024'],
        name='Contributions in 2024',
        orientation='h',
        marker_color='#f79059',
        xaxis='x2',
        offsetgroup=2
    ))

    # 添加 Followers 数据
    fig1.add_trace(go.Bar(
        y=df_sorted['name'],
        x=df_sorted['followers_count'],
        name='Followers',
        orientation='h',
        marker_color='#3480b8',
        xaxis='x1',
        offsetgroup=1
    ))

    fig1.update_layout(
        title=dict(
            text='Top 200 用户的关注者数量和2024年贡献数对比',
            x=0.5,  # 标题水平居中
            y=0.97,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=dict(size=16)  # 设置标题字体大小
        ),
        height=870,
        yaxis=dict(
            tickfont=dict(size=12),
            range=[180, 200],
            autorange=False,
            showticklabels=True,
            type="category",
            constrain="domain",
            fixedrange=False,
            tickmode='linear',
            dtick=1
        ),
        xaxis=dict(
            range=[0, 250000],
            showgrid=True,
            fixedrange=True,
            rangemode='nonnegative',
            side='bottom',
            domain=[0, 1]
        ),
        xaxis2=dict(
            range=[0, 5000],
            showgrid=True,
            fixedrange=True,
            rangemode='nonnegative',
            side='bottom',
            overlaying='x',
            position=1,
            domain=[0, 1]
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=0,
            xanchor='right',
            x=1
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        dragmode='pan',
        bargap=0.15,
        bargroupgap=0.1,
        barmode='group',
        paper_bgcolor=pcolor
    )   
    
    # 添加底部滑块
    fig1.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.05
            )
        )
    )
    
    # 添加重置按钮
    fig1.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="重置视图",
                        method="relayout",
                        args=[{
                            "yaxis.range": [180, 200],
                            "xaxis.range": [0, 250000],
                            "xaxis2.range": [0, 5000]
                        }]
                    )
                ],
                pad={"r": 10, "t": 10},
                x=0,
                y=1.03
            )
        ]
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Chart2: 世界地图
    fig2 = go.Figure()
    
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
    fig2.add_trace(go.Choropleth(
        locations=locations,
        z=z_values,
        locationmode='ISO-3',
        colorscale=[
            [0, 'rgb(242,240,247)'],
            [0.2, 'rgb(218,218,235)'],
            [0.4, 'rgb(188,189,220)'],
            [0.6, 'rgb(158,154,200)'],
            [0.8, 'rgb(117,107,177)'],
            [1, 'rgb(84,39,143)']
        ],
        colorbar=dict(
            title='用户数量',
            thickness=15,        # 减小宽度
            len=0.5,            # 减小长度
            x=1,                # 调整水平位置
            y=0.5,              # 调整垂直位置
            yanchor='middle',   # 垂直对齐方式
            titleside='right',  # 标题位置
            ticks='outside'     # 刻度线位置
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
    fig2.add_trace(go.Scattergeo(
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
    
    fig2.update_layout(
        # title='Top 200 GitHub用户地理分布',
        title=dict(
            text='Top 200 GitHub用户地理分布',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=dict(size=16)  # 设置标题字体大小
        ),
        showlegend=True,
        height=450,
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor,
        legend=dict(
            y=1.15,
            x=0.01,
            yanchor='top',
            xanchor='left'
        ),
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
        # plot_bgcolor='white'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # 添加国家分布统计图
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
            font=dict(size=16)  # 设置标题字体大小
        ),
        xaxis_title='国家',
        yaxis_title='用户数量',
        xaxis_tickangle=-45,  # 倾斜x轴标签防叠
        height=400,  # 控制图表高度
        # margin=dict(t=50, b=50),  # 调整边距
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor,
        # plot_bgcolor='white',
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

# 创建新的两列布局
col3, col4 = st.columns(2)

with col3:
    # Chart3: 语言分布饼图
    languages = df['languages'].explode().value_counts().head(10)
    # fig3 = px.pie(values=languages.values,
    #               names=languages.index,
    #               title='最受欢迎编程语言 Top 10')
    fig3 = px.pie(values=languages.values,
                  names=languages.index)
    fig3.update_layout(
        title=dict(
            text='最受欢迎编程语言 Top 10',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=dict(size=16)  # 设置标题字体大小
        ),
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # Chart4: Github Pro比例饼
    pro_counts = df['is_pro'].value_counts()
    pro_counts.index = ['Github Pro用户' if x else '非Github Pro用户' for x in pro_counts.index]
    fig4 = px.pie(values=pro_counts.values,
                  names=pro_counts.index)
    fig4.update_layout(
        title=dict(
            text='Github Pro 用户比例',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=dict(size=16)  # 设置标题字体大小
        ),
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor
    )
    st.plotly_chart(fig4, use_container_width=True)

# 创建最后两列布局
col5, col6 = st.columns(2)

with col5:
    # Chart5: 仓库数量分布
    fig5 = px.histogram(df,
                       x='repo_num',
                       nbins=30,
                       color_discrete_sequence=px.colors.qualitative.Set3)
    fig5.update_traces(marker_line_width=1,
                      marker_line_color="white")
    fig5.update_layout(
        title=dict(
            text='仓库数量分布',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=dict(size=16)  # 设置标题字体大小
        ),
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    # Chart6: 上部分折线图下部分圆角柱状图
    join_year_counts = df['join_year'].value_counts().sort_index()
    
    # 补充缺失年份的数据（用户数为0）
    all_years = range(int(join_year_counts.index.min()), int(join_year_counts.index.max()) + 1)
    join_year_counts = join_year_counts.reindex(all_years, fill_value=0)
    
    fig6 = go.Figure()
    
    # 添加上半部分折线
    fig6.add_trace(go.Scatter(
        x=join_year_counts.index,
        y=join_year_counts.values,
        mode='lines',
        line=dict(
            shape='spline',
            smoothing=0,
            width=2,
            color='rgba(117,107,177,0.8)'
        ),
        fill='tonexty',
        fillcolor='rgba(117,107,177,0.4)',
        name='加入用户数',
        hovertemplate='%{y}人<extra></extra>'
    ))
    
    # 为每个年份创建下半部分圆角柱形
    for year, value in join_year_counts.items():
        if value == 0:
            continue  # 跳过数值为0的年份
            
        # 计算颜色深浅（值越大颜色越深）
        intensity = max(0.3, value/max(join_year_counts.values))
        # 从浅紫到深紫的渐变
        r = int(117 + (77-117)*intensity)
        g = int(107 + (61-107)*intensity)
        b = int(177 + (143-177)*intensity)
        color = f'rgb({r},{g},{b})'
        
        # 矩形主体
        fig6.add_trace(go.Scatter(
            x=[year-0.4, year-0.4, year+0.4, year+0.4],
            y=[0, -value, -value, 0],
            fill="toself",
            mode='none',
            fillcolor=color,
            hoverinfo='skip'
        ))
    
    # 添加箭头
    fig6.add_annotation(
        x=max(join_year_counts.index) + 3,
        y=0,
        ax=max(join_year_counts.index) + 2.5,
        ay=0,
        xref='x',
        yref='y',
        axref='x',
        ayref='y',
        text='',
        showarrow=True,
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor='rgba(0,0,0,0.8)'
    )
    
    # 更新布局
    fig6.update_layout(
        title=dict(
            text='用户加入 Github 年份分布',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=dict(size=16)  # 设置标题字体大小
        ),
        showlegend=False,
        # height=400,
        margin=dict(b=30, l=30, r=30),
        paper_bgcolor=pcolor,
        # plot_bgcolor='white',
        yaxis=dict(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='rgb(117,107,177)',
            showgrid=False,
            showticklabels=False
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickmode='linear',
            dtick=1
        )
    )
    
    st.plotly_chart(fig6, use_container_width=True)

# 创建新的两列布局
col7, col8 = st.columns(2)

with col7:
    # Chart7: 桑基图
    # 数据准备
    org_lang_counts = []
    org_df = df.dropna(subset=['org', 'languages'])
    
    # 清洗数据：跳过空org和org与loc相同的情况
    org_df = org_df[org_df['org'] != org_df['loc']]
    
    for idx, row in org_df.iterrows():
        for lang in row['languages']:
            org_lang_counts.append((row['org'], lang))

    ol_df = pd.DataFrame(org_lang_counts, columns=['org', 'language'])
    top_orgs = ol_df['org'].value_counts().head(10).index
    ol_filtered = ol_df[ol_df['org'].isin(top_orgs)]
    ol_count = ol_filtered.groupby(['org','language']).size().reset_index(name='count')

    # 构建Sankey数据
    all_orgs = ol_count['org'].unique().tolist()
    all_langs = ol_count['language'].unique().tolist()
    nodes = all_orgs + all_langs

    # 节点索引映射
    node_dict = {node: i for i, node in enumerate(nodes)}

    # 准备links数据
    links = {
        'source': [],
        'target': [],
        'value': []
    }

    for _, r in ol_count.iterrows():
        links['source'].append(node_dict[r['org']])
        links['target'].append(node_dict[r['language']])
        links['value'].append(r['count'])

    # 计算每个节点的连接数
    node_connections = {}
    for node in nodes:
        if node in all_orgs:
            # 对于组织，计算它连接的语言数量
            node_connections[node] = len(ol_count[ol_count['org'] == node])
        else:
            # 对于语言，计算使用它的组织数量
            node_connections[node] = len(ol_count[ol_count['language'] == node])
    
    # 计算连接的颜色
    max_connections = max(node_connections.values())
    node_colors = []
    for node in nodes:
        intensity = max(0.3, node_connections[node]/max_connections)
        if node in all_orgs:
            # 组织节点的颜色
            r = int(117 + (77-117)*intensity)
            g = int(107 + (61-107)*intensity)
            b = int(177 + (143-177)*intensity)
        else:
            # 语言节点的颜色
            r = int(77 + (117-77)*intensity)
            g = int(61 + (107-61)*intensity)
            b = int(143 + (177-143)*intensity)
        node_colors.append(f'rgb({r},{g},{b})')
    
    # 为节点设置渐变色系
    org_colors = [
        f'rgb({255-i*10},{140+i*5},{i*10})'  # 从橙红色到色的渐变
        for i in range(len(all_orgs))
    ]
    
    lang_colors = [
        f'rgb({50+i*10},{200-i*5},{220-i*5})'  # 从青色到深蓝的渐变
        for i in range(len(all_langs))
    ]
    
    # 计算连接的颜色
    link_colors = []
    for _, r in ol_count.iterrows():
        source_idx = node_dict[r['org']]
        target_idx = node_dict[r['language']] - len(all_orgs)
        # 混合源节点和目标节点的颜色
        source_color = np.array([int(c) for c in org_colors[source_idx][4:-1].split(',')])
        target_color = np.array([int(c) for c in lang_colors[target_idx][4:-1].split(',')])
        mix_color = (source_color + target_color) / 2
        link_colors.append(f'rgba({int(mix_color[0])},{int(mix_color[1])},{int(mix_color[2])},0.4)')

    # 创建桑基图
    fig7 = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(
                color = "white",
                width = 0.5
            ),
            label = nodes,
            color = org_colors + lang_colors,
            customdata = ['组织'] * len(all_orgs) + ['语言'] * len(all_langs),
            hovertemplate='%{label}<br>类型: %{customdata}<br>连接数: %{value}<extra></extra>'
        ),
        link = dict(
            source = links['source'],
            target = links['target'],
            value = links['value'],
            color = link_colors,
            hovertemplate='%{source.label} → %{target.label}<br>数量: %{value}<extra></extra>'
        )
    )])

    # 更新布局
    fig7.update_layout(
        title=dict(
            text='Top 10 组织与编程语言关系图',  # 保持原有的标题文本
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(
                size=16
            )
        ),
        font=dict(size=12),
        paper_bgcolor=pcolor,
        # plot_bgcolor='rgb(17,17,17)',
        height=600,
        margin=dict(t=60, b=30, l=30, r=30)
    )
    
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    # Chart8: 旭日图
    # 数据准备
    country_lang_counts = []
    
    for idx, row in df.dropna(subset=['languages']).iterrows():
        country = row['country'] if pd.notna(row['country']) else 'Unknown'
        for lang in row['languages']:
            country_lang_counts.append((country, lang))

    cl_df = pd.DataFrame(country_lang_counts, columns=['country', 'language'])
    cl_count = cl_df.groupby(['country','language']).size().reset_index(name='count')
    
    # 过滤掉 'Other' 和 'Unknown' 国家
    cl_count = cl_count[~cl_count['country'].isin(['Other', 'Unknown'])]
    
    # 创建旭日图
    fig8 = px.sunburst(
        cl_count,
        path=['country', 'language'],
        values='count',
        color='count',
        color_continuous_scale=[
            [0, 'rgb(255,140,0)'],      # 橙色
            [0.2, 'rgb(255,0,128)'],    # 粉红
            [0.4, 'rgb(128,0,255)'],    # 紫色
            [0.6, 'rgb(0,128,255)'],    # 蓝色
            [0.8, 'rgb(0,255,192)'],    # 青色
            [1, 'rgb(0,255,64)']        # 绿色
        ],
        maxdepth=2,
        branchvalues='total'
    )
    
    # 更新悬停信息样式
    hover_template = """
        <b style='color: white'>%{label}</b><br>
        用户数量: %{value}<br>
        占比: %{percentParent:.1%} of %{parent}
        <extra></extra>
    """
    
    fig8.update_traces(
        hovertemplate=hover_template,
        textfont=dict(color='white')
    )
    
    # 更新布局
    fig8.update_layout(
        title=dict(
            text='国家与编程语言分布',  # 保持原有的标题文本
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(
                size=16
            )
        ),
        font=dict(size=12),
        paper_bgcolor=pcolor,
        # plot_bgcolor='rgb(17,17,17)',
        height=600,
        margin=dict(t=60, b=30, l=30, r=30)
    )
    
    st.plotly_chart(fig8, use_container_width=True)

# 创建新的两列布局
col9, col10 = st.columns(2)

with col9:
    # Chart9: 3D散点图

    def convert_to_number(value):
        if pd.isna(value):
            return 0
        if isinstance(value, (int, float)):
            return value
        value = str(value).lower()
        multipliers = {'k': 1000, 'm': 1000000, 'b': 1000000000}
        for suffix, multiplier in multipliers.items():
            if suffix in value:
                try:
                    return float(value.replace(suffix, '')) * multiplier
                except ValueError:
                    return 0
        try:
            return float(value)
        except ValueError:
            return 0
    
    # 准备数据
    plot_df = df.copy()
    plot_df['followers_num'] = df['followers'].apply(convert_to_number)
    plot_df['stars_num'] = df['stars'].apply(convert_to_number)
    
    # 创建3D散点图
    fig9 = go.Figure()
    
    # 添加散点
    fig9.add_trace(go.Scatter3d(
        x=plot_df['followers_num'],
        y=plot_df['repo_num'],
        z=plot_df['contributions_in_2024'],
        mode='markers',
        marker=dict(
            size=plot_df['stars_num'].apply(lambda x: np.log(x + 1) * 2),  # 使用对数缩放
            color=plot_df['stars_num'],  # 颜色基于stars数量
            colorscale=[
                [0, 'rgb(255,140,0)'],      # 橙色
                [0.2, 'rgb(255,0,128)'],    # 粉红
                [0.4, 'rgb(128,0,255)'],    # 紫色
                [0.6, 'rgb(0,128,255)'],    # 蓝色
                [0.8, 'rgb(0,255,192)'],    # 青色
                [1, 'rgb(0,255,64)']        # 绿色
            ],
            opacity=0.8,
            colorbar=dict(
                title=dict(
                    text="Stars数",
                    # font=dict(color='white')
                ),
                # tickfont=dict(color='white')
            )
        ),
        text=plot_df['name'],  # 用于悬停显示
        hovertemplate=
        "<b>%{text}</b><br>" +
        "关注者: %{x:,.0f}<br>" +
        "仓库数: %{y:,.0f}<br>" +
        "2024贡献: %{z:,.0f}<br>" +
        "<extra></extra>"
    ))
    
    # 更新布局
    fig9.update_layout(
        title=dict(
            text='用户多维度3D分布',
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=16)
        ),
        scene=dict(
            xaxis=dict(
                title='关注者数量',
                # titlefont=dict(color='white'),
                # tickfont=dict(color='white'),
                gridcolor='rgba(255,255,255,0.1)',
                backgroundcolor='#dddddd',
                showbackground=True
            ),
            yaxis=dict(
                title='仓库数量',
                # titlefont=dict(color='white'),
                # tickfont=dict(color='white'),
                gridcolor='rgba(255,255,255,0.1)',
                backgroundcolor='#dddddd',
                showbackground=True
            ),
            zaxis=dict(
                title='2024年贡献',
                # titlefont=dict(color='white'),
                # tickfont=dict(color='white'),
                gridcolor='rgba(255,255,255,0.1)',
                backgroundcolor='#dddddd',
                showbackground=True
            )
        ),
        paper_bgcolor=pcolor,
        # plot_bgcolor='rgb(17,17,17)',
        height=700,
        margin=dict(t=60, b=30, l=30, r=30)
    )
    
    # 添加相机视角
    fig9.update_layout(
        scene_camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    )
    
    st.plotly_chart(fig9, use_container_width=True)

with col10:
    # Chart10: 用户综合影响力趋势图

    # 首先创建数值型的followers列
    df['followers_num'] = df['followers'].apply(convert_to_number)
    
    def calculate_influence_score(row):
        """计算用户综合影响力分数
        
        计算公式：
        1. followers_score: 关注者数量的对数值 (权重: 0.4)
        2. contribution_score: 2024年贡献数的对数值 (权重: 0.3)
        3. repo_score: 仓库数量的对数值 (权重: 0.2)
        4. experience_score: 注册年限 (权重: 0.1)
        
        所有分数都归一化到0-100的范围
        """
        # 获取当前年份
        current_year = 2024
        
        # 计算各项原始分数
        followers_num = convert_to_number(row['followers'])
        followers_score = np.log10(followers_num + 1)
        
        contribution_score = np.log10(float(row['contributions_in_2024']) + 1)
        
        repo_score = np.log10(float(convert_to_number(row['repo_num'])) + 1)
        
        join_year = pd.to_datetime(row['join_date']).year
        experience_years = current_year - join_year
        experience_score = experience_years
        
        return {
            'followers_score': followers_score,
            'contribution_score': contribution_score,
            'repo_score': repo_score,
            'experience_score': experience_score
        }
    
    # 计算所有用户的原始分数
    scores = []
    for _, row in df.iterrows():
        if row['contributions_in_2024'] == None:
            scores.append(dict())
            continue
        score_dict = calculate_influence_score(row)
        scores.append(score_dict)
    
    # 转换为DataFrame
    scores_df = pd.DataFrame(scores)
    
    # 对每个维度进行归一化（0-100）
    for column in scores_df.columns:
        min_val = scores_df[column].min()
        max_val = scores_df[column].max()
        scores_df[column] = 100 * (scores_df[column] - min_val) / (max_val - min_val)
    
    # 计算加权总分
    weights = {
        'followers_score': 0.4,
        'contribution_score': 0.3,
        'repo_score': 0.2,
        'experience_score': 0.1
    }
    
    df['influence_score'] = sum(scores_df[col] * weight 
                              for col, weight in weights.items())
    
    # 使用followers_num进行排序
    df['followers_rank'] = df['followers_num'].rank(ascending=False)
    
    # 创建趋势图
    fig11 = go.Figure()
    
    # 添加主要趋势线
    fig11.add_trace(go.Scatter(
        x=df['followers_rank'],
        y=df['influence_score'],
        mode='lines',
        name='影响力趋势',
        line=dict(
            color='rgba(0,128,255,0.8)',
            width=1
        )
    ))
    
    # 添加散点
    fig11.add_trace(go.Scatter(
        x=df['followers_rank'],
        y=df['influence_score'],
        mode='markers',
        name='用户',
        marker=dict(
            size=10,
            color=df['influence_score'],
            colorscale=[
                [0, 'rgb(255,140,0)'],      # 橙色
                [0.2, 'rgb(255,0,128)'],    # 粉红
                [0.4, 'rgb(128,0,255)'],    # 紫色
                [0.6, 'rgb(0,128,255)'],    # 蓝色
                [0.8, 'rgb(0,255,192)'],    # 青色
                [1, 'rgb(0,255,64)']        # 绿色
            ],
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="影响力分数",
                    # font=dict(color='white')
                ),
                # tickfont=dict(color='white')
            )
        ),
        text=[f"{name}<br>关注者: {followers:,}" 
              for name, followers in zip(df['name'], df['followers_num'])],
        hovertemplate=
        "<b>%{text}</b><br>" +
        "关注者排名: %{x:.0f}<br>" +
        "影响力分数: %{y:.1f}<br>" +
        "<extra></extra>"
    ))
    
    # 更新布局
    fig11.update_layout(
        title=dict(
            text='GitHub Top 200 用户影响力分布 (按关注者数排序)',
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=16)
        ),
        xaxis=dict(
            title='关注者数排名',
            # titlefont=dict(color='white'),
            # tickfont=dict(color='white'),
            # gridcolor='rgba(255,255,255,0.1)',
            tickmode='linear',
            dtick=20
        ),
        yaxis=dict(
            title='影响力分数',
            # titlefont=dict(color='white'),
            # tickfont=dict(color='white'),
            # gridcolor='rgba(255,255,255,0.1)'
        ),
        paper_bgcolor=pcolor,
        # plot_bgcolor='rgb(17,17,17)',
        height=700,
        margin=dict(t=60, b=30, l=30, r=30),
        showlegend=True,
        legend=dict(
            # font=dict(color='white'),
            # bgcolor='rgba(0,0,0,0)',
            # bordercolor='rgba(255,255,255,0.2)',
            x = 0.8,
            y = 1,
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig11, use_container_width=True)
    