import 'dart:mirrors';
import 'package:client/game/core/abstract/game_object.dart';

class Command
{
  String targetID;
  String action;
  List args;

  Command(this.targetID, this.action, [this.args = const []]){}

  Command.from(Map serialization)
  {
    targetID = serialization['targetID'];
    action = serialization['action'];
    args = serialization['args'];
  }

  execute(GameObject target)
  {
    //Invoke a command on a given GameObject
    InstanceMirror mirror = reflect(target);
    mirror.invoke(MirrorSystem.getSymbol(action), args);
  }

  Map serialize()
  {
    return {'targetID': targetID, 'action': action, 'args': args};
  }
}