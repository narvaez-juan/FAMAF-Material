import requests

# Obtener todas las películas
print("Test: Obtener detalles de todas las películas")
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, "
          f"Título: {pelicula['titulo']}, "
          f"Género: {pelicula['genero']}")
print()

# Agregar una nueva película
print("Test: Agregar una película")
nueva_pelicula = {
    'titulo': 'Pelicula de prueba de agregar_peliculas',
    'genero': 'Test'
}
response = requests.post(
    'http://localhost:5000/peliculas',
    json=nueva_pelicula
)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, "
          f"Título: {pelicula_agregada['titulo']}, "
          f"Género: {pelicula_agregada['genero']}")
    # Guardo el dato de la nueva pelicula para que
    # si este test se hace muchas veces no colapse
    id_pelicula_agregada = pelicula_agregada['id']
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
print("Test: Obtener detalles de una película específica")
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, "
          f"Título: {pelicula['titulo']}, "
          f"Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
print("Test: Actualizar los detalles de una película")
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(
    f'http://localhost:5000/peliculas/{id_pelicula}',
    json=datos_actualizados
)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, "
          f"Título: {pelicula_actualizada['titulo']}, "
          f"Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Actualizar solo el título de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título'
}
response = requests.put(
    f'http://localhost:5000/peliculas/{id_pelicula}',
    json=datos_actualizados
)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada, solo titulo:")
    print(f"ID: {pelicula_actualizada['id']}, "
          f"Título: {pelicula_actualizada['titulo']}, "
          f"Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Actualizar solo el género de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'genero': 'Terror'
}
response = requests.put(
    f'http://localhost:5000/peliculas/{id_pelicula}',
    json=datos_actualizados
)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada, solo genero:")
    print(f"ID: {pelicula_actualizada['id']}, "
          f"Título: {pelicula_actualizada['titulo']}, "
          f"Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

id_pelicula = 200  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nueva pelicula',
    'genero': 'Terror'
}
response = requests.put(
    f'http://localhost:5000/peliculas/{id_pelicula}',
    json=datos_actualizados
)
if response.status_code == 404:
    error = response.json()
    print("Pelicula actualizada,id no encontrado: Ok")
else:
    print("Pelicula actualizad id no encontrado: Fail")
print()

# Eliminar una película
print("Test: Eliminar una pelicula")
nueva_pelicula = {
    'titulo': 'Pelicula de prueba para eliminacion',
    'genero': 'Romance'
}
response = requests.post(
    'http://localhost:5000/peliculas',
    json=nueva_pelicula
)
# Mostrar que se agregó una película para el test
if response.status_code == 201:
    pelicula = response.json()
    print(f"Se agregó la película: "
          f"ID: {pelicula['id']}, "
          f"Título: {pelicula['titulo']}, "
          f"Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")

if response.status_code == 201:
    pelicula_agregada = response.json()
    print(response.json())
    response = requests.delete(
        f'http://localhost:5000/peliculas/{pelicula_agregada['id']}'
    )
    if response.status_code == 200:
        print(f"Se eliminó la película: "
              f"ID: {pelicula['id']}, "
              f"Título: {pelicula['titulo']}, "
              f"Género: {pelicula['genero']} (caso esperado)")
    else:
        print("Error al eliminar la película.")
else:
    print("Error al agregar una película para testear eliminacion.")
print()

# Consultar una película luego de ser eliminarla
print("Test: Consultar una pelicula luego de ser eliminada")
nueva_pelicula = {
    'titulo': 'Pelicula de prueba consulta post eliminacion',
    'genero': 'Terror'
}
response = requests.post(
    'http://localhost:5000/peliculas',
    json=nueva_pelicula
)
# Mostrar que se agregó una película para el test
if response.status_code == 201:
    pelicula = response.json()
    print(f"Se agregó la película: "
          f"ID: {pelicula['id']}, "
          f"Título: {pelicula['titulo']}, "
          f"Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")

