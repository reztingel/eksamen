from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

API_URL = 'http://127.0.0.1:5001/api'

@app.route('/')
def index():
    # Hent alle bøker fra API-et
    response = requests.get(f'{API_URL}/boker')
    boker = response.json()
    return render_template('index.html', boker=boker)

@app.route('/bok/<int:nummer>')
def bok(nummer):
    # Hent detaljer om en spesifikk bok fra API-et
    response = requests.get(f'{API_URL}/bok/{nummer}')
    bok = response.json()
    return render_template('bok.html', bok=bok)

@app.route('/slettbok/<int:nummer>', methods=['POST'])
def slett_bok(nummer):
    # Slett en bok via API-et
    response = requests.delete(f'{API_URL}/slettbok/{nummer}')
    return response.json()

@app.route('/leggtilbok', methods=['POST'])
def legg_til_bok():
    # Legg til en ny bok via API-et
    data = request.json
    response = requests.post(f'{API_URL}/leggtilbok', json=data)
    return response.json()

@app.route('/filter', methods=['POST'])
def filter_boker():
    # Filtrer bøker basert på søketekst via API-et
    streng = request.form['streng']
    response = requests.get(f'{API_URL}/filter/{streng}')
    boker = response.json()
    return jsonify(boker)

@app.route('/sok_bok', methods=['POST'])
def sok_bok():
    # Søk etter en bok basert på ISBN via API-et
    isbn = request.form['isbn']
    response = requests.get(f'{API_URL}/bok?isbn={isbn}')
    bok = response.json()
    return jsonify(bok)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
