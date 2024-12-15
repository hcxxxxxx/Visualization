# 关注者数量和贡献数对比

import plotly.graph_objects as go
import streamlit as st

def chart_02(df, pcolor, title_font, tick_font):
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
        marker_color='rgba(148,0,211,0.8)',
        xaxis='x2',
        offsetgroup=2
    ))

    # 添加 Followers 数据
    fig1.add_trace(go.Bar(
        y=df_sorted['name'],
        x=df_sorted['followers_count'],
        name='Followers',
        orientation='h',
        marker_color='rgba(255,20,147,0.8)',
        xaxis='x1',
        offsetgroup=1
    ))

    fig1.update_layout(
        title=dict(
            text='Top 200 用户的关注者数量和2024年贡献数对比',
            x=0.5,  # 标题水平居中
            y=0.955,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=title_font  # 设置标题字体大小
        ),
        height=865,
        yaxis=dict(
            tickfont=tick_font,
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
            gridcolor='rgba(255,255,255,0.1)',
            gridwidth=1,
            fixedrange=True,
            rangemode='nonnegative',
            side='bottom',
            tickfont=tick_font,
            domain=[0, 1]
        ),
        xaxis2=dict(
            range=[0, 5000],
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            gridwidth=1,
            fixedrange=True,
            rangemode='nonnegative',
            side='bottom',
            overlaying='x',
            position=1,
            tickfont=tick_font,
            domain=[0, 1]
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=0,
            xanchor='right',
            x=1,
            font=tick_font,
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        dragmode='pan',
        bargap=0.15,
        bargroupgap=0.1,
        barmode='group',
        paper_bgcolor=pcolor,
        plot_bgcolor='rgba(17,17,17,0)'
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
                y=-0.04
            )
        ]
    )
    
    st.plotly_chart(fig1, use_container_width=True)