import 'package:client/game/core/abstract/command_router.dart';
import 'package:client/game/core/command.dart';
import 'package:client/game/core/abstract/actor.dart';
import 'package:client/game/core/game.dart';

class GameRouter extends CommandRouter
{
  Game game;

  GameRouter(this.game)
  {

  }

  @override
  route(Command command) {

    if(game == null)
    {
      throw new Exception('Game not initialized!');
    }

    Actor target = game.getActor(command.targetID);
    if(target != null)
    {
      target.queueCommand(command);
    }
    else
    {
      throw new Exception('Actor with ID ${command.targetID} does not exist!');
    }
  }
}