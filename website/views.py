from flask import current_app
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user,logout_user
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask import send_file, send_from_directory
from .models import Note, Track
from . import db
import json
from flask_uploads import UploadSet, configure_uploads, AUDIO, UploadNotAllowed
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from .script import TrackInfo
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
views = Blueprint('views', __name__)


@views.route('/note', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/', methods = ['GET','POST'])
@login_required
def dashboard():
    # if request.method == 'POST':
    tracks = Track.query.all()
    return render_template("dashboard.html",tracks=tracks, user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route("/listen", methods=["GET"])
def listen():
    tracks = Track.query.all()
    # for song in tracks:
    #     print(song)
    return render_template("listen.html",tracks=tracks)


audio = UploadSet("audio", AUDIO)

sep = os.path.sep
path = os.getcwd() + os.path.join(sep, "website"+sep+"static" + sep, "songs")
# C:\Users\mayan\OneDrive\Desktop\AuthFlask\Music-APP-\website\static\songs\Songs.PK_Unchained_Melodies_Encore_-_03_-_Ya_Rabba_Salaam-E-Ishq_1.mp3
@views.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST" and "audio" in request.files:
        # print(1111111)
        try:
            filename = audio.save(request.files["audio"])
            
            uploaded_track_path = filename
            
            if filename and uploaded_track_path:
                print(path + sep + uploaded_track_path)
                track_info = TrackInfo.All(path + sep + uploaded_track_path)
                artist = track_info["artist"]
                if artist == None:
                    artist = "Unknown artist"
                title = track_info["title"]
                if title == None:
                    title = "Unknown track"
                duration = track_info["track_lenght"]
                new_track = Track(
                    track_title=title,
                    track_artist=artist,
                    track_location=uploaded_track_path,
                    track_duration=duration,
                )
                db.session.add(new_track)
                db.session.commit()
            else:
                # else block to handle weird thing flask-uploads does, if any errors occur remove the file
                file = path + sep + uploaded_track_path
                os.remove(file)

            return filename + " " + "has been added to the library"
        except UploadNotAllowed as err:

            return "<h1>sorry file type is not allowed :( </h1>", 406

    return render_template("upload.html")


#search
@views.route('/search',methods=['GET','POST'])
def search():
    tracks = Track.query.all()
    return render_template("search.html",tracks=tracks)
        # for song in tracks:
        #     # print(song.track_location,co)
        #     if song.track_location == co:
        #         # print(1111111)
        #         # print(song)
        #         render_template("search.html",tracks=tracks)
        
        # return render_template('search.html')
# def new():
# 	string=""
	# co=request.form['give']
# 	song=co
# 	song_name=co+'.mp3'
    
# 	cur=db.connection.cursor()
    
# 	result=cur.execute("SELECT * FROM songs_list WHERE song_name=%s",[song_name])
# 	albu69=cur.fetchall()
    
# 	if result>0:
# 		return render_template('search.html',albu=albu69)
# 	else:
# 		try:
# 			page = request.get("https://www.youtube.com/results?search_query="+song)
# 			soup = BeautifulSoup(page.text,'html.parser')
# 			for div in soup.find_all('div', { "class" : "yt-lockup-video" }):
# 				if div.get("data-context-item-id") != None:
# 					video_id = div.get("data-context-item-id")
# 					break
# 			os.system('youtube-dl --extract-audio --audio-format mp3 -o "akhil.mp3" https://www.youtube.com/watch?v='+video_id)
# 			os.system("mv *.mp3 ./static/music/")
# 			os.rename("static/music/akhil.mp3","static/music/"+song_name)
# 			string="/static/music/"+song_name
# 			cur=db.connection.cursor()
# 			cur.execute("INSERT INTO songs_list(path,album,song_name) VALUES (%s,%s,%s)",(string,"NA",song_name))
# 			db.connection.commit()
# 			result=cur.execute("SELECT * FROM songs_list WHERE song_name=%s",[song_name])
# 			albu99=cur.fetchall()
# 			return render_template('search.html',albu=albu99)
        
# 		except NameError:
# 			flash('Song Not Found','success')
# 			return render_template('dashboard.html')

sep = os.path.sep
path = os.getcwd() + os.path.join(sep, "website"+sep+"static" + sep, "songs")
# Download
@views.route('/download', methods=["GET","POST"])
def download():
    if request.method == "POST":
        co = request.form['download']
        try:
            return send_file(path+sep+co, as_attachment=True)
        except Exception as e:
            return str(e)
        
#Map
@views.route('/map',methods=['GET','POST'])
def map():
    tracks = Track.query.all()
    return render_template("map.html",tracks=tracks)