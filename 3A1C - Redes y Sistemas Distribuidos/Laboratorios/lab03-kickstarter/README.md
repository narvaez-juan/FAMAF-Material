# Laboratorio N°3: Capa de Transporte

Redes y Sistemas Distribuidos 2025

# Objetivos

- Leer, comprender y generar modelos de red en Omnet++.

- Analizar tráfico de red bajo tasas de datos acotadas y tamaño de buffers limitados.

- Diseñar y proponer soluciones de control de congestión y flujo.

# Requisitos

- Omnet++ v6.0.1

# Opciones descartadas

- [/] Parada y espera.

# Primera iteración del diseño

- [x] Mensajes para ambos tipos de mensajes: datos y acks.
- [x] N° de seq.
- [x] ACK flag.
- [x] Ack Queue.
- [x] Data Queue.
- [x] BufferSize en cada cola.
- [x] Ventana corrediza.
- [x] Ventana de congestión (CW).
- [x] Custom packet: Volt
    - [x] Volt.msg
    - Flag methods
        - [x] getFlags()
        - [x] setFlags()
    - ACK methods
        - [x] getAckFlag()
        - [x] setAckFlag()
    - SeqNumber methods
        - [x] getSeqNumber()
        - [x] setSeqNumber()
    - WindowSize methods
        - [x] getWindowSize()
        - [x] setWindowSize()

# Segundo iteración del diseño

- [x] maxSize.
- [x] size.
- [x] Threshold.
- [x] Stages
    - [x] arranque lento al inicio y
    - [x] luego recuperación rápido.
- [x] Timer -> Timeout.
- [x] Control de flujo.
- [x] RTT fijo o dinámico.

# Tercer iteración del diseño

- [x] Retransmisión.
- [ ] ACKs duplicados.
- [ ] Reordenamiento de paquetes.


# Valores para la simulacion si solicita valores:

simTime = 0
packetByteSize = 12500
Network.nodeTx.trSender.bufferSize = 2000000


## cPacket

https://doc.omnetpp.org/omnetpp/api/classomnetpp_1_1cPacket.html

### Cómo saber de qué gate viene un mensaje

```cpp
bool arrivedOn()
```

### Cómo crear class template de packet

1) Crear el archivo `testPacket.msg`

```cpp

packet testPacket

{

     int srcAddress;

     int destAddress;

     int remainingHops = 32;

};

```

2) Correr el comando

```bash
opp_msgc testPacket.msg
```

3) Se habrán generado los archivos `testPacket_m.h` y `testPacket_m.cc`

# OMNet++

https://doc.omnetpp.org/omnetpp/manual/

https://stackoverflow.com/questions/52445993/omnet-on-windows-or-linux

https://stackoverflow.com/questions/7020069/make-library-not-found

