# Inforce-restaurant-api

A REST api written in DRF for people with deadlines

## Technologies used

* [Django](https://www.djangoproject.com/): Django builds better web apps with less code.
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs

## Installation

* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can
  get python [here](https://www.python.org").
* After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
    ```
         pip install virtualenv
    ```
* Then, Git clone this repo to your PC
    ```
        git clone https://github.com/VitaliiKos/Inforce.git
    ```

* #### Dependencies
    1. cd into your cloned repo as such:
        ```
            cd Inforce
        ```
    2. Create and fire up your virtual environment:
        ```
            python -m venv venv
            venv\Scripts\activate
        ```
    3. Install the dependencies needed to run the app:
        ```
            pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```
            python manage.py makemigrations
        ```   
    5. Create .env and fill it according to the example .env.example



## Running an application in Docker

#### Build a Docker image

pen a command line and make sure you are at the root of your project. Run the command to build a Docker image:

```
    docker-compose up --build
```

#### Running a Django application

After the Django container is started, the application will be available at http://localhost:8000/. You can go
to http://localhost:8000/auth/ in your web browser.

