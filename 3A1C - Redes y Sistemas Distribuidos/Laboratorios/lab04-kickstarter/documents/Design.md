# Diseño 1 (brindado por cátedra)

Hace que los nodos envíen mensaje siempre en sentido horario, al ser de topología de anillo (cerrada), siempre llegará a destino, sin embargo no es el mas optimo de los algoritmos considerando el caso en el que un nodo esté al lado del nodo destino pero el nodo destino se halla en sentido antihorario, esto haría que el mensaje tenga que recorrer todos los demás nodos debido a que no cuenta con una forma de ir en sentido antihorario.

```cpp
void Net::handleMessage(cMessage *msg) {

    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;

    // If this node is the final destination, send to App
    if (pkt->getDestination() == this->getParentModule()->getIndex()) {
        send(msg, "toApp$o");
    }

    // If not, forward the packet to link interface #0 which
    // is the one connected to the clockwise side of the ring
    else {
        send(msg, "toLnk$o", 0);
    }
}
```

# Diseño 2 (envío al nodo del lado mas cercano)

Calcula la distancia entre el nodo origen y el nodo destino tanto si va en sentido horario o antihorario, una vez hecho, envía el mensaje en el sentido que menos distancia halla entre ambos nodos, haciendo que el mensaje tenga que recorrer a lo sumo la mitad de los nodos, optimizando la rapidez de la llegada del mensaje.

Sin embargo este algoritmo solo funciona si sabemos con exactitud la cantidad de nodos que contiene la topología de la red, si sabemos el orden de las mismas, y si la topología de red es un anillo bidireccional. No obstante la única información que suponemos saber es solo conocer el tipo de topología que presenta la red, lo demás es algo que no conocemos.

```cpp
void Net::handleMessage(cMessage *msg) {

    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;
    int destination = pkt->getDestination();
    int nodeIndex = this->getParentModule()->getIndex();

    // If this node is the final destination, send to App
    if (destination == nodeIndex) {
        send(msg, "toApp$o");
    }

    // If not, forward the packet to the side closest to destination
    else {
        int direction = 0; // 0 clockwise - 1 counterclockwise

        // Calculate the distance between nodes depending on the direction you take
        int counterclockwise = (destination - nodeIndex + 8) % 8;
        int clockwise = (nodeIndex - destination + 8) % 8;

        // If clockwise is closer, chooses gate 0, otherwise chooses gate 1
        direction = (clockwise < counterclockwise) ? 0 : 1;

        // Sends message to the closest side
        send(msg, "toLnk$o", direction);
    }
}
```

# Diseño 3 (Descubrimiento de nodos y optimización de envío de paquetes)

Debemos saber primero que para este diseño se usan dos tipos distintos de paquetes

```cpp
typedef enum {DATA, COUNTER} type_pkt;
```

`DATA` el cual será el paquete de datos que enviará datos a traves de los nodos o a la App, y `COUNTER` que servirá de contador para descubrir cuantos nodos posee esta red.

Basado en el diseño 2, este algoritmo se diferencia en que no asume el orden de los nodos ni asume la cantidad de nodos que posee la red, para descubrirlo los Net de cada nodo, al inicializar, envían todos un paquete `COUNTER` en un mismo sentido el cual recorre todo el anillo de la red, sumando el valor de counter por cada nodo recorrido.

```cpp
void Net::initialize() {
    // Create the initial COUNTER packet to count the number of nodes in the ring network
    Packet *counter = new Packet();
    int nodeIndex = getParentModule()->getIndex();
    counter->setKind(COUNTER);
    counter->setHopCount(0);
    counter->setSource(nodeIndex);
    counter->setDestination(nodeIndex);

    // Send the counter clockwise through gate 0
    send(counter, "toLnk$o", 0);
}
```

Una vez el paquete `COUNTER` vuelve al nodo de la Net que lo envió, guarda el valor en nodeCounter.

```cpp
void Net::handleMessage(cMessage *msg) {
// ...
    // The counter packet has already gone all the way around
    if (kind == COUNTER && destination == nodeIndex) {
        handleCounterReturn(pkt);
    }
// ...
}

void Net::handleCounterReturn(Packet* pkt) {
    nodeCounter = pkt->getHopCount() + 1;
    backToOrigin = true;
    delete pkt;
}
```

El envio de los paquetes entre los nodos se divide en casos:
- Si el paquete viene del Lnk, es decir que viene de otro nodo, se envía el mismo paquete al siguiente nodo incrementando el contador si se trata del paquete `Counter`.
- Si el paquete viene de la App, si no se conoce la cantidad de nodos que contiene la red, se guarda el paquete `Data` en un buffer hasta que se conozca el tamaño del anillo, caso contrario se vacía el buffer y se envía los paquetes `Data` a la dirección del nodo mas cercano al nodo destino calculando tanto la distancia por izquierda como por derecha en base a la cantidad de nodos que contiene la red.

```cpp
void Net::bufferOrSend(Packet* pkt, int nodeIndex) {
        // Store packets on a buffer until we know the ring size
        dataBuffer.insert(pkt);

        // Once we know the ring size, empties the data buffer
        if (backToOrigin) {
            while (!dataBuffer.isEmpty()) {
                Packet* data = (Packet*) dataBuffer.pop();
                int destination = data->getDestination();

                // Calculates closest side to destination node to send data packet
                int clockwiseDistance = (destination - nodeIndex + nodeCounter) % nodeCounter;
                int counterClockwiseDistance = nodeCounter - clockwiseDistance;

                // Choose direction based on shortest path (0 = clockwise, 1 = counterclockwise)
                int direction = (clockwiseDistance <= counterClockwiseDistance) ? 1 : 0;

                // Send the DATA packet in the chosen direction
                send(data, "toLnk$o", direction);
            }
        }
    }
```

- Últimamente si el paquete `Data` llega al nodo destino luego de los pasos previos, se envía finalmente a la App.
