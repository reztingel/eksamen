from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/database.db'



API_URL = 'http://127.0.0.1:5001/api'




@app.route('/')
def index():
    return redirect(url_for("get_books"))
    

@app.route('/get_books')
def get_books():
    response = requests.get('http://127.0.0.1:5001/')
    return render_template('index.html', bøker=response.json())


@app.route('/book/<int:nummer>')
def get_book(nummer):
    try:
        response = requests.get(f'{API_URL}/book/{nummer}')
        if response.status_code == 200:
            book = response.json()
            return render_template('book.html', book=book)
        else:
            return render_template('book.html', error="Error fetching book details")
    except requests.exceptions.ConnectionError:
        return render_template('book.html', error="Could not connect to the backend server")



# Adjust route methods and error handling
@app.route('/filter', methods=['GET'])
def filter_boker():
    # Filtrer bøker basert på søketekst via API-et
    streng = request.args.get('streng')
    response = requests.get(f'{API_URL}/filter/{streng}')
    if response.status_code == 200:
        boker = response.json()
        return jsonify(boker)
    else:
        return jsonify({'message': 'Error filtering books'}), 500

@app.route('/sok_bok', methods=['GET'])
def sok_bok():
    # Søk etter en bok basert på ISBN via API-et
    isbn = request.args.get('isbn')
    response = requests.get(f'{API_URL}/bok?isbn={isbn}')
    if response.status_code == 200:
        bok = response.json()
        return jsonify(bok)
    else:
        return jsonify({'message': 'Error searching for book'}), 500

# Redirect after actions
@app.route('/slettbok/<int:nummer>', methods=['POST'])
def slett_bok(nummer):
    # Slett en bok via API-et
    response = requests.delete(f'{API_URL}/slettbok/{nummer}')
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return jsonify({'message': 'Error deleting book'}), 500

@app.route('/leggtilbok', methods=['POST'])
def legg_til_bok():
    # Legg til en ny bok via API-et
    data = request.form
    response = requests.post(f'{API_URL}/leggtilbok', data=data)
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return jsonify({'message': 'Error adding book'}), 500




if __name__ == '__main__':
    app.run(debug=True, port=5000)
