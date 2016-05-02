import 'package:client/game/core/abstract/command_router.dart';
import 'package:client/game/core/command.dart';
import 'package:client/io/websocket_client.dart';
import 'dart:convert';
import 'package:client/game/core/routers/game_router.dart';

class ClientRouter extends CommandRouter {
  GameRouter gameRouter;
  WebsocketClient client;

  ClientRouter(this.gameRouter, this.client) {
    client.listen(handleIncoming);
    client.connect();
  }

  @override
  route(Command command) {
    client.send(command.serialize());
  }

  handleIncoming(dynamic data) {
    dynamic message = JSON.decode(data);

    if (message is Map) {
      String messageType = message['HEAD'];

      switch(messageType)
      {
        case 'CLIENT_STATUS.CONNECT' :
        case 'CLIENT_STATUS.DISCONNECT' :
        case 'CLIENT_STATUS.ERROR' :
          print(messageType);
          break;
        case 'CMD':
          Command command = new Command.from((message['BODY']));
          gameRouter.route(command);
          break;
      }

    } else {
      throw new Exception('Invalid message received: ${message}');
    }
  }
}
