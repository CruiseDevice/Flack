import os

from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room

from forms import LoginForm

from credentials import SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = LoginForm()
	if form.validate_on_submit():
		session['name'] = form.name.data
		session['room'] = form.room.data
		return redirect(url_for('chat'))
	elif request.method == 'GET':
		form.name.data = session.get('name', '')
		form.room.data = session.get('room', '')
	return render_template('index.html', form=form)


@app.route('/chat')
def chat():
	name = session.get('name', '')
	room = session.get('room', '')
	if name == '' or room == '':
		return redirect(url_for('index'))
	return render_template('chat.html', name=name, room=room)


@socketio.on('joined', namespace='/chat')
def joined(message):
	pass
	room = session.get('room')
	join_room(room)
	emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
	room = session.get('room')
	leave_room(room)
	emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
