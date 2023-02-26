# Music-APP

#Hosted Application
http://mayankgupta.pythonanywhere.com/

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

