# weather-api

Essa API permite que você solicite a previsão do tempo para os próximos cinco dias para uma cidade específica através da API [OpenWeatherMap](https://openweathermap.org/). Além disso, ela armazena os dados da previsão no MongoDB e fornece um endpoint para recuperar solicitações de previsão do tempo passadas.

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
  - Exemplo Resposta:
    ```
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
            }, ... ]}```


- **Retrieve Past Requests:**
  - Endpoint: `/past-requests`
  - Método: `GET`
  - Parâmetros:
    - `start_date` (str): Data de ínicio (YYYY-MM-DD)
    - `end_date` (str): Data final (YYYY-MM-DD)
    - `city (str)`: Nome da cidade (opcional)
    - `language` (str): The language for the weather data (opcional)
    - `start_date` e `end_date` devem ser usados em conjunto
  - Exemplo Resposta:
    ```[
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
                }], ... }]```

## Testes Insomnia

- /weather
![Screenshot from 2023-11-29 20-17-34](https://github.com/evandroduarte/weather-api/assets/39135867/3c7a9df1-0cca-41bc-a9c4-c6d961c5874a)

- /weather (Filtro composto)
![Screenshot from 2023-11-29 20-47-15](https://github.com/evandroduarte/weather-api/assets/39135867/8d12ebaa-9c2d-4f99-8f4e-f1b874f6c167)

- /requests (Sem filtro)
![Screenshot from 2023-11-29 20-17-49](https://github.com/evandroduarte/weather-api/assets/39135867/5830dc6a-28ad-4c42-8397-07f3fbfcc630)

- /requests (Filtro cidade)
![Screenshot from 2023-11-29 20-18-17](https://github.com/evandroduarte/weather-api/assets/39135867/e79ce967-d0a9-44c9-9f4f-0e1b8794e390)

- /requests (Filtro composto)
![Screenshot from 2023-11-29 20-20-29](https://github.com/evandroduarte/weather-api/assets/39135867/468559d1-83ec-4811-900a-161639f5a113)

