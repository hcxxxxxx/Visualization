# 用户影响力分布

import plotly.graph_objects as go
import streamlit as st
import numpy as np
import pandas as pd

def chart_11(df, pcolor):
    # Chart10: 用户综合影响力趋势图

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
                    font=dict(color='white', family='Arial')
                ),
                tickfont=dict(color='white', family='Arial')
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
            font=dict(color='white', size=16, family='Arial')
        ),
        xaxis=dict(
            title='关注者数排名',
            titlefont=dict(color='white', size=12, family='Arial'),
            tickfont=dict(color='white', size=12, family='Arial'),
            # gridcolor='rgba(255,255,255,0.1)',
            tickmode='linear',
            dtick=20
        ),
        yaxis=dict(
            title='影响力分数',
            titlefont=dict(color='white', size=12, family='Arial'),
            tickfont=dict(color='white', size=12, family='Arial'),
            # gridcolor='rgba(255,255,255,0.1)'
        ),
        paper_bgcolor=pcolor,
        plot_bgcolor='rgba(17,17,17,0)',
        height=700,
        margin=dict(t=60, b=30, l=30, r=30),
        showlegend=True,
        legend=dict(
            font=dict(color='white', size=12, family='Arial'),
            # bgcolor='rgba(0,0,0,0)',
            # bordercolor='rgba(255,255,255,0.2)',
            x = 0.7,
            y = 1,
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig11, use_container_width=True)