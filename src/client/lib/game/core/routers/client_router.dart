import 'package:client/game/core/abstract/command_router.dart';
import 'package:client/game/core/command.dart';
import 'package:client/io/websocket_client.dart';
import 'dart:convert';
import 'package:client/game/core/routers/game_router.dart';

class ClientRouter extends CommandRouter {
  GameRouter gameRouter;
  WebsocketClient client;

  static final String VERSION = "mpwp0.1";
  static final int OK_STATUS = 100;

  String client_id;
  String game_id;


  ClientRouter(this.gameRouter, this.client) {
    client.listen(handleIncoming);
    client.connect();
  }

  @override
  route(Command command) {
    //print(command.serialize());
    String JSONCMD = JSON.encode(command.serialize());
    String msg = VERSION + " " + OK_STATUS.toString() + " " + JSONCMD;
    print(msg);
    client.send(msg);
  }

  handleIncoming(dynamic data) {
    dynamic message = '';

    try
    {
      message = JSON.decode(data);
    }
    catch(e){}

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
        default :
          print(message['BODY']);
      }

    } else {
      //TODO: figure out how to handle invalid messages cleanly
      //throw new Exception('Invalid message received: ${message}');
    }
  }
}
