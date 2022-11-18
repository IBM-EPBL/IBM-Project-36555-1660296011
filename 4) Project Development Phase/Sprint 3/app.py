import numpy as np
import pandas
from flask import Flask, request, jsonify, render_template
import pickle
import inputScript

app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')


ans = ""   
bns = ""   
@app.route('/y_predict', methods=['POST','GET'])
def y_predict():
    url = request.form['url']
    checkprediction = inputScript.main(url)
    prediction = model.predict(checkprediction)
    print(prediction)
    output=prediction[0]
    if(output==1):
        pred="You are safe!!  This is a legitimate Website."
        return render_template('index.html',bns=pred)
    
    else:
        pred="You are on the wrong site. Be cautious!"        
        return render_template('index.html',ans=pred)


@app.route('/predict_api', methods=['POST'])
def predict_api():
    
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output=prediction[0]
    return jsonify(output)        
 
if __name__ == '__main__':
    app.run()
    


# In[10]:





# In[ ]:


'''import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
#importing the inputScript file used to analyze the URL
import inputScript 


#load model
app = Flask(__name__)
model = pickle.load(open("Phishing_Website.pkl", 'rb'))

@app.route('/')
# def helloworld():
#     return render_template("index.html")


#Redirects to the page to give the user input URL.
@app.route('/predict')
def predict():
    return render_template('index.html')

#Fetches the URL given by the URL and passes to inputScript
@app.route('/y_predict',methods=['POST'])
def y_predict():
   
   # For rendering results on HTML GUI
  
    url = request.form['URL']
    checkprediction = inputScript.FeatureExtraction(url)
    print(checkprediction)
    prediction = model.predict(np.array(checkprediction.features).reshape(-1,30))
    print(prediction)
    output=prediction[0]
    if(output==1):
        pred="Your are safe!!  This is a Legitimate Website."
        
    else:
        pred="You are on the wrong site. Be cautious!"
    return render_template('index.html', prediction_text='{}'.format(pred),url=url)

#Takes the input parameters fetched from the URL by inputScript and returns the predictions
@app.route('/predict_api',methods=['POST'])
def predict_api():
   
    #For direct API calls trought request
  
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    '''