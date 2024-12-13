# 最受欢迎语言Top10

import streamlit as st
import plotly.express as px
def chart_05(df, pcolor, title_font, tick_font):
    # Chart5: 语言分布饼图
    languages = df['languages'].explode().value_counts().head(10)

    fig3 = px.pie(values=languages.values,
                  names=languages.index)
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
        legend=dict(font=tick_font, x=0.75, y=0.5)
    )
    st.plotly_chart(fig3, use_container_width=True)