if response.status_code == 201:
    pelicula_agregada = response.json()
    response = requests.delete(
        f'http://localhost:5000/peliculas/{pelicula_agregada['id']}'
    )
    id_peli_agregada = pelicula_agregada['id']
    if response.status_code == 200:
        response = requests.get(
            f'http://localhost:5000/peliculas/{id_peli_agregada}'
        )
        if response.status_code == 404:
            print(f"Se eliminó la película: "
                  f"ID: {pelicula['id']}, "
                  f"Título: {pelicula['titulo']}, "
                  f"Género: {pelicula['genero']}")
            print(f"No se encontró la Película: ID: {pelicula['id']} "
                  "por su previa eliminación (caso esperado).")
        else:
            print("Error al acceder a una película eliminada.")
else:
    print("Error al agregar una película para testear "
          "consulta post eliminacion.")
print()

# Tests para obtener pelicula
print("Test: Obtener varias peliculas")


# Probar con un ID inexistente
id_pelicula = 999+id_pelicula_agregada
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 404:
    print(f"La película {999+id_pelicula_agregada} no fue "
          "encontrada (caso esperado).")
else:
    print("Error: Se esperaba un error 404.")

# Probar con un ID eliminado
id_pelicula = id_pelicula_agregada+1
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 404:
    print(f"La película {id_pelicula_agregada+1} no fue encontrada "
          "por eliminarse antes (caso esperado).")
else:
    print("Error: Se esperaba un error 404.")

# Probar con un ID 2 luego de eliminar al ID 1
id_pelicula = id_pelicula_agregada-11
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print(f"La película {id_pelicula_agregada-11} "
          "fue encontrada (caso esperado).")
else:
    print("Error: Se esperaba encontrarla.")

# Probar con un ID afuera del rango
id_pelicula = 14432142314432114312413243421+id_pelicula_agregada
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 404:
    print(f"La película {14432142314432114312413243421+id_pelicula_agregada} "
          "no fue encontrada (caso esperado).")
else:
    print("Error: Se esperaba un error 404.")

# Probar con el ID 0
id_pelicula = 0
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 404:
    print("La película 0 no fue encontrada (caso esperado).")
else:
    print("Error: Se esperaba un error 404.")

# Probar con un ID 13 luego de agregar esta pelicula
id_pelicula = id_pelicula_agregada
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print(f"La película {id_pelicula_agregada} "
          f"fue encontrada (caso esperado).")
else:
    print("Error: Se esperaba encontrarla.")

# Obtener detalles de peliculas por genero
print("Test: Obtener peliculas de un genero que si tenemos en nuestra lista")
genero = 'Acción'
nueva_pelicula = {
    'titulo': 'Pelicula de prueba busqueda de peliculas por genero',
    'genero': genero
}
response = requests.post(
    'http://localhost:5000/peliculas',
    json=nueva_pelicula
)
print("Respuesta POST:", response.status_code, response.text)
if response.status_code == 201:
    pelicula_agregada = response.json()
    response = requests.get(
        f'http://localhost:5000/peliculas?genero={genero}'
    )
    peliculas = response.json()
    print(f"Películas seleccionadas por género: {genero}")
    if response.status_code == 404:
        print(f"Películas de género {genero} no encontrados")
    else:
        for pelicula in peliculas:
            print(f"ID: {pelicula['id']}, "
                  f"Título: {pelicula['titulo']}, "
                  f"Género: {pelicula['genero']}")
        response = requests.delete(
            f'http://localhost:5000/peliculas/{pelicula_agregada['id']}'
        )
else:
    print("Error al agregar una película para testear peliculas por genero.")
print()

# Obtener detalles de peliculas por genero inexistente
print("Test: Obtener peliculas de un genero inexistente")
genero = 'GENERO_NOT_FOUND'
response = requests.get(f'http://localhost:5000/peliculas?genero={genero}')
peliculas = response.json()
print(f"Películas seleccionadas por género: {genero}")
if response.status_code == 404:
    print(f"Películas de género {genero} no encontrados")
else:
    for pelicula in peliculas:
        print(f"ID: {pelicula['id']}, "
              f"Título: {pelicula['titulo']}, "
              f"Género: {pelicula['genero']}")
print()

