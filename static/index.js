document.addEventListener('DOMContentLoaded', () => {

    //connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    //when connected, configure buttons
    socket.on('connect', () => {
        //send message button should emit a send message event
        document.querySelector('#send').onclick = () => {
            const message = document.querySelector('#message').value;
            const channel = document.title;
           socket.emit('send message', {'message': message, 'channel':channel } );
        }
    })

    socket.on('update messages', data => {
        const li = document.createElement('li');
        li.innerHTML = data.message;
        document.querySelector('#messages').append(li);
    })
})