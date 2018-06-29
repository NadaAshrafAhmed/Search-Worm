
from flask import Flask, render_template, request, json

from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from Clustering import k_means

from TopicModelling import LDA , clean

from Integrating import get_recommendations

import compyler

import db


app = Flask(__name__)

def history1():
    return str([["a","b","c","d"],["e","f","g","h"],["i","j","k","l"],["m","n","o","p"]]).replace("'", '"')


@app.route('/history',methods=["POST"])
def history():

    print("here")

    # list of user history
    urls=list(set(request.get_json()['urls']))
    id = request.get_json()['ID']
    print(id)

    return get_recommendations(urls,id)


@app.route('/save_data',methods=["POST"])
def save_data():
    id = request.form.get('id')
    name=request.form.get('name')
    age = request.form.get( 'age' )
    nation=request.form.get('nation')
    print(id)

    db.add_user(id,name,age,nation)

    return "Thank you !"


@app.route('/id_exist',methods=["POST"])
def id_exist():

    id = request.get_json()['ID']
    print(id)
    db.user_exist(id)
    #check database ..
    if(db.user_exist(id)):
        return ("true")
    return ("false")


@app.route('/get_html', methods=["POST"])
def get_html():

    url = request.get_json()['url']
    gen = compyler.compile(url, True, True, True, True, True, True, True)
    html = gen.decode("UTF-8")

    return html

if __name__ == '__main__':
    app.run(debug=True)