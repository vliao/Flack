document.addEventListener('DOMContentLoaded', () => {

    //connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    //when connected, configure buttons
    socket.on('connect', () => {

        //Sign in button should emit a sign in event
        document.querySelector('#signIn').onclick = () => {
            const user = document.querySelector('#user').value;
           socket.emit('sign in', {'user': user } );
        }
    })


    // when the user is signed in, alert. 
    socket.on('sign in', data => {
        alert(`${data.user} is signed in`)
        socket.emit('')
    })
})