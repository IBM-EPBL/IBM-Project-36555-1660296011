import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import inputScript
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')


ans = ""   
bns = ""   
@app.route('/y_predict', methods=['POST','GET'])
def y_predict():
    url = request.form['url']
    print(url)
    checkprediction = inputScript.main(url)
    prediction = model.predict(checkprediction)
    print("Prediction = " ,prediction)
    output=prediction[0]
    if(output==1):
        pred="You are safe!!  This is a legitimate Website."
        return render_template('output.html',url=url,bns=pred)
    
    else:
        pred="You are on the wrong site. Be cautious!"        
        return render_template('output.html',ans=pred,url=url)
   
 
if __name__ == '__main__':
    app.run()
    