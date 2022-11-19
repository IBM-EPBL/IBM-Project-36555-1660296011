import numpy as np
import pandas
from flask import Flask, request, jsonify, render_template
import pickle
import inputScript
import warnings
warnings.filterwarnings('ignore')

import requests

app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl','rb'))

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "6obABeznZn5tA-IxCaXq-fqblOJRsXOcHyfkAHauaGVI"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/')
def home():
    return render_template('index.html')


ans = ""   
bns = ""   
@app.route('/y_predict', methods=['POST','GET'])
def y_predict():
    url = request.form['url']
    checkprediction = inputScript.main(url)
    #print(checkprediction)
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [["IPAddress","LongURL","ShortURL","@Symbol","//Redirecting","PrefixSuffix","SubDomain","SSLfinal_state","DomainLength","Favicon","Port","HTTPStoken","RequestURL","AnchorURL","LinksInScriptTags","ServerFormHandler","InfoEmail","AbnormalURL","Redirect","Onmouseover","RightClick","PopupWindow","Iframe","AgeofDomain","DNSRecord","WebTraffic","PageRank","GoogleIndex","LinksPointingToPage","StatisticalReport"
]], "values": checkprediction}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/876222b8-8095-45a1-872c-5f80ec95a06b/predictions?version=2022-11-16', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions=response_scoring.json()
    print(predictions)
    pred=predictions['predictions'][0]['values'][0][0]
    print(pred)
    if(pred != -1):
     output="The Website is the Legitimate Website ... Continue!!"
     return render_template('index.html',bns=output)
    else:
        output="The Website is not Legitimate... BEWARE!!"
        return render_template('index.html',ans=output)

   

@app.route('/predict_api', methods=['POST'])
def predict_api():
    
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output=prediction[0]
    return jsonify(output)        
 
if __name__ == '__main__':
    app.run()
    



