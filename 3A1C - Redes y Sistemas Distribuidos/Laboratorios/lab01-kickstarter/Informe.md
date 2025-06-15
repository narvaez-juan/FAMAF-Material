# Informe de Laboratorio 1: Desarrollo de una API - RySD 2025

- [Informe de Laboratorio 1: Desarrollo de una API - RySD 2025](#informe-de-laboratorio-1-desarrollo-de-una-api---rysd-2025)
- [Integrantes](#integrantes)
- [Objetivos](#objetivos)
- [Features (funcionalidades)](#features-funcionalidades)
- [Decisiones de diseño e implementacion](#decisiones-de-diseño-e-implementacion)
  - [Endpoints de películas `main.py`](#endpoints-de-películas-mainpy)
  - [API de feriados](#api-de-feriados)
- [Test de las funciones implementadas](#test-de-las-funciones-implementadas)
- [Nuestra manera de trabajar](#nuestra-manera-de-trabajar)


# Integrantes

- Dahlquist, Nicolás.
- Lucero, Carolina.
- Narvaez, Juan.
- Vispo, Valentina Solange.

# Objetivos

* Utilizar y diseñar Apis, que corresponden a la programación en la capa de aplicación de redes según el modelo OSI de redes.
* Incorporar fluidez y buenos hábitos en la programación con python.
* Familiarizarse con herramientas propias de la industria (git, python, flask, postman, curl).

# Features (funcionalidades)

`main.py`

* `obtener_pelicula`: Buscar la película por su `ID` y devolver sus detalles (`GET`).
* `actualizar_pelicula`: Buscar la película por su `ID` y actualizar sus detalles (`PUT`).
* `eliminar_pelicula`: Buscar la película por su `ID` y eliminarla (`DELETE`).
* Devolver el listado de películas de un género específico (`GET`).
* Buscar de películas, devolviendo la lista de películas que tengan determinado string en el título (`GET`).
* `buscar_peliculas`: Buscar las películas segun su género o si contiene cierto texto en sus títulos (`GET`).
* `pelicula aleatoria`: Sugerir una película aleatoria (`GET`).
* `pelicula_aleatoria_genero`: Sugerir una película aleatoria según género (`GET`).
* `feriados`: Devolver todos los feriados del año actual. (`GET`)
* `feriado`: Devolver el próximo feriado respecto a la fecha actual. (`GET`)
* `/feriado/<string>?day=<int>&month=<int>`: Devolver el próximo feriado de un tipo en particular ('inamovible', 'nolaborable', 'puente', 'trasladable') y opcionalmente se puede agregar como query string `day` y `month` para realizar un filtrado sobre esas fechas. (`GET`)
* `/feriado/feriado_pelicula?type_holiday=<string>&type_movie=<string>`: Devolver una sugerencia de que pelicula del genero solicitar ver en el proximo feriado del tipo solicitado. (`GET`)

# Decisiones de diseño e implementacion

## Endpoints de películas `main.py`

* `obtener pelicula`: Inicialmente, planeábamos buscar la película por su ID, accediendo directamente a la posición de la lista correspondiente, lo que nos permitía mantener una complejidad constante (O(1)). Sin embargo, nos dimos cuenta de que si eliminábamos una película en la posición 0, lo que antes estaba en la posición 1 (por ejemplo, la película con ID 2) pasaba a ocupar la posición 0, lo que haría obsoleta nuestra implementación. Por esta razón, decidimos cambiar la implementación y hacer que el algoritmo recorra todas las películas, comparando el ID proporcionado con el de cada película. Si encuentra una coincidencia, devuelve la película; en caso contrario, indica que no se ha encontrado la película y devuelve status_code 404.

* `actualizar_pelicula`: Se obtiene el id de la película mediante la función obtener_pelicula_id(id), luego si la película existe, se actualiza el campo correspondiente. Se permite al usuario actualizar genero y/o título de la película, al finalizar, se devuelve el código 200 de éxito y se muestran los datos actualizados. En el caso de que el id solicitado no exista, se devulve el codigo de error 404 y un mensaje informando que no se encontró la película.
La mayoría de las decisiones para este caso, fueron tomadas en base a la lectura y ejemplos de APIs genericas o con funcionalidades similares.

* `eliminar_pelicula`: Se recorre la lista de peliculas, si se encuentra la pelicula que tiene el mismo `ID` con la que se la llama a la funcion, se la elimina, devolviendo un mensaje indicando que la pelicula se eliminó exitosamense, en caso de que no se halle, devuelve status_code 404 y un mensaje notificando el error.

  Se recorre toda la lista ya que si se busca borrar una pelicula usando como index el ID, al borrarse una pelicula y volver a usar esta funcion, borrara otra pelicula ya que el index de las peliculas cambió al haber un ID menos, y esto se agrava a medida que borramos peliculas.

* `buscar_peliculas`: Segun los argumentos ingresados en la URL despues del `localhost:5000/peliculas` la función separa en casos por si buscamos películas según el género o si contiene un texto en específico en su título, como asi también permite buscar por `ID`.

    Esta funcion recorre toda la lista de películas para encontrar la o las películas que coincidad con el texto o el género que se solicita, permite tambien además buscar en base al género de la película y el texto en el título a la vez, por ejemplo llamando al curl con `GET` y el siguiente argumento `localhost:5000/peliculas?genero=Acción&search=The`
* `pelicula_aleatoria`: Verifica que haya al menos una pelicula, y entre esas elige una al azar y devuelve la pelicula con todos sus detalles
* `pelicula_aleatoria_genero`: Se recorre la lista de peliculas y coloca las peliculas del genero que se pide en una lista aparte, si esa lista contiene al menos una pelicula, elige una al azar entre todas ellas, caso contrario devuelve error.

## API de feriados

Se corroboró si era posible utilizar la api de feriados con query strings de `fecha`, `día` y `tipo` de feriado, pero esta api no provee estas funcionalidades. Por este motivo, se tuvo que realizar **una request con el año actual**, obteniendo los feriados del año, e iterando sobre estos feriados aplicando los filtros que son ingresados por path y `query string`.

Por decisión de diseño, en el endpoint para recomendar una película de un género en un feriado de cierto tipo, decidimos que la respuesta no sea una única película dado que si el usuario, por ejemplo, ya ha visto esa película, debería realizar varias requests hasta que obtenga una película que le interese, en cambio si nosotros devolvemos una recomendación de todas las películas de ese género tiene más sentido. Si la cantidad de datos de películas es mayor, se debería agregar una limitacińo de cuántas películas devolver (podría ser 10 o 20). No se decidió utilizar el endpoint de devolver película aleatoria porque esto generaría inconvenientes para probar de manera efectiva el endpoint.

# Test de las funciones implementadas

`main.py`

- `obtener pelicula`:
    - test.py: Realizamos varios tests en los que buscábamos obtener películas tanto existentes como no existentes, imprimiendo en pantalla si el resultado era el esperado o si no se cumplía el caso esperado. Un obstáculo que encontramos fue que, después de ejecutar el test.py un número determinado de veces, este dejaba de funcionar correctamente. Para resolverlo, decidimos guardar el ID de la película agregada en cada test (la película de prueba) y usarlo en lugar de verificar siempre que la película con ID 14 no estaba presente. Así, por ejemplo, en lugar de verificar que la película con ID 14 no estuviera, ahora verificamos que la película con el ID "id_agregada + 1" no estaba.
    - test_pytest.py: Utilizamos la librería requests_mock junto con pytest para simular respuestas de la API durante nuestras pruebas. Usamos el fixture mock_response que simula varias interacciones con la API de películas. Primero, simulamos la respuesta del GET para obtener todas las películas, devolviendo una lista con dos películas: "Indiana Jones" (ID 1) y "Star Wars" (ID 2). Luego, simulamos la respuesta para obtener los detalles de dos películas existentes, la película con ID 1 ("Indiana Jones") y la película con ID 2 ("Star Wars"), asegurándonos de que los datos devueltos sean correctos. También simulamos la respuesta para obtener los detalles de una película inexistente, con ID 4, devolviendo un error 404 con el mensaje "Pelicula no encontrada". Finalmente, implementamos dos tests: uno que verifica la obtención correcta de los detalles de una película existente (ID 2) y otro que valida el manejo adecuado de un caso de error cuando la película no existe (ID 4). Estas simulaciones permiten realizar pruebas controladas sin necesidad de un servidor real. Para este punto tuvimos que investigar bastante para saber cómo hacer los tests de la manera correcta.

- `actualizar_pelicula`:
    - Test actualizar película: Corrobora que la pelicula se actualice correctamente y entregue el código correspondiente. Se devuelven los datos actualizados.
    - Test actualizar pelicula con solo un parámetro: Corrobora que la pelicula se actualice correctamente con un solo parámetro, tanto para el título como para el género y entregue el código correspondiente. Se devuelven los datos actualizados.
    - Test id no encontrado: Corrobora que se maneje el caso en el que el usuario ingrese un id que no exista, imprime 'OK' si el código es un 404, de lo contrario, 'FAIL'.

- `eliminar_pelicula`:
    - Test eliminar una película: Agrega una nueva pelicula y la elimina, verifica que esté eliminada y devuelva un status code 200 OK.
    - Test consultar pelicula post eliminación: Agrega una nueva película, la elimina, y consulta los datos de la película eliminada, el test verifica que obtener los datos de una pelicula eliminada no sea posible y devueelve status code 404.
    - Test actualizar película: Corrobora que la pelicula se actualice correctamente y entregue el código correspondiente. Se devuelven los datos actualizados.
    - Test actualizar pelicula con solo un parámetro: Corrobora que la pelicula se actualice correctamente con un solo parámetro, tanto para el título como para el género y entregue el código correspondiente. Se devuelven los datos actualizados.
    - Test id no encontrado: Corrobora que se maneje el caso en el que el usuario ingrese un id que no exista, imprime 'OK' si el código es un 404, de lo contrario, 'FAIL'.
- `buscar_peliculas:`
  - Test buscar peliculas por genero que existe: Agrega una pelicula en caso de que no existan peliculas de genero Acción y verifica que esta exista, devolviendo sus detalles, luego elimina la pelicula creada para testeo.
  - Test buscar peliculas en base a un genero inexistente: Busca entre las peliculas una pelicula de un genero inexistente, el test verifica que esto devuelva un status code 404.
  - Test buscar peliculas que contenga un determinado texto en sus titulos: Agrega una pelicula en caso de que no exista peliculas con un texto comun como lo es "The", devolviendo los detalles de las peliculas que coincidan con el texto y/o de la pelicula recien creada, dando sus detalles y un status code 200.
  - Test buscar peliculas que contengan un determinado texto imposible que coincida con titulos: Revisa entre todas las peliculas alguna que contenga un título creado con el propósito de no matchear con ninguna, devolviendo status code 404.

- `pelicula_aleatoria_genero:`
  - Test buscar película aleatoria por genero: busca una película del género indicado, corrobora que se reciba el codigo correcto y se devuelve los datos de la película.
  - Test buscar una película con género inexistente: busca un película con un género no existente, verifica que el codigo sea 404 y devuelve el error con un OK para indicar que todo salió bien, de lo contrario devuelve 'FAIL' indicando que falló.

API de feriados:

* `/feriado`: se corrobora el `status_code` y response esperado. Archivos: [test_pytest.py](test_pytest.py) y [test.py](test.py)

* `/feriado/<string>?day=<int>&month=<int>`: se corrobora el `status_code` y response esperado para los diferentes tipos de feriados. Archivos: [test_pytest.py](test_pytest.py) y [test.py](test.py)

* `/feriado/feriado_pelicula?type_holiday=<string>&type_movie=<string>`: se corrobora el `status_code` y response esperado para los diferentes tipos de feriados. Archivos: [test_pytest.py](test_pytest.py) y [test.py](test.py).

# Nuestra manera de trabajar

Nosotros empezamos a trabajar en el laboratorio desde GitHub con PRs previa a la fecha de acceso al repositorio en Bitbucket.

Trabajamos con branches que tienen origen desde `main`, de allí trabajamos cada funcionalidad en su propia branch. Una vez estaba finalizada, creamos una PR a main dónde solitamos Code Review a los compañaros del grupo.

Para los paths optamos por usar el estándar de Python que es agregar los archivos principales dentro de `src/`.
