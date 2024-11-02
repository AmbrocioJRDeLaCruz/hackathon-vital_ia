
# Proyecto de la hackathon - Vital.ia

Este proyecto es un sistema de ejemplo que se ejecuta en contenedores Docker usando Docker Compose. Contiene servicios como una aplicación web y un multiagente de LLM. Se integra con servicios desplegados en Azure como Azure Open AI, Document Intelligence, Storage Account, entre otros no contenerizables.

## Requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Estructura del Proyecto

```
.
├── docker/       # Carpeta con código para ejecutar los 3 componenentes mediante docker compose
├── front/         # Carpeta con código para ejecutar el UI directamente
├── back/         # Carpeta con código para ejecutar el API server directamente
├── agent/         # Carpeta con código para ejecutar el agente directamente
└── README.md        # Este archivo
└── requirements.txt      # Módulo de pip a instalar para correr la aplicación directamente
└── requirements.txt      # Archivo con descripción de la licencia del proyecto
```

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/jeffangel/hackathon-vital_ia.git
   cd docker
   ```

2. Asegúrate de que Docker y Docker Compose estén instalados en tu máquina.

## Configuración

Dentro de la carpeta docker, encontrarás un archivo `docker-compose.yml` que puede editarlo para ajustar la configuración del proyecto si es necesario. Puedes cambiar puertos, variables de entorno, y otros parámetros en este archivo.

## Uso

Para iniciar el proyecto, ejecuta el siguiente comando:

```bash
docker-compose up
```

Este comando construirá y levantará los contenedores definidos en el archivo `docker-compose.yml`. Si prefieres ejecutar el comando en modo "detached" (en segundo plano), puedes usar:

```bash
docker-compose up -d
```

Para detener los contenedores, usa:

```bash
docker-compose down
```

## Servicios

El proyecto contiene los siguientes servicios:

- **Frontend**: Servicio de cara al usuario final de la aplicación, que corre en [http://localhost](http://localhost).
- **Backend**: Servicio de gestión de API de la aplicación, que corre en [http://localhost:81](http://localhost:81).
- **Agente**: Servicio de multiagente LLM con LangGraph de la aplicación, que corre en [http://localhost:82](http://localhost:82).

## Variables de Entorno

Puedes configurar las variables de entorno en un archivo `.env` en la raíz del proyecto. Estas variables serán cargadas automáticamente por Docker Compose.

## Acceso a la Aplicación

Una vez que los contenedores están en ejecución, puedes acceder a la aplicación en tu navegador web en [http://localhost:8000](http://localhost:8000).

## Troubleshooting

- Para ver los logs de un servicio específico, usa `docker-compose logs <nombre_del_servicio>`.
- Si necesitas reconstruir las imágenes, usa `docker-compose up --build`.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
