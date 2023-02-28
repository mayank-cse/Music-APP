# Music-APP

#Hosted Application
http://mayankgupta.pythonanywhere.com/

`Music-App` is a working Flask music streaming project with features:

- Upload a song
  -	Has metadata fields title, artist, album
  -	Song should have a unique URL which can be shared with anyone publically.
-	Delete an uploaded song
-	View all songs
-	Search for any song via album/title/artist
  -	Stream song
  -	Each song have a page where you can play the song from the browser itself. Use HTML5 for this, not flash.
  -	Clicking on the unique URL of a song leads to this page.
  -	Clicking on a song entity from either search or view all pages also lead to this page.
  -	There is an option to download this song
- **Database migrations** out-of-the-box (uses Alembic)
- Simple setup `make setup && make run`, you only need to provide your security and secret key (will work with example keys only on `127.0.0.1:5000`). Allow user login/logout.
- Static files managed by `bower`. By default, templates use `Bootstrap` but don't force you to use this UI framework. 
- Built-In `Flask-Script` shell commands
- **Fixtures** dump/restore support
- Integrated [Celery](http://celeryproject.org/) background tasks management
- Cache using [Flask-Cache](https://pythonhosted.org/Flask-Cache/)
- Logging with an example of how to make email notifications when something goes wrong on the server

Using Flask to build a Restful API Server.

Integration with Flask-Uploads, Flask-SQLalchemy,and Flask-OAuth extensions.

### Extension:

- SQL ORM: [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

- Hosting Server: [PythonAnywhere](https://www.pythonanywhere.com/)

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```
Then manually clone this repository and change it later by own. Project is ready to run (with some requirements). You need to clone and run:

```sh
$ mkdir Music-App
$ cd Music-App
$ git clone git@github.com:mayank-cse/Music-App.git .
$ make
$ make run
```

Open http://127.0.0.1:5000/, customize project files and **have fun**.

If you have any ideas about how to improve it [Fork project]https://github.com/mayank-cse/Music-APP/fork) and send me a pull request.

## Flask Application Structure 
```
.
|──────main.py
| |────instance
| | |────music.db
| | |────cve/
| | |────user/
| | |────oauth/
| |──────website
| | |────static/
| | | |──css
| | | |──images
| | | |──songs
| | |────templates/
| | | |──base.html
| | | |──dash.html
| | | |──Extview.html
| | | |──login.html
| | | |──map.html
| | | |──notes.html
| | | |──search.html
| | | |──sign_up.html
| | | |──song.html
| | | |──upload.html
| | |────__init__.py
| | |────auth.py
| | |────models.py
| | |────script.py
| | |────views.py


```


## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```
### Configuring From Files



#### Builtin Configuration Values

SERVER_NAME: the name and port number of the server. 

JSON_SORT_KEYS : By default Flask will serialize JSON objects in a way that the keys are ordered.

- [reference¶](http://flask.pocoo.org/docs/0.12/config/)


### OAuth Setup
add your `client_id` and `client_secret` into config file.
 
## Run Flask
### Run flask for develop
```
$ python music-app/run.py
```
In flask, Default port is `5000`

Swagger document page:  `http://127.0.0.1:5000/api`

### Run flask for production

** Run with gunicorn **

In  webapp/

```
$ gunicorn -w 4 -b 127.0.0.1:5000 run:app

```

* -w : number of worker
* -b : Socket to bind


### Run with Docker

```
$ docker build -t flask-example .

$ docker run -p 5000:5000 --name flask-example flask-example 
 
```

In image building, the webapp folder will also add into the image


## Unittest
```
$ nosetests webapp/ --with-cov --cover-html --cover-package=app

```
- --with-cov : test with coverage
- --cover-html: coverage report in html format

## Reference

Offical Website

- [Flask](http://flask.pocoo.org/)
- [Flask Extension](http://flask.pocoo.org/extensions/)
- [Flask restplus](http://flask-restplus.readthedocs.io/en/stable/)
- [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [Flask-OAuth](https://pythonhosted.org/Flask-OAuth/)
- [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)
- [gunicorn](http://gunicorn.org/)

Tutorial

- [Flask Overview](https://www.slideshare.net/maxcnunes1/flask-python-16299282)
- [In Flask we trust](http://igordavydenko.com/talks/ua-pycon-2012.pdf)

[Wiki Page](https://github.com/tsungtwu/flask-example/wiki)



## Changelog
- Version 2.1 : Profile view and update
- Version 2.0 : add SQL ORM extension: FLASK-SQLAlchemy
- Version 1.4 : Note|Map|Dashboard Feature Added
- Version 1.3 : Added Live Search Function
- Version 1.2 : Download Feature Added
- Version 1.1 : song upload and play integrated
- Version 1.0 : Authentication Page
