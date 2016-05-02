import 'package:client/game/core/abstract/actor.dart';
import 'dart:math';

class Ball extends Actor
{
  int speed;

  Ball(String ID) : super(ID);

  @override
  init(dynamic args)
  {
    speed = 10;
    reset();
  }

  @override
  act()
  {
    //move(speed);

    if(atGameTopEdge() || atGameBottomEdge())
    {
      bounce();
    }
  }

  bounce([int variance = 0])
  {
    setRotation(rotation + 270 + variance);
  }

  randomizeDirection()
  {
    Random random = new Random();

    //Make sure the rotation is either left or right focused
    double randomAngle = random.nextInt(45).toDouble();
    int randomDirection = random.nextInt(4);
    double randomRotation = 0.0;

    switch(randomDirection)
    {
      case 0 : randomRotation = randomAngle;
        break;
      case 1 : randomRotation = 180 - randomAngle;
        break;
      case 2 : randomRotation = 180 + randomAngle;
        break;
      case 3 : randomRotation = 360 - randomAngle;
    }

    setRotation(randomRotation);
  }

  reset()
  {
    setPosition(game.width~/2, game.height~/2);
    randomizeDirection();
  }
}