import 'package:client/game/core/abstract/command_router.dart';
import 'package:client/game/core/command.dart';

abstract class GameCommander
{
  CommandRouter endpoint;
  Command command;

  GameCommander(this.endpoint);

  static int count = 0;

  sendCommand(Command command)
  {
    this.command = command;
  }

  pushCommand()
  {
    if(command != null) {
      endpoint.route(command);
      command = null;
      //print(count++);
    }
  }
}