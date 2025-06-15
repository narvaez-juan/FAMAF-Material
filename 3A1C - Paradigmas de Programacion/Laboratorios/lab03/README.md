# Lector automático de Feeds RRS con Apache Spark

## Configuración del entorno y ejecución
Instrucciones para el usuario sobre cómo correr las dos partes del laboratorio con spark. Explicación del resultado que se espera luego de ejecutar cada parte.

### Correr Spark en modo local

Para correr nuestro programa Spark en modo local contamos con un Makefile ya implementado, primero deberemos ver que los valores de las variables coinciden con los nuestros, revisar valores como el nombre de usuario o la versión del Spark, seguidamente basta con abrir bash y correr ```make```, lo cual debería ejecutar ```make build``` y luego ```make run```, esto último se puede hacer por separado si no buscamos correr el proyecto sino solo buildearlo. 

Importante tener en cuenta que si se ejecuta en local, la sesión de spark del SparkFeedReaderService.java deberá estar configurada como tal (local[*])

### Correr Spark en un clúster

Se debe tener en cuenta las variables del Makefile, al igual que en el caso anterior.

Para correr nuestro programa Spark en un clúster debemos seguir los siguientes pasos:
1. Dentro del directorio ${SPARK_FOLDER} ejecutar ```./start-master.sh```
2. Abrir ```http://localhost:8080```
3. Copiar la URL que empieza por ```spark://```
4. Dentro del mismo directorio ejecutar ```./start-worker.sh $(URL-HERE) -m 1G -c 1```
5. Ejecutar ```make spark``` para lectura de los feed o ```make spark-ne``` para aplicar heuristica

Importante tener en cuenta que si se ejecuta en cluster, la sesión de spark del SparkFeedReaderService.java deberá estar configurada como tal (misma URL del punto 3)

## Decisiones de diseño

Decidimos implementar SparkFeedReaderService que hereda la función de parseo de feeds de la interfaz IFeedReaderService, utilizando el framework Spark, de ésta forma no es necesario implementar una nueva lógica para correr el programa usando computación distribuida, sino sólo paralelizar las tareas y funciones del programa. 

Por otra parte, se decidió convertir el getParserFeed de IFeedReaderService.java en un método estático porque funciona con la misma lógica tanto si queremos usar ejecutar el programa usando computación distribuida como si no.

## Conceptos importantes

1. **Describa el flujo de la aplicación** ¿Qué pasos sigue la aplicación desde la lectura del archivo subscriptions.json hasta la obtención de las entidades nombradas? ¿Cómo se reparten las tareas entre los distintos componentes del programa?

- El flujo de aplicación es el siguiente, primero se instancia subscriptionParser, HttpRequester y SparkFeedReaderService, luego se parsea el contenido del susbscription.json a un Subscription, los cuales contienen muchas SingleSubscription, según el input de usuario, se descarga y muestra feeds o se muestran feeds por heurística, para ello primero se paraleliza la descarga de feeds los cuales se guardan en pares <SingleSubscription, Integer> y luego se crea JavaRDD o lista distribuida de Articles en el que se obtiene el feed parseado usando métodos de Spark, seguidamente con los mismos métodos se procesan las entidades nombradas también en paralelo, y seguidamente se las agrupa y cuenta para poder imprimir los resultados de una manera ordenada.
- Estas tareas se reparten del siguiente modo, SubscriptionParser se encarga de parsear las subscriptions (como el subscription.json), IFeedRederService se encarga del parseo de feeds, y SparkFeedReaderService se encarga de imprimir feeds y entidades nombradas a su vez que procesarlas y parsearlas (estos últimos en paralelo usando el framework Spark).

2. **¿Por qué se decide usar Apache Spark para este proyecto?** ¿Qué necesidad concreta del problema resuelve?

- Se decide usar Apache Spark para este proyecto ya que se descarga muchos feeds y se debe calcular grandes cantidades de entiddes nombradas, y Apache Spark es un framework que soluciona esto pues se encarga de ejecutar en paralelo varias tareas en distintas computadoras, permitiendo el procesamiento distribuido de datos, reduciendo así los tiempos de cómputo.

3. **Liste las principales ventajas y desventajas que encontró al utilizar Spark.**

- Ventajas:
    - Mejor manejo de sets de datos (como pueden ser diccionarios, tuplas, listas), ya que provee métodos para manipular las mismas al estilo de EntityFramework y LINQ en C# o similares en otros lenguajes.
    - Posibilidad de paralelizar la ejecución de un programa en multiples núcleos (ejecutando en local) o computadoras (cluster).
    - Nos evita ocupar el tiempo en una lógica para paralelizar el computo, dejandonos ocupar ese tiempo para desarrollar la lógica del programa.
- Desventajas:
    - La documentación de Spark es muy confusa y dificil de leer la primera vez.
    - Para sacarle el mayor provecho, requiere de cierta experiencia por parte del desarrollado, aunque se pueden llegar a buenos resultados igualmente.

4. **¿Cómo se aplica el concepto de inversión de control en este laboratorio?** Explique cómo y dónde se delega el control del flujo de ejecución. ¿Qué componentes deja de controlar el desarrollador directamente?

- En este laboratorio se aplica el concepto de inversión de control a traves de la inyección de dependencias en las clases (lograda a través del constructor) y en la utilización de Spark, ya que este nos permite delegar la lógica del paralelismo, como se distribuyen las tareas, como se manejan los recursos y que hacer frente a un fallo de lo mencionado. En pocas palabras, el desarrollador deja de controlar la ejecución paralela, la gestión de memoria y la organización de las tareas a ejecutar, permitiendo que ese esfuerzo se coloque en la lógica del programa.

5. **¿Considera que Spark requiere que el codigo original tenga una integración tight vs loose coupling?**

- Consideramos que el código original debe tener una integración loose coupling ya que la función de parseo de feeds no debe ser fuertemente dependiente de que se esté ejecutando el programa usando Spark o no, ni de otras funciones, sino que debe ser independiente.

6. **¿El uso de Spark afectó la estructura de su código original?** ¿Tuvieron que modificar significativamente clases, métodos o lógica de ejecución del laboratorio 2?

- No hubo que hacer cambios significativos en cuanto al código original, solo se creó un nuevo archivo SparkFeedReaderService.java que implementa el lector de feeds usando Spark, y se hizo cambios en la interfaz IFeedReaderService en el método del parseo de feeds. Con todo esto solo basta con cambiar el reader a utilizar en el archivo main para utilizar o dejar de utilizar Spark.
