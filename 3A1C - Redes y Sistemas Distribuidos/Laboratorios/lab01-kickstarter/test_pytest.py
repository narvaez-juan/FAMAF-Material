import requests
import pytest
import requests_mock


@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201,
               json={'id': 3, 'titulo': 'Pelicula de prueba',
                     'genero': 'Acción'})

        # Simulamos la respuesta para obtener una película específica
        m.get('http://localhost:5000/peliculas/1',
              json={'id': 1, 'titulo': 'Indiana Jones',
                    'genero': 'Acción'})
        m.get('http://localhost:5000/peliculas/2',
              json={'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'})
        m.get('http://localhost:5000/peliculas/4',
              status_code=404, json={'error': 'Pelicula no encontrada',
                                     'codigo': 404})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200,
              json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)

        # Simulamos la respuesta para eliminar una pelicula que no existe
        m.get('http://localhost:5000/peliculas/3', status_code=404,
              json={'codigo': 404})

        m.get('http://localhost:5000/feriado', status_code=200)

        motivo_p1 = "Paso a la Inmortalidad del "
        motivo_p2 = "General Jos\u00e9 de San Mart\u00edn"
        m.get(
            'http://localhost:5000/feriado/trasladable?day=18&month=6',
            status_code=200,
            json={
                "dia": 17,
                "fecha": "Domingo 17 de Agosto",
                "mes": 8,
                "motivo": motivo_p1 + motivo_p2,
                "tipo": "trasladable",
                "year": 2025
            }
        )

        m.get(
            'http://localhost:5000/feriado/inamovible?day=18&month=6',
            status_code=200,
            json={
                "dia": 20,
                "fecha": "Viernes 20 de Junio",
                "mes": 6,
                "motivo": "Paso a la Inmortalidad del General Manuel Belgrano",
                "tipo": "inamovible",
                "año": 2025
                }
            )

        m.get(
            'http://localhost:5000/feriado/nolaborable?day=1&month=1',
            status_code=404,
            json={
                "error": "No se ha encontrado un feriado del tipo solicitado."
                }
            )

        m.get(
            'http://localhost:5000/feriado/puente?day=1&month=1',
            status_code=404,
            json={
                "error": "No se ha encontrado un feriado del tipo solicitado."
            }
        )

        # Simulamos la respuesta para obtener una pelicula del genero Accion
        m.get(
            'http://localhost:5000/peliculas?genero=Acción',
            status_code=200,
            json=[
                {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
                {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
            ]
        )

        ''' Simulamos la respuesta para obtener una pelicula de un
        genero que no existe '''
        m.get('http://localhost:5000/peliculas?genero=GENERO_NOT_FOUND',
              status_code=404, json={'codigo': 404})

        ''' Simulamos la respuesta para obtener una pelicula con el texto
        Indiana en el titulo '''
        m.get(
            'http://localhost:5000/peliculas?search=Indiana',
            status_code=200,
            json=[
                {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
                {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
            ]
        )

        ''' Simulamos la respuesta para obtener una pelicula con un texto
        en su titulo que no existe '''
        m.get('http://localhost:5000/peliculas?search=WEIRD_RANDOM_TEXT',
              status_code=404, json={'codigo': 404})

        m.get('http://localhost:5000/peliculas/random/accion',
              status_code=200,
              json=[
                {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
                {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
              ])

        m.get('http://localhost:5000/peliculas/random/sevillana',
              status_code=404, json={'codigo': 404})

        yield m

# With Mocks #


def test_mock_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_mock_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas',
                             json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3


def test_mock_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'


def test_mock_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1',
                            json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'


def test_mock_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200


def test_mock_eliminar_pelicula_inexistente(mock_response):
    response = requests.get('http://localhost:5000/peliculas/3')
    assert response.json()['codigo'] == 404
    assert response.status_code == 404


def test_mock_pelicula_aleatoria_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/random/accion')
    assert response.status_code == 200
    assert response.json()[0]['genero'] == 'Acción'


def test_mock_spelicula_aleatoria_genero_no_listado(mock_response):
    response = requests.get(
        'http://localhost:5000/peliculas/random/sevillana')
    assert response.status_code == 404
    assert response.json()['codigo'] == 404

# Tests de obtener pelicula


def test_mock_obtener_detalle_pelicula_existente(mock_response):
    response = requests.get('http://localhost:5000/peliculas/2')
    pelicula = response.json()
    assert pelicula['id'] == 2
    assert pelicula['titulo'] == 'Star Wars'
    assert pelicula['genero'] == 'Acción'


def test_mock_obtener_detalle_pelicula_inexistente(mock_response):
    # Caso fallido: Película no encontrada
    response = requests.get('http://localhost:5000/peliculas/4')
    assert response.status_code == 404
    assert response.json()['error'] == 'Pelicula no encontrada'


def test_mock_peliculas_por_genero(mock_response):
    response = requests.get('http://localhost:5000/feriado')
    assert response.status_code == 200


def test_obtener_proximo_feriado_trasladable_con_fecha(mock_response):
    response = requests.get(
        'http://localhost:5000/feriado/trasladable?day=18&month=6'
        )
    motivo = 'Paso a la Inmortalidad del General José de San Martín'
    assert response.status_code == 200
    assert response.json()['dia'] == 17
    assert response.json()['fecha'] == 'Domingo 17 de Agosto'
    assert response.json()['mes'] == 8
    assert response.json()['motivo'] == motivo
    assert response.json()['tipo'] == 'trasladable'
    assert response.json()['año'] == 2025


def test_obtener_proximo_feriado_inamovible_con_fecha(mock_response):
    response = requests.get(
        'http://localhost:5000/feriado/inamovible?day=18&month=6'
        )
    motivo = 'Paso a la Inmortalidad del General Manuel Belgrano'
    assert response.status_code == 200
    assert response.json()['dia'] == 20
    assert response.json()['fecha'] == 'Viernes 20 de Junio'
    assert response.json()['mes'] == 6
    assert response.json()['motivo'] == motivo
    assert response.json()['tipo'] == 'inamovible'
    assert response.json()['año'] == 2025


def test_obtener_proximo_feriado_nolaborable_con_fecha(mock_response):
    response = requests.get(
        'http://localhost:5000/feriado/nolaborable?day=1&month=1'
        )
    assert response.status_code == 404
    not_found = 'No se ha encontrado un feriado del tipo solicitado.'
    assert response.json()['error'] == not_found


def test_obtener_proximo_feriado_puente_con_fecha(mock_response):
    response = requests.get(
        'http://localhost:5000/feriado/puente?day=1&month=1'
        )
    assert response.status_code == 404
    not_found = 'No se ha encontrado un feriado del tipo solicitado.'
    assert response.json()['error'] == not_found


def test_peliculas_por_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas?genero=Acción')
    assert response.status_code == 200


def test_mock_peliculas_por_genero_nonexistent(mock_response):
    response = requests.get(
        'http://localhost:5000/peliculas?genero=GENERO_NOT_FOUND'
        )
    print(response.json())
    assert response.status_code == 404
    assert response.json()['codigo'] == 404


def test_mock_peliculas_por_texto_en_titulo_nonexistent(mock_response):
    response = requests.get(
        'http://localhost:5000/peliculas?search=WEIRD_RANDOM_TEXT'
        )
    assert response.status_code == 404
    assert response.json()['codigo'] == 404


def test_mock_pelicula_aleatoria_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/random/accion')
    assert response.status_code == 200
    assert response.json()[0]['genero'] == 'Acción'


def test_mock_pelicula_aleatoria_genero_no_listado(mock_response):
    response = requests.get('http://localhost:5000/peliculas/random/sevillana')
    assert response.status_code == 404
    assert response.json()['codigo'] == 404


def test_mock_peliculas_por_texto_en_titulo(mock_response):
    response = requests.get(
        'http://localhost:5000/peliculas?search=Indiana')
    assert response.status_code == 200
    peliculas_seleccionadas = []
    for pelicula in response.json():
        if 'Indiana' in pelicula["titulo"]:
            peliculas_seleccionadas.append(pelicula)
    assert len(peliculas_seleccionadas) > 0


def test_mock_peliculas_por_texto_en_titulo_nonexistent(mock_response):
    response = requests.get(
        'http://localhost:5000/peliculas?search=WEIRD_RANDOM_TEXT')
    assert response.status_code == 404
    assert response.json()['codigo'] == 404


def test_peliculas_por_texto_en_titulo(mock_response):
    response = requests.get('http://localhost:5000/peliculas?search=Indiana')
    assert response.status_code == 200
    peliculas_seleccionadas = []
    for pelicula in response.json():
        if 'Indiana' in pelicula["titulo"]:
            peliculas_seleccionadas.append(pelicula)
    assert len(peliculas_seleccionadas) > 0


# Without Mocks #

# Peliculas #


def test_peliculas_por_genero_nonexistent():
    response = requests.get(
        'http://localhost:5000/peliculas?genero=GENERO_NOT_FOUND')
    print(response.json())
    assert response.status_code == 404
    assert response.json()['codigo'] == 404


def test_peliculas_por_texto_en_titulo():
    response = requests.get('http://localhost:5000/peliculas?search=Indiana')
    assert response.status_code == 200
    peliculas_seleccionadas = []
    for pelicula in response.json():
        if 'Indiana' in pelicula["titulo"]:
            peliculas_seleccionadas.append(pelicula)
    assert len(peliculas_seleccionadas) > 0


def test_peliculas_por_texto_en_titulo_nonexistent():
    response = requests.get(
        'http://localhost:5000/peliculas?search=WEIRD_RANDOM_TEXT')
    assert response.status_code == 404
    assert response.json()['codigo'] == 404


# Feriados #

def test_obtener_todos_los_feriado():
    response = requests.get('http://localhost:5000/feriado')
    assert response.status_code == 200


def test_obtener_proximo_feriado_trasladable_con_fecha():
    response = requests.get(
        'http://localhost:5000/feriado/trasladable?day=18&month=6')
    assert response.status_code == 200
    assert response.json()['dia'] == 17
    assert response.json()['fecha'] == 'Domingo 17 de Agosto'
    assert response.json()['mes'] == 8
    assert response.json()['motivo'] == 'Paso a la Inmortalidad del General José de San Martín'  # noqa
    assert response.json()['tipo'] == 'trasladable'
    assert response.json()['año'] == 2025


def test_obtener_proximo_feriado_inamovible_con_fecha():
    response = requests.get(
        'http://localhost:5000/feriado/inamovible?day=18&month=6')
    assert response.status_code == 200
    assert response.json()['dia'] == 20
    assert response.json()['fecha'] == 'Viernes 20 de Junio'
    assert response.json()['mes'] == 6
    assert response.json()['motivo'] == 'Paso a la Inmortalidad del General Manuel Belgrano'  # noqa
    assert response.json()['tipo'] == 'inamovible'
    assert response.json()['año'] == 2025


def test_obtener_proximo_feriado_nolaborable_con_fecha():
    response = requests.get(
        'http://localhost:5000/feriado/nolaborable?day=1&month=1')
    assert response.status_code == 404
    assert response.json()['error'] == 'No se ha encontrado un feriado del tipo solicitado.'  # noqa


def test_obtener_proximo_feriado_puente_con_fecha():
    response = requests.get(
        'http://localhost:5000/feriado/puente?day=1&month=1')
    assert response.status_code == 404
    assert response.json()['error'] == 'No se ha encontrado un feriado del tipo solicitado.'  # noqa

# Sugerir pelicula en feriado #


def test_sugerir_pelicula_en_feriado_inamovible_drama():
    response = requests.get(
        'http://localhost:5000/feriado_pelicula?type_holiday=inamovible&type_movie=Drama')  # noqa
    assert response.status_code == 200
    assert response.json()['peliculas'][0]['genero'] == "Drama"


def test_sugerir_pelicula_en_feriado_inamovible_drama():
    response = requests.get(
        'http://localhost:5000/feriado_pelicula?type_holiday=inamovible&type_movie=Drama')  # noqa
    assert response.status_code == 200
    assert response.json()['peliculas'][0]['genero'] == "Drama"


def test_sugerir_pelicula_en_feriado_inamovible_teatro():
    response = requests.get(
        'http://localhost:5000/feriado_pelicula?type_holiday=inamovible&type_movie=Teatro')  # noqa
    assert response.status_code == 200  # Diseño
    assert response.json()['peliculas'] == "No podemos sugerirte una pelicula de teatro"  # noqa


def test_sugerir_pelicula_en_feriado_inamovible_drama_con_fecha():
    response = requests.get(
        'http://localhost:5000/feriado_pelicula?type_holiday=inamovible&type_movie=Drama&day=18&month=6')  # noqa
    assert response.status_code == 200
    print(response.json()['feriado'])
    assert response.json()['feriado']['dia'] == 20
    assert response.json()['feriado']['fecha'] == 'Viernes 20 de Junio'
    assert response.json()['feriado']['mes'] == 6
    assert response.json()['feriado']['motivo'] == 'Paso a la Inmortalidad del General Manuel Belgrano'  # noqa
    assert response.json()['feriado']['tipo'] == 'inamovible'
    assert response.json()['feriado']['año'] == 2025
    assert response.json()['peliculas'][0]['genero'] == "Drama"
