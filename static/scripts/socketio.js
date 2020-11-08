document.addEventListener('DOMContentLoaded',() => {
	    var socket = io();
		socket.on('connect',() =>{
			socket.send("Connected");
		});
		socket.on('message',data =>{
			const p = document.createElement('p');
			const br = document.createElement('br');
			p.innerHTML = data;
			document.querySelector('#display_messages_area').append(p); 
		});
		document.querySelector('#send_message').onclick = () => {
			socket.send(document.querySelector('#user_message').value);
		}
})