from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import streamlit as st
import pickle

app = Flask(__name__)

train_df = pd.read_csv('train.csv')
X_train, X_test, y_train, y_test = train_test_split(train_df['tweet'], train_df['label'], test_size=0.3, random_state=42)
vectorizer = CountVectorizer()
X_train_bow = vectorizer.fit_transform(X_train)
X_test_bow = vectorizer.transform(X_test)

@app.route('/')
def hello_world():
    usertwitte = ""
    text = ""
    return render_template('index.html'  , text=text , check=usertwitte)

@app.route('/predict', methods = ['POST'])
def get_predict():
    model_load = pickle.load(open('NB-Model.pkl','rb'))
    usertwitte = ""
    usertwitte = request.form['twitte']
    user_input = [usertwitte]
    twittw_pass = vectorizer.transform(user_input)
    p =  model_load.predict(twittw_pass)

    if p[0] == 0 :
        result = "Tweet Seems to be good."
    else:
        result = "Tweet Seems to be hateful."
        
    text =  str(result)

    return render_template('index.html', text=text , check=usertwitte) 

if __name__ == '__main__':
    app.run(debug=True)