# Laboratorio 2 - RySD 2025 - Grupo 8 dlnv

> HFTP: Aplicación Servidor

- [Laboratorio 2 - RySD 2025 - Grupo 8 dlnv](#laboratorio-2---rysd-2025---grupo-8-dlnv)
- [Integrantes](#integrantes)
- [Objetivos](#objetivos)
- [Requisitos Previos](#requisitos-previos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Funcionalidades](#funcionalidades)
- [Comandos](#comandos)
  - [Chequear que cumpla las reglas de pep8](#chequear-que-cumpla-las-reglas-de-pep8)
  - [Desactivar el entorno](#desactivar-el-entorno)
- [Video](#video)
- [Documentacion](#documentacion)
- [Extensiones Visual Studio Code](#extensiones-visual-studio-code)

# Integrantes

- Dahlquist, Nicolás.
- Lucero, Carolina.
- Narvaez, Juan.
- Vispo, Valentina Solange.

# Objetivos

- Aplicar la comunicación cliente/servidor por medio de la programación de sockets, desde la perspectiva del servidor.
- Familiarizarse con un protocolo de aplicación diseñado en casa.
- Comprender, diseñar e implementar un programa servidor de archivos en Python.

# Funcionalidades

- Connection
  - [x] init()
  - [x] handle()
- Server
  - [x] init()
  - [x] serve()
- Client: no es necesario tocar nada.

# Requisitos Previos

- Python 3.7 o superior
- pip
- Git (opcional)
- Sistema operativo: probado en Windows 10/11 y Linux Ubuntu
- Telnet (instalado por defecto en Linux, en Windows se debe activar desde "Características de Windows")

# Estructura del Proyecto

.
├── client.py               # Cliente HFTP para interactuar con el servidor
├── command.py              # Módulo con lógica de comandos del protocolo
├── connection.py           # Manejo de conexiones de clientes
├── constants.py            # Constantes usadas en la aplicación
├── execute.py              # Ejecuta y coordina comandos del cliente
├── hftp_exception.py       # Manejo de excepciones específicas de HFTP
├── logger.py               # Módulo para logging de eventos
├── parser.py               # Parser del protocolo HFTP
├── README.md               # Este archivo, con instrucciones y documentación
├── response_manager.py     # Lógica para generar respuestas del servidor
├── server-test.py          # Pruebas automatizadas del servidor
└── server.py               # Servidor principal

# Comandos

1. Creamos el entorno

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

**Consola 1: Servidor**

```bash
python3 server.py
```

**Consola 2: Cliente**

```bash
python client.py -p 19500 0.0.0.0
```

## Chequear que cumpla las reglas de pep8

```bash
pycodestyle --show-source --show-pep8 server.py client.py constants.py connection.py
```

Otra alternativa:

```bash
flake8 server.py client.py constants.py connection.py
```

## Desactivar el entorno

```bash
deactivate
```

# Video

[Clic aquí para ver el video](https://youtu.be/j7JxQy0w28Y).

# Documentacion

[Pycodestyle - Chequear pep8](https://pycodestyle.pycqa.org/en/latest/intro.html)

[Pylint - Chequear pep8](https://www.pylint.org/)

# Extensiones Visual Studio Code

- [Trailing Spaces](https://marketplace.visualstudio.com/items?itemName=shardulm94.trailing-spaces)
