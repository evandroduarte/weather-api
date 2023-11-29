# weather-api

Essa API permite que você solicite a previsão do tempo para os próximos cinco dias para uma cidade específica. Além disso, ela armazena os dados da previsão no MongoDB e fornece um endpoint para recuperar solicitações de previsão do tempo passadas.

## Pré-requisitos 

Antes de começar se certifique que você possui o Docker e o Docker Compose instalados na sua máquina

- [Guia Docker](https://docs.docker.com/get-docker/)
- [Guia Docker Compose](https://docs.docker.com/compose/install/)

## Iniciando a aplicação

Na pasta da aplicação execute o comando

```
docker-compose up --build
```

Após o build do projeto a aplicação irá estar acessível na url

```
http://localhost:5000
```

Para finalizar a aplicação basta utilizar o comando

```
docker-compose down
```

## Testes

Para executar os testes *com o container docker rodando* execute o comando

```
docker exec -it web /bin/bash -c "cd /app && python -m unittest discover -s tests -p '*_test.py'
```

- **Buscar previsão dos próximos 5 dias:**
  - Endpoint: `/weather`
  - Método: `GET`
  - Parâmetros:
    - `city` (str): Nome da cidade (default: Brasilia)
    - `language` (str): Linguagem para descrição do clima (default: pt_br)
    - `units` (str): Unidade de medida dos resultados (default: metric)
  - Exemplo Resposta:
    - { "city_name": "Brasília",
        "forecasts": [
            {
                "datetime": "30/11/2023 00:00:00",
                "feels_like": "297.77°C",
                "humidity": "58%",
                "max_temperature": "297.74°C",
                "min_temperature": "297.35°C",
                "temperature": "297.74°C",
                "weather_description": "Broken clouds"
            },
            {
                "datetime": "30/11/2023 03:00:00",
                "feels_like": "296.1°C",
                "humidity": "63%",
                "max_temperature": "296.1°C",
                "min_temperature": "295.19°C",
                "temperature": "296.1°C",
                "weather_description": "Broken clouds"
            },
            {
                "datetime": "30/11/2023 06:00:00",
                "feels_like": "293.4°C",
                "humidity": "74%",
                "max_temperature": "293.39°C",
                "min_temperature": "293.39°C",
                "temperature": "293.39°C",
                "weather_description": "Overcast clouds"
            }, ... ]}


- **Retrieve Past Requests:**
  - Endpoint: `/past-requests`
  - Método: `GET`
  - Parâmetros:
    - `start_date` (str): Data de ínicio (YYYY-MM-DD)
    - `end_date` (str): Data final (YYYY-MM-DD)
    - `city (str)`: Nome da cidade (opcional)
    - `language` (str): The language for the weather data (opcional)
    - `units` (str): Unidade de medida dos resultados (opcional)
  - Exemplo Resposta:
    [
        {
            "_id": {
                "$oid": "6567a0d0da696d6ae8dc7616"
            },
            "city": "Brasilia",
            "language": "pt_br",
            "units": "metric",
            "forecast": [
                {
                    "datetime": "29/11/2023 21:00:00",
                    "temperature": "24.78°C",
                    "min_temperature": "24.78°C",
                    "max_temperature": "26.88°C",
                    "humidity": "61%",
                    "feels_like": "24.91°C",
                    "weather_description": "Nublado"
                },
                {
                    "datetime": "30/11/2023 00:00:00",
                    "temperature": "24.59°C",
                    "min_temperature": "24.2°C",
                    "max_temperature": "24.59°C",
                    "humidity": "58%",
                    "feels_like": "24.62°C",
                    "weather_description": "Nublado"
                }], ... }]