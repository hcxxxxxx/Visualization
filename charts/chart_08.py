# Top10组织与编程语言关系

import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np

def chart_08(df, pcolor, title_font, tick_font):
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
                color = "rgba(0,0,0,0)",  # 透明边框
                width = 0
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
            font=title_font
        ),
        font=dict(color='white', size=12, family='Arial'),
        paper_bgcolor=pcolor,
        plot_bgcolor='rgba(17,17,17,0)',
        height=600,
        margin=dict(t=60, b=30, l=30, r=30)
    )
    
    st.plotly_chart(fig7, use_container_width=True)
