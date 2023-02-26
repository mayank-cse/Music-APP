from flask import current_app,url_for,redirect
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

@views.route('/', methods = ['GET','POST'])
@login_required
def home():
    # if request.method == 'POST':
    tracks = Track.query.filter_by(user_id=current_user.id).all()
    # print(len(tracks))
    Notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("dash.html",tracks=tracks, Notes = Notes, user=current_user,countTracks = len(tracks), countNotes = len(Notes))


@views.route('/note', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)



@views.route('/delete_note/<string:idd>', methods=['POST'])
@login_required
def delete_note(idd):  
    print(1)
    
    noteId = idd
    # request.form['noteId']
    print(noteId)
    note = Note.query.filter_by(id = noteId).first()
    print(note)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note successfully deleted",'success')
    else:
        flash("Unable to find the note")
    notes = Note.query.all(user_id)
    return render_template("notes.html", notes=notes, user=current_user)
#     return jsonify({})
# notes = Note.query.filter_by(Note.id = idd).first()
#     # print(tracks)
#     db.session.delete(tracks)
#     db.session.commit()
#     # flash("Playlist successfully deleted",'success')
#     tracks = Track.query.all()
    return render_template("listen.html", tracks = tracks, user=current_user)


@views.route("/listen", methods=["GET"])
@login_required
def listen():
    tracks = Track.query.all()
    # for song in tracks:
    #     print(song)
    return render_template("listen.html",tracks=tracks,user=current_user)


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
            song_lang = request.form["song_lang"]
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
                    track_language = song_lang,
                    user_id=current_user.id
                )
                db.session.add(new_track)
                db.session.commit()
            else:
                # else block to handle weird thing flask-uploads does, if any errors occur remove the file
                file = path + sep + uploaded_track_path
                os.remove(file)

            flash(filename + " " + "has been added to the library")
            tracks = Track.query.all()
            return render_template("dashboard.html", user=current_user, tracks=tracks)
        except UploadNotAllowed as err:

            return "<h1>sorry file type is not allowed :( </h1>", 406

    return render_template("upload.html", user=current_user)


#search
@views.route('/search',methods=['GET','POST'])
@login_required
def search():
    tracks = Track.query.all()
    return render_template("search.html",tracks=tracks, user=current_user)

@views.route('/search/<string:idd>',methods=['GET','POST'])
@login_required
def ytsearch(idd):
    # print(1)
    # if request.method == 'POST':
    tracks = Track.query.filter_by(track_title=idd,user_id=current_user.id).all()
    print(tracks)
    # print(tracks)
    # db.session.delete(tracks)
    # db.session.commit()
    # # flash("Playlist successfully deleted",'success')
    # tracks = Track.query.all()
    return render_template("song.html", tracks = tracks, user=current_user)
# @views.route('/ytsearch/<string:song>',methods=['GET','POST'])   
# def ytSearch(idd):
# 	string=""
# 	song=idd
# 	song_name=song +'.mp3'
#     # print(song_name)
#     tracks = Track.query.filter_by(track_title=song, user_id=current_user.id).first()
# 	# cur=db.connection.cursor()
    
# 	# # result=cur.execute("SELECT * FROM songs_list WHERE song_name=%s",[song_name])
# 	# # albu69=cur.fetchall()
#     # tracks = Track.query.all()
# 	# if result>0:
# 	# 	return render_template('search.html',albu=albu69)
# 	# else:
# 	# 	try:
# 	# 		page = request.get("https://www.youtube.com/results?search_query="+song)
# 	# 		soup = BeautifulSoup(page.text,'html.parser')
# 	# 		for div in soup.find_all('div', { "class" : "yt-lockup-video" }):
# 	# 			if div.get("data-context-item-id") != None:
# 	# 				video_id = div.get("data-context-item-id")
# 	# 				break
# 	# 		os.system('youtube-dl --extract-audio --audio-format mp3 -o "akhil.mp3" https://www.youtube.com/watch?v='+video_id)
# 	# 		os.system("mv *.mp3 ./static/music/")
# 	# 		os.rename("static/music/akhil.mp3","static/music/"+song_name)
# 	# 		string="/static/music/"+song_name
# 	# 		cur=db.connection.cursor()
# 	# 		cur.execute("INSERT INTO songs_list(path,album,song_name) VALUES (%s,%s,%s)",(string,"NA",song_name))
# 	# 		db.connection.commit()
# 	# 		result=cur.execute("SELECT * FROM songs_list WHERE song_name=%s",[song_name])
# 	# 		albu99=cur.fetchall()
# 	# 		return render_template('search.html',albu=albu99)
        
# 	# 	except NameError:
# 	# 		flash('Song Not Found','success')
# 	# 		return render_template('home.html')
@views.route('/share', methods=["GET","POST"])
@login_required
def share():
    if request.method == "POST":
        co = request.form['share']
        # print(f"{redirect(url_for('views.search'))}")
        
        # flash('you are now logout','success')
	    # return redirect(url_for('login'))
    return render_template('home.html', user = current_user)
sep = os.path.sep
path = os.getcwd() + os.path.join(sep, "website"+sep+"static" + sep, "songs")
# Download
@views.route('/download', methods=["GET","POST"])
@login_required
def download():
    if request.method == "POST":
        co = request.form['download']
        try:
            return send_file(path+sep+co, as_attachment=True)
        except Exception as e:
            return str(e)
        
#Map
@views.route('/map',methods=['GET','POST'])
@login_required
def map():
    tracks = Track.query.filter_by(user_id=current_user.id).all
    return render_template("map.html",tracks=tracks, user=current_user)
#profile
@views.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    # if request.method == 'POST':
    tracks = Track.query.filter_by(user_id=current_user.id).all()
    # print(len(tracks))
    Notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("dash.html",tracks=tracks, Notes = Notes, user=current_user,countTracks = len(tracks), countNotes = len(Notes))

#profile update
@views.route('/profile-update', methods=['GET','POST'])
@login_required
def profile_update():
    if request.method =='POST':
        newName = request.form.get('name')
        newEmail = request.form.get('email')
        if newName:
            current_user.first_name = newName
        if newEmail:
            current_user.email = newEmail
        db.session.commit()
    return render_template("dash.html", user=current_user)
@views.route('/delete_playlist/<string:idd>',methods=['GET','POST'])
@login_required
def delete_playlist(idd):
    # print(1)
    # if request.method == 'POST':
    tracks = Track.query.filter_by(track_title=idd,user_id=current_user.id).first()
    if tracks.user_id == current_user.id:
            db.session.delete(tracks)
            db.session.commit()
            flash("Playlist successfully deleted",'success')
            tracks = Track.query.filter_by(user_id=current_user.id).all
            return render_template("listen.html", tracks = tracks, user=current_user)
    
    return render_template("dashboard.html", tracks = tracks, user=current_user)