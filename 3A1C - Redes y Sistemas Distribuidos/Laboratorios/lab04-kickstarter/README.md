# Laboratorio N°4: Capa de Red - Redes y Sistemas Distribuidos, FAMAF - 2025

Fecha límite de entrega: 13/05

# Índice

- [Laboratorio N°4: Capa de Red - Redes y Sistemas Distribuidos, FAMAF - 2025](#laboratorio-n4-capa-de-red---redes-y-sistemas-distribuidos-famaf---2025)
- [Índice](#índice)
- [Objetivos](#objetivos)
- [Métricas](#métricas)
- [Caso I](#caso-i)
- [Caso II](#caso-ii)
- [Si no se genera el archivo General.anf](#si-no-se-genera-el-archivo-generalanf)
- [Extensiones de Visual Studio Code](#extensiones-de-visual-studio-code)

# Objetivos

- Leer, comprender y generar modelos de red en Omnet++.
- Analizar tráfico de red bajo diferentes estrategias de enrutamiento.
- Diseñar y proponer soluciones de enrutamiento bajo diferentes topologías.

------


[Informe](documents/Informe.md) y [Diseño](documents/Design.md)

------

# Métricas

- [x] Medidas de demora de entrega de paquetes
- [x] Cantidad de saltos utilizados por cada paquete
- [x] Utilización de los recursos de la red
  - [x] Bufferes
  - [x] Enlaces

# Caso I

node[0] y node[1] enviando a node[5]

Configuración del omnetpp.ini

```bash
[General]
network = Network
sim-time-limit = 200s

Network.node[0].app.interArrivalTime = exponential(1)
Network.node[0].app.packetByteSize = 125000
Network.node[0].app.destination = 5

Network.node[2].app.interArrivalTime = exponential(1)
Network.node[2].app.packetByteSize = 125000
Network.node[2].app.destination = 5
```

# Caso II

node[0],node[1],node[2],node[3],node[4],node[6],node[7] enviando a node[5]

`packetByteSize` e `intervalTime` iguales

```bash
intervalTime = exponential(1)
packetByteSize = 125000
destination = 5
```

```bash
[General]
network = Network
sim-time-limit = 200s

Network.node[{0,1,2,3,4,6,7,8}].app.interArrivalTime = exponential(1)
Network.node[{0,1,2,3,4,6,7,8}].app.packetByteSize = 125000
Network.node[{0,1,2,3,4,6,7,8}].app.destination = 5
```

# Si no se genera el archivo General.anf

Copiar el siguiente apartado y generarlo:

```html
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<analysis version="2">
    <inputs>
        <input pattern="/lab4-kickstarter/results/General-*.vec"/>
        <input pattern="/lab4-kickstarter/results/General-*.sca"/>
    </inputs>
    <charts/>
</analysis>
```

> NOTA: se debe modificar el "/lab4-kickstarter/results/General-*.vec" y "/lab4-kickstarter/results/General-*.sca" según el path del nombre del proyecto en Omnet++

# Extensiones de Visual Studio Code

- [Markdown Preview with Bitbucket Styles](https://marketplace.visualstudio.com/items/?itemName=hbrok.markdown-preview-bitbucket)
