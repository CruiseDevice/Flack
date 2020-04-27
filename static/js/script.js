$(document).ready(function(){
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
	console.log(socket);
	socket.on('connect', function(){
		socket.emit('joined',{});
	});

	socket.on('status', function(data) {
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    socket.on('message', function(data) {
        $('#chat').val($('#chat').val() + data.msg + '  ' +moment(data.timestamp).format('MMMM Do YYYY, h:mm:ss a') +'\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
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