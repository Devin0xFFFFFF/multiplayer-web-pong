import 'dart:mirrors';
import 'package:client/game/core/abstract/game_object.dart';
import 'dart:convert';

class Command
{
  String targetID;
  String action;
  List args;

  Command(this.targetID, this.action, [this.args = const []]){}

  Command.from(List serialization)
  {
    targetID = serialization[0];
    action = serialization[1];
    args = serialization[2];
  }

  execute(GameObject target)
  {
    //Invoke a command on a given GameObject
    InstanceMirror mirror = reflect(target);
    mirror.invoke(MirrorSystem.getSymbol(action), args);
  }

  String serialize()
  {
    return JSON.encode([targetID, action,  args]);
  }
}