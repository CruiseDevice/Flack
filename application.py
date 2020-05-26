import os
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room

from forms import LoginForm

from credentials import SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app)

room_list = []
user_list = []
messages = []

MESSAGE_LIMIT = 100
msg_count = 0


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        if ((session['room'] not in room_list)
                and (session['name'] not in user_list)):
            room_list.append(session['room'])
            user_list.append(session['name'])
        return redirect(url_for('chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form, room_list=room_list)


@app.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')

    if name == '' or room == '':
        return redirect(url_for('index'))
    return render_template('chat.html', name=name, room=room)


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {
        'msg': '{0} has entered the room.'.format(session.get('name'))
    }, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    user = session.get('name')
    context = {
        'msg': message['msg'],
        'user': session.get('name'),
        'timestamp': datetime.now()
    }
    messages.append(context)
    for message in messages:
        if user == message['user']:
            msg_count += 1
    if msg_count > MESSAGE_LIMIT:
        emit('message', {
            'msg': 'You are only allowed to send {0} messages a session'.format(
                MESSAGE_LIMIT
            )
        })
    else:
        emit('message', {
            'msg': message['msg'],
            'user': session.get('name'),
            'timestamp': '{0}'.format(datetime.now())
        }, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    messages = []
    msg_count = 0
    leave_room(room)
    emit('status', {
        'msg': session.get('name') + ' has left the room.'
    }, room=room)
