# Laboratorio 1 - RySD 2025

[**Informe**](Informe.md) | [**Enunciado Laboratorio**](Lab1_enunciado_2025.pdf)


- [Laboratorio 1 - RySD 2025](#laboratorio-1---rysd-2025)
- [Integrantes](#integrantes)
- [Features (funcionalidades)](#features-funcionalidades)
  - [Recomendacion de pelicula en feriado](#recomendacion-de-pelicula-en-feriado)
- [Comandos para correr](#comandos-para-correr)
  - [Desactivar el entorno](#desactivar-el-entorno)
- [Curls](#curls)
    - [Actualizar pelicula](#actualizar-pelicula)
    - [Feriado](#feriado)
    - [Sugerir pelicula en feriado](#sugerir-pelicula-en-feriado)
- [Comandos para git](#comandos-para-git)
  - [Crear una branch a partir de la que estoy](#crear-una-branch-a-partir-de-la-que-estoy)
  - [Ver los cambios](#ver-los-cambios)
  - [Agregar un archivo](#agregar-un-archivo)
  - [Ver el historial de cambios](#ver-el-historial-de-cambios)
  - [Crear un commit en mi branch](#crear-un-commit-en-mi-branch)
  - [Modificar el mensaje del commit anterior](#modificar-el-mensaje-del-commit-anterior)
  - [Mandar (pushear) los cambios a mi branch](#mandar-pushear-los-cambios-a-mi-branch)
  - [Traer cambios de una branch a la que estoy](#traer-cambios-de-una-branch-a-la-que-estoy)
- [Descomprimir archivos](#descomprimir-archivos)
- [Documentacion](#documentacion)
- [Herramientas para utilizar](#herramientas-para-utilizar)
  - [Para realizar request con interfaz](#para-realizar-request-con-interfaz)

# Integrantes

* Dahlquist, Nicolás.
* Lucero, Carolina.
* Narvaez, Juan.
* Vispo, Valentina Solange.

# Features (funcionalidades)

`main.py`
* [x] `obtener_pelicula`: Buscar la película por su `ID` y devolver sus detalles (`GET`).
* [x] `actualizar_pelicula`: Buscar la película por su `ID` y actualizar sus detalles (`PUT`).
* [x] `eliminar_pelicula`: Buscar la película por su `ID` y eliminarla (`DELETE`).
* [x] `buscar_peliculas`: Buscar peliculas segun el género o si tienen cierto texto en sus títulos. (`GET`).
* [x] `pelicula_aleatoria`: Sugerir una película aleatoria (`GET`).
* [x] `pelicula_aleatoria_genero`: Sugerir una película aleatoria según género (`GET`).

**API Feriados**
* [x] Modifica el código para que agregar la opción de buscar feriados por tipo:
    ```bash
    inamovible | trasladable | nolaborable | puente
    ```
* [x] Obtener la próxima fecha de feriado y recomendar una película que se ajuste al género solicitado para ese día. (Leer más)

`test.py` y `test_pytest.py`
* [x] Agregar test para las funcionalidades solicitadas
  * [x] `GET movie`
  * [x] `POST movie`
  * [x] `PUT movie`
  * [x] `DELETE movie`
  * [x] `GET /random`
  * [x] `GET /random/<genero:string>`
  * [x] `GET /feriados`
  * [x] `GET /feriado`
  * [x] `GET /feriado/trasladable/?day=<int>&month=<int>`
  * [x] `GET /feriado/inamovible/?day=<int>&month=<int>`
  * [x] `GET /feriado/nolaborable/?day=<int>&month=<int>`
  * [x] `GET /feriado/puente/?day=<int>&month=<int>`

## Recomendacion de pelicula en feriado

El comportamiento debería ser el siguiente:
Pregunta en lenguaje humano “Sugerime una película de DRAMA para ver el próximo feriado” Respuesta en lenguaje humano: “El próximo feriado es el xxxx con motivo yyyy , Te sugiero ver la pelicula de DRAMA <titulo de pelicula>  Obviamente no tienen que entregar este texto, el ejemplo es solo de comportamiento, deberán hacer las consultas usando las url de la api y programar las respuestas en formato json con los campos correspondientes.

# Comandos para correr

```bash
python3 -m venv .venv
```

2. Activamos el entorno

```bash
source .venv/bin/activate
```

3. Instalamos las dependencias (se hace una sola vez)

```bash
pip install -r requirements.txt
```

4. Ejecutar el programa

```bash
python3 main.py
```

Output:

```bash
┌──(.venv)─(kali㉿kali)-[~/api-kickstarter]
└─$ python main.py
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
127.0.0.1 - - [19/Mar/2025 21:30:19] "GET /peliculas HTTP/1.1" 200 -
```

Y en otra consola, o en Postman, ejecutan una curl:

```bash
curl http://localhost:5000/peliculas
```

Output:

```bash
[{"genero":"Acci\u00f3n","id":1,"titulo":"Indiana Jones"},{"genero":"Acci\u00f3n","id":2,"titulo":"Star Wars"},{"genero":"Ciencia ficci\u00f3n","id":3,"titulo":"Interstellar"},{"genero":"Aventura","id":4,"titulo":"Jurassic Park"},{"genero":"Acci\u00f3n","id":5,"titulo":"The Avengers"},{"genero":"Ciencia ficci\u00f3n","id":6,"titulo":"Back to the Future"},{"genero":"Fantas\u00eda","id":7,"titulo":"The Lord of the Rings"},{"genero":"Acci\u00f3n","id":8,"titulo":"The Dark Knight"},{"genero":"Ciencia ficci\u00f3n","id":9,"titulo":"Inception"},{"genero":"Drama","id":10,"titulo":"The Shawshank Redemption"},{"genero":"Crimen","id":11,"titulo":"Pulp Fiction"},{"genero":"Drama","id":12,"titulo":"Fight Club"}]
```

Levantarlo con flask:

```bash
flask --app main run --debug
```

Output:

```bash
└─$ flask --app main run --debug
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 335-015-848
```

1. Correr los test

```bash
python3 -m doctest test.py
```

```bash
pytest test_pytest.py -v
```

![](./assets/pytest%20test_pytest.png)

```bash
pytest test_pytest_main.py -v
```

![](./assets/pytest%20test_pytest_main.png)

```bash
pytest
```

## Desactivar el entorno

```bash
deactivate
```
# Curls

### Actualizar pelicula

```bash
curl -X PUT http://localhost:5000/peliculas/2 -H "Content-Type: application/json"
-d '{
    "titulo": "Nueva pelicula",
    "genero": "Nuevo genero"
    }'

```

```bash
curl -X PUT http://localhost:5000/peliculas/2 -H "Content-Type: application/json"
-d '{
    "titulo": "otro titulo"
    }'

```

```bash
curl -X PUT http://localhost:5000/peliculas/2 -H "Content-Type: application/json"
-d '{
    "genero": "otro genero"
    }'

```

### Feriado

```bash
curl --location 'http://localhost:5000/feriados' \
--header 'Content-Type: application/json'
```

```bash
curl --location 'http://localhost:5000/feriado' \
--header 'Content-Type: application/json'
```

```bash
curl --location --request GET 'http://localhost:5000/feriado/inamovible' \
--header 'Content-Type: application/json'
```

```bash
curl --location --request GET 'http://localhost:5000/feriado/trasladable' \
--header 'Content-Type: application/json'
```

```bash
curl --location --request GET 'http://localhost:5000/feriado/nolaborable' \
--header 'Content-Type: application/json'
```

```bash
curl --location --request GET 'http://localhost:5000/feriado/puente' \
--header 'Content-Type: application/json'
```

### Sugerir pelicula en feriado

```bash
curl --location 'http://localhost:5000/feriado_pelicula?type_holiday=inamovible&type_movie=Drama' \
--header 'Content-Type: application/json'
```

# Comandos para git

## Crear una branch a partir de la que estoy

```bash
git checkout -b <nombre_branch>
```

## Ver los cambios

```bash
git status
```

## Agregar un archivo

```bash
git add <file>
```

## Ver el historial de cambios

```bash
git log
```

## Crear un commit en mi branch

```bash
git commit -m "Texto del commit"
```

## Modificar el mensaje del commit anterior

```bash
git commit --amend "Mensaje nuevo del commit"
```

## Mandar (pushear) los cambios a mi branch

> Es necesario tener `commits` para subir cambios

```bash
git push origin
```

o

```bash
git push origin <mi_branch>
```

## Traer cambios de una branch a la que estoy

> origin es para indicarle "donde estoy"

```bash
git pull origin <branch_donde_traigo_los_cambios>
```

# Descomprimir archivos

**Descomprimir .tar.gz**

```bash
tar -xvzf file.tar.gz
```

**Descomprimir .zip**

```bash
unzip file.zip
```

# Documentacion

* [API de Feriados No Laborables Argentina](https://pjnovas.gitbooks.io/no-laborables/content/)

# Herramientas para utilizar

## Para realizar request con interfaz

> Permite guardar las curls y compartirlas de manera rapida y simple.

* [Postman](https://www.postman.com/) - Recomendado por la catedra
* [Insomnia](https://insomnia.rest/download)
