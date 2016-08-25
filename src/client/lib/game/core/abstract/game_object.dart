import 'dart:collection';

import 'package:client/game/core/command.dart';

abstract class GameObject
{
  String ID;
  Queue<Command> commands;

  GameObject(this.ID)
  {
    commands = new Queue<Command>();
  }

  init([dynamic args=null]);

  update(num delta);

  act();

  queueCommand(Command command)
  {
    commands.add(command);
  }
}