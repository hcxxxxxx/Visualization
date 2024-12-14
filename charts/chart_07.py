# 加入Github年份分布

import plotly.graph_objects as go
import streamlit as st

def chart_07(df, pcolor, title_font, tick_font):
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
            color='rgba(111,111,255,0.9)'
        ),
        fill='tonexty',
        fillcolor='rgba(111,111,255,0.6)',
        name='加入用户数',
        hovertemplate='%{y}人<extra></extra>'
    ))
    
    for year, value in join_year_counts.items():
        if value == 0:
            continue  # 跳过数值为0的年份
            
        # 计算颜色深浅（值越大颜色越深）
        intensity = max(0.7, value/max(join_year_counts.values))
        # 从浅紫到深紫的渐变
        # r = int(117 + (77-117)*intensity)
        # g = int(107 + (61-107)*intensity)
        # b = int(177 + (143-177)*intensity)
        # color = f'rgb({r},{g},{b})'
        color = f'rgba(111,33,222,{intensity})'
        
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
        x=max(join_year_counts.index) + 4,
        y=0,
        ax=max(join_year_counts.index) + 2,
        ay=0,
        xref='x',
        yref='y',
        axref='x',
        ayref='y',
        text='',
        showarrow=True,
        arrowhead=3,
        arrowsize=3,
        arrowwidth=2,
        arrowcolor='rgba(255,255,255,1)'
    )
    
    # 更新布局
    fig6.update_layout(
        title=dict(
            text='用户加入 Github 年份分布',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=title_font  # 设置标题字体大小
        ),
        showlegend=False,
        # height=400,
        margin=dict(b=30, l=30, r=30),
        paper_bgcolor=pcolor,
        plot_bgcolor='rgba(17,17,17,0)',
        yaxis=dict(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='rgba(255,255,255,1)',
            showgrid=False,
            showticklabels=False,
            tickfont=tick_font
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.2)',
            zeroline=False,
            tickmode='linear',
            dtick=5,
            tickfont=tick_font
        )
    )
    
    st.plotly_chart(fig6, use_container_width=True)