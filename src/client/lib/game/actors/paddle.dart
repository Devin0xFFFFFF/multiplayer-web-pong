import 'package:client/game/core/abstract/actor.dart';

class Paddle extends Actor
{

  int speed;

  Paddle(String ID) : super(ID);
  
  @override
  init([dynamic args=null]) {
    speed = 10;
  }

  @override
  act() {

  }
}