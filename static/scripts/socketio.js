document.addEventListener('DOMContentLoaded',() => {
		console.log("oka")
	    var socket = io();
		socket.on('connect',() =>{
			socket.send("Connected");
		});
		socket.on('message',function(msg){
			$('messages').append('<li>'+msg+'</li>');
		}
})