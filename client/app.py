from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

API_URL = 'http://127.0.0.1:5001'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bok/<int:nummer>')
def bok(nummer):
    # Hent bokdetaljer
    response = requests.get(f'{API_URL}/api/bok/{nummer}')
    bok = response.json()
    return render_template('bok.html', bok=bok)


@app.route('/filter/<string:streng>', methods=['GET'])
def filter_boker(streng):
    # Filtrer bøker etter tittel eller forfatter
    response = requests.get(f'{API_URL}/api/filter/{streng}')
    boker = response.json()
    return jsonify(boker)


@app.route('/slettbok/<int:nummer>', methods=['POST'])
def slett_bok(nummer):
    # Slett bok
    response = requests.delete(f'{API_URL}/api/slettbok/{nummer}')
    return response.json()


@app.route('/leggtilbok', methods=['POST'])
def legg_til_bok():
    # Legg til ny bok
    data = request.json
    response = requests.post(f'{API_URL}/api/leggtilbok', json=data)
    return response.json()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
