import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
from io import StringIO
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt



# Initialize NLTK resources
stop_words = set(stopwords.words('english'))
porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Tokenize the text
    words = word_tokenize(text)
    
    # Remove stop words
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    # Perform stemming (you can also use lemmatization here)
    stemmed_words = [porter.stem(word) for word in filtered_words]
    
    # Join the words back into a string
    preprocessed_text = ' '.join(stemmed_words)
    
    return preprocessed_text

def vader_sentiment_result(sent):
    scores = analyser.polarity_scores(sent)
    if scores["neg"] > scores["pos"]:
            return 0
    return 1

def generate_wordcloud(text):
    # Simply print the processed text for each category
    print(text)

def sentiment(df):
    if isinstance(df, str):
      
        # Assuming df is a CSV string, adjust the function accordingly
        df = pd.read_csv(StringIO(df), header=None, names=['Comments'],nrows=None)
      
    # Check if 'Comment' column exists
    if 'Comments' not in df.columns:
        print(f"The DataFrame type is: {type(df)}")
        raise KeyError("The 'Comments' column is not present in the DataFrame",df.columns)
    
    # Preprocess the comments
    df['Comments'] = df['Comments'].apply(preprocess_text)

    # Apply sentiment analysis
    df['vader_sentiment'] = df['Comments'].apply(lambda x: vader_sentiment_result(x))

    positive_comments = df[df['vader_sentiment'] == 1]
    negative_comments = df[df['vader_sentiment'] == 0]

     # Generate word cloud for positive comments
    positive_text = ' '.join(positive_comments['Comments'])
    generate_wordcloud(positive_text)

    # Generate word cloud for negative comments
    negative_text = ' '.join(negative_comments['Comments'])
    generate_wordcloud(negative_text)

    # Return total number of positive and negative comments
    total_positive_comments = len(positive_comments)
    total_negative_comments = len(negative_comments)
    #total_no_of_comments  = len(df['vader_sentiment'])

    return total_positive_comments, total_negative_comments, positive_text, negative_text #,total_no_of_comments
    # Other processing or analysis as needed


# Initialize SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()