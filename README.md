https://docs.google.com/document/d/1EvGlcuyp7TpjpFUGFFi2WMSuhkljKSAeugJgcAgCceg/edit?usp=sharing

## Cloning & Run

1. Clone the project on your PC

`https://github.com/lsujh72/car_search_service.git`

2. Build and run docker image

`docker-compose build`
 
### Migrate database and initial database

`docker-compose run --rm web alembic upgrade head`

`docker-compose run --rm web python src/initial_data.py`

### Run docker

`docker-compose up`

### Swagger

`http://0.0.0.0:8000/docs`
