# Configurar las sugerencias y sintaxis de omnet

```json
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${env:__omnetpp__dir}/include",
                "${workspaceFolder}/**"
            ],
            "defines": [],
            "compilerPath": "/usr/bin/clang",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "linux-clang-x64"
        }
    ],
    "version": 4
}
```

```bash
export __omnetpp__dir=/ruta/a/tu/omnetpp-6.0.1
```

Si es desde la maquina virtual de la catedra:

```bash
export __omnetpp__dir=/home/estudiante/omnetpp-6.0.1
```