import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# 读取数据
with open('person_data_top200.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 将数据转换为 DataFrame
df = pd.DataFrame(data)

# Chart 1: 水平双向柱状图，followers & contributions
def chart1():
    df['followers'] = df['followers'].str.replace('k', '').astype(float) * 1000
    df['contributions_in_2024'] = pd.to_numeric(df['contributions_in_2024'], errors='coerce').fillna(0).astype(int)
    df_sorted = df.sort_values(by=['followers', 'contributions_in_2024'], ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.barh(df_sorted['name'], df_sorted['followers'], color='blue', label='Followers')
    plt.barh(df_sorted['name'], df_sorted['contributions_in_2024'], color='orange', label='Contributions', alpha=0.5)
    plt.xlabel('Count')
    plt.title('Top 200 GitHub Users: Followers & Contributions')
    plt.legend()
    plt.show()

# Chart 2: 世界地图，loc
def chart2():
    fig = px.choropleth(df, locations="loc", locationmode='country names', 
                        title='Top 200 Users Location Distribution')
    fig.show()

# Chart 3: 饼状图，languages
def chart3():
    languages = df['languages'].explode().value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(languages, labels=languages.index, autopct='%1.1f%%', startangle=140)
    plt.title('Most Popular Languages Distribution')
    plt.axis('equal')
    plt.show()

# Chart 4: 饼状图，is_pro
def chart4():
    is_pro_counts = df['is_pro'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(is_pro_counts, labels=is_pro_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('GitHub Pro Upgrade Status')
    plt.axis('equal')
    plt.show()

# Chart 5: 柱状图，repo_num
def chart5():
    df['repo_num'] = df['repo_num'].astype(int)
    plt.figure(figsize=(10, 6))
    plt.bar(df['name'], df['repo_num'], color='green')
    plt.xlabel('User')
    plt.ylabel('Number of Repositories')
    plt.title('Top 200 Users Repository Count')
    plt.xticks(rotation=90)
    plt.show()

# Chart 6: 柱状图，join_date
def chart6():
    df['join_date'] = df['join_date'].astype(int)
    join_counts = df['join_date'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    plt.bar(join_counts.index, join_counts.values, color='purple')
    plt.xlabel('Join Year')
    plt.ylabel('Number of Users')
    plt.title('Top 200 Users Join Year Distribution')
    plt.show()

# 调用所有图表函数
chart1()
chart2()
chart3()
chart4()
chart5()
chart6()
