import random
import requests as rq
from unidecode import unidecode
from flask import Flask, jsonify, request
from src.proximo_feriado import type_of_holidays, NextHoliday

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]

genre_of_movies = ["accion", "ciencia ficcion", "fantasia", "drama", "teatro"]
"""
Generos de pelicula aceptados por la api.
"""

base_uri = "http://localhost:5000/"


# Endpoint para buscar peliculas segun id, genero o texto
@app.route('/peliculas', methods=['GET'])
def buscar_peliculas():
    """
    Endpoint que devuelve una película, puede ser por
    `genero` o por `texto` que son ingresados por query string.
    """
    genero = request.args.get('genero', '').strip()
    texto = request.args.get('search')

    # Si se pasa un ID como parámetro numérico
    if request.args.get('id'):
        id_pelicula = int(request.args.get('id'))
        return obtener_pelicula(id_pelicula)

    # Filtrar por género
    if genero:
        try:
            genero = genero.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        genero = unidecode(genero.lower())
        peliculas_filtradas = []
        for pelicula in peliculas:
            if genero == unidecode(pelicula['genero'].lower()):
                peliculas_filtradas.append(pelicula)
        if len(peliculas_filtradas) > 0:
            return jsonify(peliculas_filtradas), 200
        return jsonify({"mensaje": "Películas por género no encontradas",
                        "codigo": 404}), 404

    # Filtrar por texto en título
    if texto:
        texto = texto.lower()
        peliculas_filtradas = []
        for pelicula in peliculas:
            if texto in pelicula["titulo"].lower():
                peliculas_filtradas.append(pelicula)
        if len(peliculas_filtradas) > 0:
            return jsonify(peliculas_filtradas), 200
        return jsonify({"mensaje": "Películas por título no encontradas",
                        "codigo": 404}), 404

    # Si no se pasa ningún parámetro, devuelve todas las películas
    return jsonify(peliculas), 200


# Endpoint para obtener peliculas segun su id
@app.route('/peliculas/<int:id>', methods=['GET'])
def obtener_pelicula(id):
    """
    Endpoint que obtiene una película por su `ID` y devuelve sus detalles
    """
    # Lógica para buscar la película por su ID y devolver sus detalles
    for pelicula in peliculas:
        if id == pelicula["id"]:
            return jsonify(pelicula), 200

    # Si no se encuentra ninguna película con ese ID
    return jsonify({"error": "Pelicula no encontrada", "codigo": 404}), 404


# Endpoint para agregar una nueva película
@app.route('/peliculas', methods=['POST'])
def agregar_pelicula():
    """
    Endpoint que permite agregar una película.

    Body: `{"titulo": "titulo", "genero": "genero"}`
    """
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    return jsonify(nueva_pelicula), 201


# Endpoint para actualizar una película
@app.route('/peliculas/<int:id>', methods=['PUT'])
def actualizar_pelicula(id):
    """
    Endpoint que actualiza una película existente por medio de su `ID`.
    """
    # Lógica para buscar la película por su ID y actualizar sus detalles"
    actualizada = obtener_pelicula_id(id)

    if actualizada:
        actualizada['titulo'] = request.json.get('titulo',
                                                 actualizada['titulo'])
        actualizada['genero'] = request.json.get('genero',
                                                 actualizada['genero'])
        return jsonify(actualizada), 200

    return jsonify({'error': 'Pelicula no encontrada'}), 404


# Endpoint para eliminar una película
@app.route('/peliculas/<int:id>', methods=['DELETE'])
def eliminar_pelicula(id):
    """
    Endpoint que permite eliminar una película existente por medio de su `ID`.
    """
    # Lógica para buscar la película por su ID y eliminarla
    for pelicula in peliculas:
        if id == pelicula["id"]:
            peliculas.remove(pelicula)
            return jsonify(
                {
                    "mensaje": "Pelicula eliminada exitosamente",
                    "codigo": 200
                }
            ), 200

    # Si no se encuentra ninguna película con ese ID
    return jsonify({"error": "Pelicula no encontrada", "codigo": 404}), 404


# Endpoint para obtener una película aleatoria
@app.route('/peliculas/random', methods=['GET'])
def pelicula_aleatoria():
    """
    Endpoint que devuelve una película aleatoria.
    """
    # Lógica para sugerir una película aleatoria
    if len(peliculas) > 0:
        index = random.randint(0, len(peliculas) - 1)
        return jsonify(peliculas[index]), 200

    # Si no hay peliculas
    return jsonify({'error': 'No hay peliculas para sugerirte alguna'}), 404


