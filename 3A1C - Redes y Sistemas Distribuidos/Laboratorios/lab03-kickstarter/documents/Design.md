# Diseño Laboratorio 3 RySD 2025

## Opciones descartadas

Se descartaron las siguientes ideas:

### Parada y Espera

Analizando el caso base, realizamos una estimación en papel sobre qué algoritmo deberíamos apuntar primero y que luego sea más sencillo iterar, se consideró lo más simple, el protocolo de parada y espera. Si bien este protocolo era sencillo, todo aquello que necesitaríamos implementar no sería muy útil para los otros protocolos además de que la eficiencia del mismo, para el escenario actual, era muy mala.

### Verificaciones

Se omiten las siguientes verificaciones:

Validar parámetros de inicio del bufferSize y packetBySize, se asumen como correctos

```cpp
if (par("bufferSize").intValue() <= 0)
    throw cRuntimeError("bufferSize must be greater than zero");
```

```cpp
if (par("packetBySize").intValue() <= 0)
    throw cRuntimeError("packetBySize must be greater than zero");
```

### Módulo para manejar los números de secuencia

La idea era:

```cpp
#ifndef SEQUENCEGENERATOR_H_
#define SEQUENCEGENERATOR_H_

class SequenceGenerator {
private:
    int current;
    const int maxSeq;

public:
    explicit SequenceGenerator(int initial = 0, int maxSeq = 1000);
    int getNext();       // Devuelve el siguiente número de secuencia
    int getCurrent() const; // Devuelve el actual sin avanzar
};


#endif /* SEQUENCEGENERATOR_H_ */
```

```cpp
#include "SequenceGenerator.h"

SequenceGenerator::SequenceGenerator(int initial, int maxSeq)
    : current(initial), maxSeq(maxSeq) {}

int SequenceGenerator::getNext() {
    int next = (current + 1) % maxSeq;
    current = next;
    return current;
}

int SequenceGenerator::getCurrent() const {
    return current;
}
```

## Buenas prácticas de Omnet aplicadas

- **Agregar mensajes de log usando EV_INFO**: esto ayuda en la depuración sin tener que usar `bubble()` siempre, al poder visualizar en la consola los errores ocurridos.
- Modularización
- Herencia de módulos nativos de Omnet
- Creación de msg usando la librería.
- Realizar comentarios para un mejor seguimiento
- Usar nombres expresivos: se renombraron algunos componentes otorgados por el kickstarter para mayor claridad y seguimiento del flujo.

# Implementación

## Paquete custom: `Volt`

El paquete que se intercambian los hosts se llama *Volt*, y fue generado con la herramienta de template que ofrece omnet (`opp_msgc`) con el siguiente template:

<!-- Agregar imagen -->

```C++
packet Volt {
  bool flags = false;
  int seqNumber;
  int windowSize;
};
```

La primer versión del Volt solo consistía del mensaje y número de secuencia, posteriormente se agregraron las flags.

[**Volt.h**](../Volt.h)

```cpp
class Volt : public ::omnetpp::cPacket
{
  protected:
    bool flags;
    int seqNumber;
    int windowSize;
  public:
    virtual Volt *dup() const override {return new Volt(*this);}
    /* Nuestros métodos */

    // Flag methods
    virtual bool getFlags() const;
    virtual void setFlags(bool flags);

    // ACK methods
    bool getAckFlag();
    void setAckFlag(bool ackFlag);

    // SeqNumber methods
    bool getRetFlag();  // Retransmission Flag
    void setRetFlag(bool retFlag);

    // SeqNumber methods
    virtual int getSeqNumber() const;
    virtual void setSeqNumber(int seqNumber);

    // WindowSize methods
    virtual int getWindowSize() const;
    virtual void setWindowSize(int windowSize);
}
```

### seqNumber

El número de secuencia indica el orden de los paquetes. A diferencia de TCP, no implementamos números de secuencia por posición de byte, por lo que los números de secuencia simplemente **enumeran cada paquete**, y todos los paquetes tienen tamaño fijo (de *12500 b*).

Por cuestión de tiempo, simplemente seteamos el `MAX_SEQ_N = 1000`

> *Nota:* Planeabamos hacer el cambio a la implementación por bytes, y en gran parte la estructura actual del Sender ya permite eso, por lo que la transición no sería tan costosa. Se puede ver en [**mejoras posibles**](../Markdown/Analysis.md/#mejoras-posibles) para ver las posibles mejoras respecto a esto.

### Flags

Implementamos dos **FLAGS** actualmente. `ACK` y `RET`. Ambas encodeadas en el byte de flags. Para setear y obtener esos valores, hacemos *operaciones bitwise* y uso de *máscara de bits*.

**`ACK`** : Indica que el Volt actual es un volt de tipo ACK, no de datos.

**`RET`** : Indica que el Volt actual fue retransmitido. En caso de un Volt de tipo ACK, indica que es un ACK de un paquete que fue retransmitido. Esta información nos sirve para actualizar acordemente el RTT dinámico. (Ver seccion [*Karn*](#karn))

### windowSize

Por último este dato nos sirve para comunicar al emisor el tamaño de la ventana actual del receptor. (Ver sección [*Control de Flujo*](#control-de-flujo))

El windowSize máximo permitido es `2147483640`, lo cual es muy cercano al MAX_INT que se puede tener en **C**.

# Control de Flujo

Para control de flujo simplemente almacenamos la ventana de control actual en la variable de tipo entero currentControlWindowSize dentro del Sender. Cuando se verifica si es posible enviar un paquete Volt, se compara este valor con la cantidad de mensajes que están en el aire. Si la cantidad de mensajes en el aire mas el nuevo paquete que se desea enviar no excede el tamaño de la ventana, entonces se permite el envío del paquete.

# Control de Congestión

# `RenoManager`

Esta clase gestiona y almacena los timeouts de los paquetes de red, está definido de la siguiente manera:

```cpp
class RenoManager {
private:
    int maxSize;
    int size;
    int msgSendingAmount;
    bool isSlowStartStage = true;
    std::map<int, EventTimeout*> window;
public:
    int getMaxSize();
    int getSize();
    int getAvailableWin();
    void setSize(int newSize);
    void addTimeoutMsg(EventTimeout * msg);
    EventTimeout * popTimeoutMsg(int seqN);
    bool getSlowStart();
    void setSlowStart(bool state);
};
```

Los paquetes se gestionan mediante un diccionario que mapea un número de secuencia (tipo int) a un objeto EventTimeout. Tanto la clase `EventTimeout` como `Volt`, fueron generada a partir del template `cMessage` de Omnet++.

En nuestra implementación, usamos el mecanismo de arranque lento para control de flujo, el cual se representa mediante el booleano isSlowStartStage.

Con `size` y `msgSendingAmount` es posible calcular la disponibilidad del diccionario.

# EventTimeout

Esta clase dada por el template de Omnet++ de cMessage se le agregaron las siguientes variables y funciones:

```cpp
class EventTimeout : public ::omnetpp::cMessage {
protected:
    int seqN = 0;
    int packetSize = 0;
public:
    virtual int getSeqN() const;
    virtual void setSeqN(int seqN);
    virtual int getPacketSize() const;
    virtual void setPacketSize(int packetSize);
}
```