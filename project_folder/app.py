from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def tab1():
    df = pd.read_csv('project_folder/static/csv/AnimeList.csv')
    top10 = df.sort_values(by='Popularity').head(10)

    ratings = top10['Rating']
    plt.figure(figsize=(5, 3))
    plt.hist(ratings, bins=5, color='#7f3e16', edgecolor='black')
    plt.title('Rating Distribution (Top 10 Anime)', fontsize=12)
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.tight_layout()

    hist_path = 'project_folder/static/images/ratings_hist.png'
    os.makedirs(os.path.dirname(hist_path), exist_ok=True)
    plt.savefig(hist_path)
    plt.close()

    table_data = top10[['Popularity', 'Anime']].to_html(classes='table table-striped', index=False)

    return render_template('tab1.html', table=table_data, hist_url='/static/images/ratings_hist.png')

@app.route('/tab2')
def tab2():
    df = pd.read_csv('project_folder/static/csv/AnimeList.csv')
    top3 = df.sort_values(by='Popularity').head(3)

    plt.figure(figsize=(5, 3))
    bar_width = 0.4
    bars = plt.bar(top3['Anime'], top3['Rating'], color='#7f3e16', width=bar_width)
    plt.xlabel('Anime', fontsize=10)
    plt.ylabel('Rating', fontsize=10)
    plt.title('Top 3 Most Popular Anime by Rating', fontsize=12)
    plt.ylim(0, 10)
    plt.yticks(range(0, 11), fontsize=8)
    plt.xticks(rotation=45, ha='right', fontsize=8)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}',
                 ha='center', va='bottom', fontsize=8, color='black')

    plt.tight_layout()
    chart_path = 'project_folder/static/images/anime_chart.png'
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    plt.savefig(chart_path)
    plt.close()

    table_data = top3[['Popularity', 'Anime', 'Genre', 'Rating', 'Seasons']].to_html(
        classes='table table-striped', index=False
    )

    return render_template('tab2.html', table=table_data, chart_url='/static/images/anime_chart.png')

@app.route('/recommend')
def recommend():
    df = pd.read_csv('project_folder/static/csv/AnimeRecommendations.csv')
    random_row = df.sample(1).iloc[0]
    recommendation = {
        'Title': str(random_row['Title']),
        'Genre': str(random_row['Genre']),
        'Episodes': int(random_row['Episodes']) 
    }
    return jsonify(recommendation)

if __name__ == '__main__':
    app.run(debug=True)
