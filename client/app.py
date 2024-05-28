from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)








@app.route('/')
def index():
    response = requests.get('http://192.168.4.64/')
    return render_template('index.html', bøker=response.json())


@app.route('/book', methods=["GET"])
def book():
    nummer = request.args.get("nummer")
    print(nummer)
    response = request.get("http://192.168.4.64/book/" + str(nummer))
    print(response.json())
    return render_template("book.html", book=response.json())


@app.route('/barcode/<nummer>', methods=["GET"])
def barcode(nummer):
    path = "C:\\Users\\tobia\\Desktop\\eksamen\\bibliotek\\static\\barcode"
    barcode = os.path.join(path, f"{nummer}.png")
    print(barcode)
    return barcode



@app.route('/filter', methods=['GET'])
def filter():
    streng = request.args.get('streng')
    response = requests.get("http://192.168.4.64:/filter/" + streng)
    return render_template("index.html", bøker=response.json(), streng=streng)



@app.route('/slettbook/<nummer>', methods=['POST'])
def slettbook(nummer):
    request.delete("http://192.168.4.64:/slettbook/" + nummer)
    return redirect("/")
    

@app.route('/leggtilbook', methods=['GET','POST'])
def leggtilbook():
    if request.method == "GET":
        return render_template("legg_til.html")
    if request.method == "POST":
        tittel = request.form.get("tittel")
        forfatter = request.form.get("forfatter")
        isbn = request.form.get("isbn")
        nummer = request.form.get("nummer")
        response = request.post("http://192.168.4.64:/leggtilbook",
            json={
                "tittel": tittel,
                "forfatter": forfatter,
                "isbn": isbn,
                "nummer": nummer,
           }
    )
    print(response.status_code)
    return redirect("/")
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
