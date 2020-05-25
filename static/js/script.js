$(document).ready(function(){
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    var msg_history = document.getElementById('msg_history');

	socket.on('connect', function(){
		socket.emit('joined',{});
	});

  socket.on('status', function(data) {
    msg_history.innerHTML += data['msg'] + '<br />'
  });

  socket.on('message', function(data) {
    msg_history.innerHTML += `
      <span class="msg_user"><strong>${data['user']}:</strong></span>
      <span class="msg">${data['msg']}</span>
      <small class="text text-muted pull-right">${moment(data['timestamp']).format('MMMM Do YYYY, h:mm:ss a')}</small>
      <br />
    `
  });

  $('#text').keypress(function(e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      text = $('#text').val();
      $('#text').val('');
      if (text !== '')
        socket.emit('text', {msg: text});
    }
  });

  leave_room = function(){
	socket.emit('left', {}, function(){
      socket.disconnect();
      window.location.href = "/";
    });
  }

  window.onunload = () => {
    socket.emit('left', {}, function() {
      socket.disconnect();
    });
  }
});