from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    response = requests.get("http://127.0.0.1:5010/")
    if response.status_code == 500:
        return render_template(
            "error.html", error=response.json()["error"], status=response.status_code
        )
    return render_template("index.html", bøker=response.json())


@app.route("/book/<int:nummer>", methods=["GET"])
def book(nummer):
    if nummer == 0:
        nummer = request.args.get("nummer")
    if int(nummer) < 1 or int(nummer) > 51:
        return render_template(
            "error.html", error="Book nummer utenfor rekkevidden", status=404
        )
    response = requests.get("http://127.0.0.1:5010/book/" + str(nummer))
    if response.status_code == 500 or response.status_code == 404:
        return render_template(
            "error.html", error=response.json()["error"], status=response.status_code
        )
    return render_template("book.html", book=response.json())


@app.route("/barcode/<nummer>", methods=["GET"])
def barcode(nummer):
    path = "C:\\Users\\tobia\\Desktop\\eksamen\\client\\static\\barcode"
    barcode = os.path.join(path, f"{nummer}.png")
    print(barcode)
    return barcode


@app.route("/filter", methods=["GET"])
def filter():
    streng = request.args.get("streng")
    if not streng:
        return redirect("/")
    response = requests.get("http://127.0.0.1:5010/filter/" + streng)
    if response.status_code == 500:
        return render_template(
            "error.html", error=response.json()["error"], status=response.status_code
        )
    if response.status_code == 404:
        return render_template(
            "index.html", error=response.json()["error"], streng=streng
        )
    return render_template("index.html", bøker=response.json(), streng=streng)


@app.route("/slettbook/<nummer>", methods=["POST"])
def slettbook(nummer):
    response = requests.delete("http://127.0.0.1:5010/slettbook/" + nummer)
    if response.status_code == 500 or response.status_code == 404:
        return render_template(
            "error.html", error=response.json()["error"], status=response.status_code
        )
    return redirect("/")


@app.route("/leggtilbook", methods=["GET", "POST"])
def leggtilbook():
    if request.method == "GET":
        return render_template("leggtilbook.html")

    if request.method == "POST":
        tittel = request.form.get("tittel")
        forfatter = request.form.get("forfatter")
        isbn = request.form.get("isbn")
        nummer = request.form.get("nummer")
        if nummer == "":
            nummer = 0
        response = requests.post(
            "http://127.0.0.1:5010/leggtilbook",
            json={
                "tittel": tittel,
                "forfatter": forfatter,
                "isbn": isbn,
                "nummer": nummer,
            },
        )
        if response.status_code == 500 or response.status_code == 409:
            return render_template(
                "error.html",
                error=response.json()["error"],
                status=response.status_code,
            )
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)