# Pro用户比例

import streamlit as st
import plotly.express as px

def chart_04(df, pcolor):
    # Chart4: Github Pro比例饼
    pro_counts = df['is_pro'].value_counts()
    pro_counts.index = ['Github Pro用户' if x else '非Github Pro用户' for x in pro_counts.index]
    fig4 = px.pie(values=pro_counts.values,
                  names=pro_counts.index)
    fig4.update_layout(
        title=dict(
            text='Github Pro 用户比例',
            x=0.5,  # 标题水平居中
            y=0.95,  # 向下移动标题
            xanchor='center',
            yanchor='top',
            font=dict(color='white', size=16, family='Arial')  # 设置标题字体大小
        ),
        margin=dict(l=10, r=10),
        paper_bgcolor=pcolor
    )
    st.plotly_chart(fig4, use_container_width=True)