# Obtener detalles de peliculas que contengan cierto texto en sus titulos
print("Test: Peliculas con la palabra 'The' en sus titulos")
texto = 'The'
titulo = 'The film that contains "The" in his title for test porpuses only'
nueva_pelicula = {
    'titulo': titulo,
    'genero': 'Test'
}
response = requests.post(
    'http://localhost:5000/peliculas',
    json=nueva_pelicula
)
if response.status_code == 201:
    pelicula_agregada = response.json()
    response = requests.get(f'http://localhost:5000/peliculas?search={texto}')
    peliculas = response.json()
    print(f"Películas seleccionadas con el texto {texto} en sus títulos: ")
    if response.status_code == 404:
        print(f"Películas que contengan {texto} "
              "en sus títulos no encontrados")
    else:
        for pelicula in peliculas:
            print(f"ID: {pelicula['id']}, "
                  f"Título: {pelicula['titulo']}, "
                  f"Género: {pelicula['genero']}")
        response = requests.delete(
            f'http://localhost:5000/peliculas/{pelicula_agregada['id']}'
        )
else:
    print("Error al agregar una película para testear peliculas por genero.")
print()

# Obtener detalles de peliculas que en sus titulos tengan un texto imposible
print("Test: Peliculas que contengan en sus títulos un texto imposible")
texto = 'test text: abcdefghijklmñopqrstuv'
response = requests.get(f'http://localhost:5000/peliculas?search={texto}')
peliculas = response.json()
print(f"Películas seleccionadas con el texto {texto} en sus títulos: ")
if response.status_code == 404:
    print(f"Películas que contengan el texto "
          f"{texto} en sus títulos no encontrados")
else:
    for pelicula in peliculas:
        print(f"ID: {pelicula['id']}, "
              f"Título: {pelicula['titulo']}, "
              f"Género: {pelicula['genero']}")
print()

# Sugerir una película aleatoria de un género específico
genero = 'ciencia ficcion'  # Género de la película a sugerir
print(f"Buscar genero: {genero}")
response = requests.get(f'http://localhost:5000/peliculas/random/{genero}')
if response.status_code == 200:
    pelicula_sugerida = response.json()
    print("Película sugerida:")
    print(f"ID: {pelicula_sugerida['id']}, ",
          f"Título: {pelicula_sugerida['titulo']}, ",
          f"Género: {pelicula_sugerida['genero']}")
else:
    print("Error al obtener la película sugerida.")
print()

genero = 'No existe'  # Género de la película a sugerir
print(f"Buscar genero: {genero}")
response = requests.get(f'http://localhost:5000/peliculas/random/{genero}')
if response.status_code == 404:
    print(response.json())
    print("OK")
else:
    print("FAIL")
print()

# Feriado

print("######### API Feriados #########")

feriado_output = {
    "dia": 17,
    "fecha": "Martes 17 de Junio",
    "mes": 6,
    "motivo": "Paso a la Inmortalidad del Gral. Don Martín Güemes",
    "tipo": "trasladable",
    "year": 2025
}

print("Test: Consultar proximo feriado trasladable para el 18/06/2025")
try:
    response = requests.get(
        'http://localhost:5000/feriado/trasladable?day=18&month=6',
        json=feriado_output
    )
    if response.status_code == 200:
        print(f"Respuesta esperada correcta. Response: {response.json()}")
    else:
        print(f"Error al realizar la consulta. "
              f"Status_code: {response.status_code}")
except Exception as e:
    print(f"Excepcion: {e}")

print("\nTest: Consultar proximo feriado inamovible para el 18/06/2025")

feariado_output = {
  "dia": 20,
  "fecha": "Viernes 20 de Junio",
  "mes": 6,
  "motivo": "Paso a la Inmortalidad del General Manuel Belgrano",
  "tipo": "inamovible",
  "year": 2025
}

try:
    response = requests.get(
        'http://localhost:5000/feriado/inamovible?day=18&month=6',
        json=feriado_output
    )
    if response.status_code == 200:
        print(f"Respuesta esperada correcta. Response: {response.json()}")
    else:
        print(f"Error al realizar la consulta. "
              f"Status_code: {response.status_code}")
except Exception as e:
    print(f"Excepcion: {e}")

print("\nTest: Consultar proximo feriado no laborable para el 18/06/2025")

feariado_output = {
  "error": "No se ha encontrado un feriado del tipo solicitado."
}

try:
    response = requests.get(
        'http://localhost:5000/feriado/nolaborable?day=1&month=1',
        json=feriado_output
    )
    if response.status_code == 404:
        print(f"Respuesta esperada correcta. Response: {response.json()}")
    else:
        print(f"Error al realizar la consulta. "
              f"Status_code: {response.status_code}")
