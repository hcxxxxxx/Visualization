# 用户多维度3D分布

import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np

def chart_10(df, pcolor, title_font, tick_font):
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
                    font=dict(color='white', family='Arial')
                ),
                tickfont=dict(color='white', family='Arial')
            ),
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
            font=title_font
        ),
        scene=dict(
            xaxis=dict(
                title='关注者数量',
                titlefont=dict(color='white', family='Arial'),
                tickfont=dict(color='white', family='Arial'),
                gridcolor='rgba(255,255,255,0.1)',
                backgroundcolor='rgba(0,0,0,0.4)',
                showbackground=True
            ),
            yaxis=dict(
                title='仓库数量',
                titlefont=dict(color='white', family='Arial'),
                tickfont=dict(color='white', family='Arial'),
                gridcolor='rgba(255,255,255,0.1)',
                backgroundcolor='rgba(0,0,0,0.4)',
                showbackground=True
            ),
            zaxis=dict(
                title='2024年贡献',
                titlefont=dict(color='white', family='Arial'),
                tickfont=dict(color='white', family='Arial'),
                gridcolor='rgba(255,255,255,0.1)',
                backgroundcolor='rgba(0,0,0,0.4)',
                showbackground=True
            )
        ),
        paper_bgcolor=pcolor,
        # plot_bgcolor='rgba(17,17,17,0.5)',
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