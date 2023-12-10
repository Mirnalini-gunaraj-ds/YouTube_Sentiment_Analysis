from flask import Flask, render_template, request, jsonify
import url_to_df, df_to_senti
from flask_cors import CORS
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from textblob import TextBlob
from wordcloud import WordCloud
import requests
import os
from matplotlib.pyplot import figure, imshow, axis, savefig
import base64
from io import BytesIO
import matplotlib.pyplot as plt  # Import plt for other functions if needed

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/analyze": {"origins": ["http://localhost:5000", "http://127.0.0.1:5000"]}})
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

# Replace 'YOUR_API_KEY' with your actual API key
#API_KEY = 'AIzaSyAYlcJkAwyshjEYK1acVSKgWWjOGmVp3l0'
#youtube = build('youtube', 'v3', developerKey=API_KEY)

def save_figure(figure, filename):
    filepath = os.path.join('static', filename)
    figure.savefig(filepath, bbox_inches='tight')
    return filepath

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/proxy', methods=['GET'])
def proxy():
    # Replace 'http://localhost:3000' with the actual URL of your local development server
    target_url = 'http://localhost:5000'
    response = requests.get(target_url)
    return jsonify(response.json())

@app.route('/analyze', methods=['POST'])
def analyze():
    youtube_url = request.form.get('youtube_url')
    print(youtube_url)

    df = url_to_df.clean(youtube_url)
    print(type(df))

    # Passing the list of comments to df_to_senti.sentiment
    total_positive_comments, total_negative_comments, positive_text, negative_text = df_to_senti.sentiment(df)
    print(total_positive_comments)
    print(total_negative_comments)

    # Generate word cloud for positive comments
    #positive_wordcloud = WordCloud(width=800, height=400).generate(" ".join(total_positive_comments))
    positive_wordcloud = WordCloud(width=800, height=400).generate(" ".join(positive_text.split()))

    plt.figure(figsize=(8, 4))
    plt.imshow(positive_wordcloud, interpolation='bilinear')
    plt.axis('off')

    # Save the positive word cloud image to a BytesIO object
    positive_wordcloud_image = BytesIO()
    positive_wordcloud.to_image().save(positive_wordcloud_image, format='PNG')
    positive_wordcloud_image = base64.b64encode(positive_wordcloud_image.getvalue()).decode('utf-8')

    # Generate word cloud for negative comments
    #negative_wordcloud = WordCloud(width=800, height=400).generate(" ".join(total_negative_comments))
    negative_wordcloud = WordCloud(width=800, height=400).generate(" ".join(negative_text.split()))
    plt.figure(figsize=(8, 4))
    plt.imshow(negative_wordcloud, interpolation='bilinear')
    plt.axis('off')

    # Save the negative word cloud image to a BytesIO object
    negative_wordcloud_image = BytesIO()
    negative_wordcloud.to_image().save(negative_wordcloud_image, format='PNG')
    negative_wordcloud_image = base64.b64encode(negative_wordcloud_image.getvalue()).decode('utf-8')


     # Process the results and return a response
    result = {
        'total_positive_comments': total_positive_comments,
        'total_negative_comments': total_negative_comments,
        'positive_wordcloud_image': positive_wordcloud_image,
        'negative_wordcloud_image': negative_wordcloud_image
        #,'total_no_of_comments': total_no_of_comments
      }
 
    # Render the template with the result data
    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)