from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__, template_folder=r'C:\Users\apurb\Desktop\Sentiment Analysis\templates')

categorical_to_string = {
    0: 'Negative',
    1: 'Positive',
    2: 'Neutral'
}

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        
        model = pickle.load(open('model.pkl', 'rb'))
        vectorizer = pickle.load(open("vector.pkl", "rb"))

        transformed_reviews = vectorizer.transform(df['Reviews'])
        predictions = model.predict(transformed_reviews)
        
        num_positives = np.count_nonzero(predictions == 1)
        num_negatives = np.count_nonzero(predictions == 0)
        num_neutrals = np.count_nonzero(predictions == 2)
        num_reviews = len(predictions)
        percent_positive = num_positives / num_reviews * 100
        percent_negative = num_negatives / num_reviews * 100
        percent_neutral = num_neutrals / num_reviews * 100

        return render_template('index2.html', 
            num_reviews=num_reviews, 
            percent_positive=percent_positive, 
            percent_negative=percent_negative,
            percent_neutral=percent_neutral)

    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)
