import 'package:client/game/core/abstract/command_router.dart';
import 'package:client/game/core/command.dart';
import 'package:client/io/websocket_client.dart';
import 'dart:convert';
import 'package:client/game/core/routers/game_router.dart';

class ClientRouter extends CommandRouter
{
  GameRouter gameRouter;
  WebsocketClient client;

  ClientRouter(this.gameRouter, this.client)
  {
    client.listen(handleIncoming);
  }

  @override
  route(Command command)
  {
    client.send(command.serialize());
  }

  handleIncoming(dynamic data)
  {
    Map message = JSON.decode(data);

    if(message['HEAD'] == 'COMMAND')
    {
      Command command = new Command.from((message['BODY']));
      gameRouter.route(command);
    }
    else
    {
      //TODO: handle other kinds of messages, like CONNECT
      print(message);
    }
  }
}