except Exception as e:
    print(f"Excepcion: {e}")

print("\nTest: Consultar proximo feriado puente para el 18/06/2025")

try:
    response = requests.get(
        'http://localhost:5000/feriado/puente?day=1&month=1',
        json=feriado_output
    )
    if response.status_code == 404:
        print(f"Respuesta esperada correcta. "
              f"Response: {response.json()}")
    else:
        print(
            f"Error al realizar la consulta. "
            f"Status_code: {response.status_code}"
        )
except Exception as e:
    print(f"Excepcion: {e}")

print("\nTest: Consultar sugerir pelicula de drama para feriado inamovible")

feriado_output = {
  "feriado": {
    "a\u00f1o": 2025,
    "dia": 2,
    "fecha": "Mi\u00e9rcoles 2 de Abril",
    "mes": 4,
    "motivo": "D\u00eda del Veterano y de los Ca\u00eddos en la Guerra de Malvinas",  # noqa
    "tipo": "inamovible"
  },
  "peliculas": [
    {
      "genero": "Drama",
      "id": 10,
      "titulo": "The Shawshank Redemption"
    },
    {
      "genero": "Drama",
      "id": 12,
      "titulo": "Fight Club"
    }
  ]
}

try:
    response = requests.get(
        'http://localhost:5000/feriado_pelicula?type_holiday=inamovible&type_movie=Drama',  # noqa
        json=feriado_output)
    if response.status_code == 200:
        print(f"Respuesta esperada correcta.")
    else:
        print(f"Error al realizar la consulta.")
except Exception as e:
    print(f"Excepcion: {e}")

print("\nTest: Consultar sugerir pelicula de accion para feriado inamovible")

feriado_output = {
  "feriado": {
    "a\u00f1o": 2025,
    "dia": 20,
    "fecha": "Viernes 20 de Junio",
    "mes": 6,
    "motivo": "Paso a la Inmortalidad del General Manuel Belgrano",
    "tipo": "inamovible"
  },
  "peliculas": [
    {
      "genero": "Acci\u00f3n",
      "id": 1,
      "titulo": "Indiana Jones"
    },
    {
      "genero": "Acci\u00f3n",
      "id": 2,
      "titulo": "Star Wars"
    },
    {
      "genero": "Acci\u00f3n",
      "id": 5,
      "titulo": "The Avengers"
    },
    {
      "genero": "Acci\u00f3n",
      "id": 8,
      "titulo": "The Dark Knight"
    }
  ]
}


try:
    response = requests.get(
        'http://localhost:5000/feriado_pelicula?type_holiday=inamovible&type_movie=ACCIÓN&day=18&month=6',  # noqa
        json=feriado_output)
    if response.status_code == 200:
        print(f"Respuesta esperada correcta.")
    else:
        print(f"Error al realizar la consulta.")
except Exception as e:
    print(f"Excepcion: {e}")


print("\nTest: Consultar sugerir pelicula de teatro para feriado inamovible")  # noqa

feriado_output = {
  "feriado": {
    "a\u00f1o": 2025,
    "dia": 20,
    "fecha": "Viernes 20 de Junio",
    "mes": 6,
    "motivo": "Paso a la Inmortalidad del General Manuel Belgrano",
    "tipo": "inamovible"
  },
  "peliculas": [
    {
      "genero": "Acci\u00f3n",
      "id": 1,
      "titulo": "Indiana Jones"
    },
    {
      "genero": "Acci\u00f3n",
      "id": 2,
      "titulo": "Star Wars"
    },
    {
      "genero": "Acci\u00f3n",
      "id": 5,
      "titulo": "The Avengers"
    },
    {
      "genero": "Acci\u00f3n",
      "id": 8,
      "titulo": "The Dark Knight"
    }
  ]
}


try:
    response = requests.get(
        'http://localhost:5000/feriado_pelicula?type_holiday=inamovible&type_movie=teatro&day=18&month=6',  # noqa
        json=feriado_output)
    if response.status_code == 200:
        print(f"Respuesta esperada correcta.")
    else:
        print(
            f"Error al realizar la consulta. Status_code: {response.status_code}")  # noqa
except Exception as e:
    print(f"Excepcion: {e}")
