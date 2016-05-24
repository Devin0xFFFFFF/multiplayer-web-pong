# multiplayer-web-pong
###Online Pong using Websockets and ZMQ

##Project
The goal of this project is to expand my knowledge of the HTML 5 canvas, websockets, and ZeroMQ, and bring them together to form a working client/server online web-based game.

Each client runs in browser, and is created with Angular 2 and Dart.

Clients connect to Client Handlers, dispatched from Websocketd, giving each their own server-side process. The browser communicates over websockets to their handler. The handler communicates to the matchmaking and game servers via ZeroMQ

The matchmaking server will accept requests, add client handlers to a queue, and pairs them off, passing them a reference to a game server.

Client handlers will connect to a Game Server, which runs the actual Pong game, receives input from clients, and publishes commands.

##Resources
- [Websockets](https://github.com/Devin0xFFFFFF/websocket_experiments)
- [ZeroMQ](https://github.com/Devin0xFFFFFF/zmq_experiments)
- [HTML 5 Canvas](https://github.com/Devin0xFFFFFF/html5_canvas_experiments)
- [Angular 2 and Dart](https://github.com/Devin0xFFFFFF/angular2_dart)

##Running Websocketd
- ./websocketd --port=8080 python client_handler
