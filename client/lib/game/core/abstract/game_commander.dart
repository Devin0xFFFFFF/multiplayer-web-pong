import 'package:client/game/core/game.dart';
import 'package:client/game/core/command.dart';
import 'package:client/game/core/abstract/command_router.dart';

abstract class GameCommander
{
  CommandRouter endpoint;

  GameCommander(this.endpoint);

  sendCommand(Command command)
  {
    endpoint.route(command);
  }
}