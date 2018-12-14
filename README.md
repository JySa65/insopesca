# Insopesca
<!-- [![Build Status](https://travis-ci.org/JySa65/insopeca-api.svg?branch=master)](https://travis-ci.org/JySa65/insopeca-api) -->

## Requirements
* Git
* Docker
* Docker Compose
* Python 3
* PIP
* Virtualenv

### Install and configure Docker

1. Install docker
1. Intall docker-compose

### Set Var Environment

1. Copy to `env.example` into `.env`

        cp env.example .env

1. Edit values in `.env` depending on your preferences

        nano .env

### Generate Secret Key

1. You must generate the secret key
    
        python3.x generate_key.py

1. Copy the result in the .env file

## BackEnd

### Init work environment

        (.env) ➜ docker-compose build
        (.env) ➜ docker-compose run web python manage migrate

### Django Admin

1. Create user:

        (.env) ➜ docker-compose run web python manage createsuperuser

1. Access to django admin [localhost:8000/admin/](http://localhost:8000/admin/)

### Development

1. Start containers

        (.env) ➜ docker-compose up

1. Stop and destroy containers

        (.env) ➜ docker-compose down