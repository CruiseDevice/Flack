$(document).ready(function(){
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
	console.log(socket);
    var msg_history = document.getElementById('msg_history');
	socket.on('connect', function(){
		socket.emit('joined',{});
	});

     socket.on('status', function(data) {
        msg_history.innerHTML += data['msg'] + '<br />'
     });

     socket.on('message', function(data) {
        msg_history.innerHTML += data['msg'] + '<br />'
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