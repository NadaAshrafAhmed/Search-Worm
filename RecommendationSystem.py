from flask import Flask, request
from Integrating import get_recommendations
from Compyler import compile
from DataBase import add_user, user_exist

app = Flask(__name__)


@app.route('/start', methods=["POST"])
def start():
    # list of user history
    urls = list(set(request.get_json()['urls']))
    id = request.get_json()['ID']
    print(id)
    return get_recommendations(urls, id)


@app.route('/save_data', methods=["POST"])
def save_data():
    id = request.form.get('id')
    name = request.form.get('name')
    age = request.form.get('age')
    nation = request.form.get('nation')
    country = request.form.get('place')
    gender = request.form['gender']
    interests = request.form['interests']
    interests = interests.split('#')

    # NOTE! run this one time only and comment
    # DataBase.insert_interests()

    add_user(id, name, age, nation, country, gender, interests)

    return '<!doctype html> <html lang="en"> <head> <meta charset="utf-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link href="https://fonts.googleapis.com/css?family=Raleway:100,600" rel="stylesheet" type="text/css"> <title>Registration Complete</title> <style> html, body { background-color: #fff; color: #636b6f; font-family: "Raleway", sans-serif; font-weight: 100; height: 100vh; margin: 0; } .full-height { height: 100vh; } .flex-center { align-items: center; display: flex; justify-content: center; } .content { text-align: center; } .title { font-size: 84px; } .m-b-md { margin-bottom: 30px; } </style> </head> <body> <div class="flex-center position-ref full-height"> <div class="content"> <div class="title m-b-md"> Thank you for your patience </div> </div> </div> </body> </html>'


@app.route('/id_exist', methods=["POST"])
def id_exist():
    id = request.get_json()['ID']
    print(id)
    user_exist(id)
    # check database ..
    if (user_exist(id)):
        return ("true")
    return ("false")


@app.route('/get_html', methods=["POST"])
def get_html():
    url = request.get_json()['url']
    gen = compile(url, True, True, True, True, True, True, True)
    html = gen.decode("UTF-8")
    return html


if __name__ == '__main__':
    app.run(debug=True)
