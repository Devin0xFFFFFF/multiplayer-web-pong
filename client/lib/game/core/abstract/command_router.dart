import 'package:client/game/core/command.dart';

abstract class CommandRouter
{
  route(Command command);
}