# 仓库数量分布
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
def chart_06(df, pcolor, title_font, tick_font):
    # Chart5: 仓库数量分布
    fig5 = go.Figure()
    fig5.add_trace(go.Histogram(
        x=df['repo_num'],
        nbinsx=30,
        marker_color=[f'rgba(255,255,0,{1-i*0.05})' for i in range(20)],
        marker_line_width=1,
        marker_line_color="rgba(255,255,255,1)",
        opacity=0.8
    ))
    fig5.update_layout(
        title=dict(
            text='仓库数量分布',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=title_font  # 设置标题字体大小
        ),
        margin=dict(l=10, r=10),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', gridwidth=1, tickfont=tick_font),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', gridwidth=1, tickfont=tick_font),
        xaxis_title=dict(text='仓库数量', font=tick_font),
        yaxis_title=dict(text='用户数', font=tick_font),
        paper_bgcolor=pcolor,
        plot_bgcolor='rgba(17,17,17,0)'
    )
    st.plotly_chart(fig5, use_container_width=True)