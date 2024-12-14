# 最受欢迎语言Top10

import streamlit as st
import plotly.express as px
def chart_05(df, pcolor, title_font, tick_font):
    # Chart5: 语言分布饼图
    languages = df['languages'].explode().value_counts().head(10)

    colors = [
        'rgb(255,0,0)',      # 鲜红
        'rgb(255,165,0)',    # 橙色
        'rgb(255,255,0)',    # 鲜黄
        'rgb(0,255,0)',      # 鲜绿
        'rgb(0,255,255)',    # 青色
        'rgb(0,128,255)',    # 亮蓝
        'rgb(255,0,255)',    # 品红
        'rgb(255,105,180)',  # 热粉红
        'rgb(205,92,92)',    # 粉棕色
        'rgb(139,69,0)'     # 棕褐色
    ]

    fig3 = px.pie(values=languages.values,
                  names=languages.index,
                  color_discrete_sequence=colors)
    fig3.update_layout(
        title=dict(
            text='最受欢迎编程语言 Top 10',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=title_font  # 设置标题字体大小
        ),
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor,
        legend=dict(font=tick_font,bgcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig3, use_container_width=True)