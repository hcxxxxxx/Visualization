# 国家与编程语言分布

import streamlit as st
import pandas as pd
import plotly.express as px
def chart_09(df, pcolor):
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
        textfont=dict(color='white', family='Arial')
    )
    
    # 更新布局
    fig8.update_layout(
        title=dict(
            text='国家与编程语言分布',  # 保持原有的标题文本
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(color='white', size=16, family='Arial')
        ),
        font=dict(color='white', size=12, family='Arial'),
        paper_bgcolor=pcolor,
        plot_bgcolor='rgba(17,17,17,0)',
        height=600,
        margin=dict(t=60, b=30, l=30, r=30)
    )
    
    st.plotly_chart(fig8, use_container_width=True)