# Endpoint para obtener una película aleatoria por genero
@app.route('/peliculas/random/<string:genero>', methods=['GET'])
def pelicula_aleatoria_genero(genero):
    """
    Endpoint que devuelve una película aleatoria de un género solicitado.
    """
    # Lógica para sugerir una película aleatoria del género
    peliculas_genero = []

    for pelicula in peliculas:
        if unidecode(pelicula['genero'].lower()) == unidecode(genero.lower()):
            peliculas_genero.append(pelicula)

    if peliculas_genero:
        index = random.randint(0, len(peliculas_genero) - 1)
        return jsonify(peliculas_genero[index]), 200

    return jsonify({'error': 'Genero no encontrado'}), 404


def obtener_nuevo_id():
    """
    Genera un nuevo ID.
    """
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


@app.route('/feriados', methods=['GET'])
def feriados():
    """
    Endpoint que devuelve todos los feriados del año actual.
    """
    return NextHoliday().fetch_holidays()


@app.route('/feriado', methods=['GET'])
def feriado():
    """
    Endpoint que devuelve el proximo feriado de la fecha actual.
    """
    next_holiday = NextHoliday()
    all_holidays = next_holiday.fetch_holidays()
    next_holiday.set_next(all_holidays)
    return next_holiday.next_holiday_json()


@app.route('/feriado/<string:type_holiday>', methods=['GET'])
def proximo_feriado(type_holiday):
    """
    **Endpoint que devuelve el próximo feriado correspondiente
    al tipo de feriado solicitado, del año actual.**

    *Opcionalmente se puede ingresar un día y mes por query string.*

    **Query String**

    `?day=<int>&month=<int>`
    """

    day = request.args.get('day')
    month = request.args.get('month')

    if type_holiday not in type_of_holidays:
        return jsonify({
            "error": f"El tipo {type_holiday} no es valido. " +
            "Por favor ingrese un tipo válido."
        }), 400

    next_holiday = NextHoliday()
    all_holidays = next_holiday.fetch_holidays()
    next_holiday.set_next(all_holidays, type_holiday, day, month)
    holiday = next_holiday.next_holiday_json()

    if holiday[1] == 404:
        return jsonify(holiday[0]), 404
    else:
        return jsonify(holiday[0]), 200


@app.route('/feriado_pelicula', methods=['GET'])
def sugerir_pelicula_para_feriado():
    """
    Endpoint que sugiere películas de un género y un tipo de feriado
    solicitado.

    **Query String**

    `?type_holiday=<str>&movie_genre=<str>`

    *Opcionalmente se puede ingresar un día y mes por query string.*

    `?day=<int>&month=<int>`
    """
    type_holiday = request.args.get('type_holiday')
    if type_holiday:
        try:
            type_holiday = type_holiday.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        type_holiday = unidecode(type_holiday.lower())
    movie_genre = request.args.get('type_movie')
    if movie_genre:
        try:
            movie_genre = movie_genre.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        movie_genre = unidecode(movie_genre.lower())
    day = request.args.get('day')
    month = request.args.get('month')

    feriado = {}
    movies = {}

    if type_holiday not in type_of_holidays:
        return jsonify({
            "error": f"Tipo de feriado '{type_holiday}' no válido. " +
            "Intenta con un tipo válido."
        }), 400

    if movie_genre not in genre_of_movies:
        return jsonify({
            "error": f"Tipo de película '{movie_genre}' no válido. " +
            "Intenta con un tipo válido."
        }), 400

    try:
        feriado_response = rq.get(
            f"{base_uri}feriado/{type_holiday}?day={day}&month={month}")  # noqa
        # Lanzar una excepción si la respuesta es un error HTTP
        feriado_response.raise_for_status()
        feriado = feriado_response.json()
    except rq.exceptions.RequestException as e:
        return jsonify({
            "error": f"Error al obtener el feriado."
        }), 500

    try:
        peliculas_response = rq.get(
            f"{base_uri}peliculas?genero={movie_genre}")
        # Lanza excepción si la respuesta es un error HTTP
        peliculas_response.raise_for_status()
        movies = peliculas_response.json()
    except rq.exceptions.RequestException as e:
        if e.response.status_code not in [404]:
            return jsonify({
                "error": f"Error al obtener las películas."
            }), 500

    if len(movies) == 0:
        return jsonify({
            "feriado": feriado,
            "peliculas": f"No podemos sugerirte una pelicula de {movie_genre}"
        }), 200
    else:
        return jsonify({
            "feriado": feriado,
            "peliculas": movies
        }), 200


# Función para obtener una película por su ID
def obtener_pelicula_id(id):
    for pelicula in peliculas:
        if pelicula['id'] == id:
            return pelicula
    return None


if __name__ == '__main__':
    app.run(debug=True)
