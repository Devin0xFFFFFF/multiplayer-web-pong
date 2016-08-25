import 'package:client/game/core/abstract/command_router.dart';
import 'package:client/game/core/command.dart';

abstract class GameCommander
{
  Command command;

  GameCommander()
  {
    this.command = null;
  }

  sendCommand(Command command)
  {
    this.command = command;
  }

  List<Command> getCommands()
  {
    List<Command> cmds = [];
    if(this.command != null)
    {
      cmds.add(this.command);
      this.command = null;
    }
    return cmds;
  }
}