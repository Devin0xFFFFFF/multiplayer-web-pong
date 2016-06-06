# multiplayer-web-pong
###Online Pong using Websockets and ZMQ

##Project
The goal of this project is to expand my knowledge of the HTML 5 canvas, websockets, and ZeroMQ, and bring them together to form a working client/server online web-based game.

Each client runs in browser, and is created with Angular 2 and Dart.

Clients connect to Client Handlers, dispatched from Websocketd, giving each their own server-side process. The browser communicates over websockets to their handler. The handler communicates to the matchmaking and game servers via ZeroMQ

The matchmaking server will accept requests, add client handlers to a queue, and pairs them off, passing them a reference to a game server.

Client handlers will connect to a Game Manager Server, which runs the game instances of the actual Pong game, receives input from clients, and publishes commands.

##Resources
- [Websockets](https://github.com/Devin0xFFFFFF/websocket_experiments)
- [ZeroMQ](https://github.com/Devin0xFFFFFF/zmq_experiments)
- [HTML 5 Canvas](https://github.com/Devin0xFFFFFF/html5_canvas_experiments)
- [Angular 2 and Dart](https://github.com/Devin0xFFFFFF/angular2_dart)

##Running Websocketd
- ./websocketd --port=8080 python client_handler

##Network Protocol
Game data packets from the client are serialized into JSON

A client will send a message of the form: client_id game_id { data: [ game_id, message_type, { message_args } ] }
- game_id is a UUID representing a game instance
- client_id is a UUID representing a client connection
- message_type is an integer representing the type of message, such as COMMAND(0)
- { message_args } is a dictionary of arguments specific to the message_type

A client handler will take this message and parse it into a multi-part message of the form: [head] [status] [to] [from] [data]
The parser will split the message from a single string and do a check to make sure it is the correct client connected
- HEAD is an application identifier for the server to verify the client is running the correct version, such as mpwp_0.1
- STATUS is a message status code, used for differntiating between valid, error, and heartbeat messages
- TO is an identifier UUID for the message target, defaults to 0 for unknown reciever, client to a game, game_id
- FROM is an identifer UUID for the message sender, for a client, this would be the client_id, for a game, game_id
- DATA is the aforementioned valid JSON message { data: ... }

The game server will check for a valid HEAD, then decide on what to do based on STATUS
Any messages with an invalid HEAD will send back an error response

For a valid message:
- parse TO and FROM to get GID and CID respectively
- check GID and CID, see if there is a valid game instance with that id and that client
- if valid, forward the message to the game instance in the form: [CID] [TYPE] [ARGS]
- ARGS will be stringified

For an error:
- check STATUS against error codes, act accordingly

For a heartbeat:
- respond with a heartbeat packet with valid HEAD, heartbeat STATUS, and empty data
- heartbeats are to make sure clients and servers are running, network is up
- client_handlers are in charge of making sure both clients and servers are active
- clients also send heatbeat packets when no data has been recieved for some set interval
- client heartbeats will be a single byte, rather than a normal JSON message

