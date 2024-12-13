# 仓库数量分布

import streamlit as st
import plotly.express as px
def chart_06(df, pcolor):
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
            font=dict(color='white', size=16, family='Arial')  # 设置标题字体大小
        ),
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor,
        plot_bgcolor='rgba(17,17,17,0)'
    )
    st.plotly_chart(fig5, use_container_width=True)