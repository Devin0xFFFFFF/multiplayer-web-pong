import 'package:client/game/core/abstract/actor.dart';
import 'dart:html';

class Paddle extends Actor
{

  int speed;

  Paddle(String ID) : super(ID);
  
  @override
  init(dynamic args) {
    speed = 10;
  }

  @override
  act() {
//    if (game.keyboard.isPressed(KeyCode.UP) && !atGameTopEdge())
//    {
//      setPosition(X, Y - speed);
//    }
//    else if (game.keyboard.isPressed(KeyCode.DOWN) && !atGameBottomEdge())
//    {
//      setPosition(X, Y + speed);
//    }
  }
}