from flask import Flask, request, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup


from keras import models    

import numpy as np 
import pandas as pd 

import matplotlib.pyplot as plt
import seaborn as sns

import os
#Importing dependencies
from urllib.parse import urlparse
import os.path
import re

import keras
import joblib
import tensorflow as tf




# model = pickle.load(open('model.pkl', 'rb'))
#model = load_model('model.pkl', custom_objects={'auc': auc})
# model = tf.keras.models.load_model('./model/model.pkl')

model = models.load_model('./model/model.h5', custom_objects={'tf': tf})


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_flask():
    return render_template('index.html')


'''
@app.route('/', methods=['GET', 'POST'])
def hello_flask():
    results = {}
    if request.method == "POST" :
        url = request.form["url"]
        result = preprocessing(url)
        msg = "%s 분석 결과 : %s"  %(url, result)
        print(msg)
        results[url] = result
        return results
    return "NONE"
    #return render_template('input.html')
'''

@app.route('/data', methods = ['POST'])
def data_flask():
    print("data")
    exports = []
    results = {}
    if request.method == "POST" :
        print("[request.data] : ", request.data)
        #data = request.form["data"]
        data = request.data
        print("[data] : ")
        print(data)
        exports = export_url(data)
        for e in exports :
            results[e] = preprocessing(e)
            print(e, ": ", preprocessing(e))
        
        return results
    return "NONE"
    #return render_template('input.html')


@app.route("/post",methods=['POST'])

def post():
   url1 = request.form['input']
   result1 = preprocessing(url1)
    
#    msg = "%s 분석 결과 : %s"  %(url, result)
#    return msg
   return render_template('/result.html', url1=url1, result1=result1)



def export_url(data):
    urls = []
    #print(data)
    soup = BeautifulSoup(data, 'html.parser')
    links = soup.find_all("a")
    for a in links:
        href = a.attrs['href']
        print("여기여기 : ", href)
        urls.append(href)
    return urls


def preprocessing(test_url):
   url_data =  pd.DataFrame([test_url], columns=['url'])
   #Length of URL
   url_data['url_length'] = len(test_url)
   #Hostname Length
   url_data['hostname_length'] = len(urlparse(test_url).netloc)
   #Path Length
   url_data['path_length'] = len(urlparse(test_url).path)
   #First Directory Length


   url_data['fd_length'] = fd_length(test_url)
   url_data['count-'] = test_url.count('-')
   url_data['count@'] = test_url.count('@')
   url_data['count?'] = test_url.count('?')
   url_data['count%'] = test_url.count('%')
   url_data['count.'] = test_url.count('.')
   url_data['count='] = test_url.count('=')
   url_data['count-http'] = test_url.count('http')
   url_data['count-https'] = test_url.count('https')
   url_data['count-www'] = test_url.count('www')

   
   url_data['count-digits']= digit_count(test_url)
   url_data['count-letters']= letter_count(test_url)
   url_data['count_dir'] = no_of_dir(test_url)

   url_data['use_of_ip'] = having_ip_address(test_url)

   data = url_data.drop('url',axis=1)
   data = data.drop('url_length',axis=1)

   result = predict_model(data)
   return result



def fd_length(url):
    urlpath= urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0



def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits

def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters


def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')

#Use of IP or not in domain
def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        # print match.group()
        return -1
    else:
        # print 'No matching pattern found'
        return 1




def predict_model(data):
   output = (model.predict(data))
   if output > 0.5 :
      msg = "malicious"
   else : 
      msg = "non malicious"
      
   return msg



if __name__ == "__main__":
   app.run()