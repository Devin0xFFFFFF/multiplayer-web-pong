import 'package:client/game/core/actor.dart';
import 'dart:math';

class Ball extends Actor
{
  int speed;

  Ball()
  {

  }

  @override
  init()
  {
    speed = 10;
    reset();
  }

  @override
  act()
  {
    move(speed);

    if(atGameTopEdge() || atGameBottomEdge())
    {
      bounce();
    }
    else if(atGameLeftEdge() || atGameRightEdge())
    {
      randomizeDirection();
    }

//    if (game.keyboard.isPressed(KeyCode.LEFT))
//    {
//      setPosition(X - speed, Y);
//    }
//    else if (game.keyboard.isPressed(KeyCode.RIGHT))
//    {
//      setPosition(X + speed, Y);
//    }
//    else if (game.keyboard.isPressed(KeyCode.UP))
//    {
//      setPosition(X, Y - speed);
//    }
//    else if (game.keyboard.isPressed(KeyCode.DOWN))
//    {
//      setPosition(X, Y + speed);
//    }
  }

  bounce()
  {
    setRotation(rotation + 270);
  }

  randomizeDirection()
  {
    Random random = new Random();

    setRotation(random.nextInt(360).toDouble());
  }

  reset()
  {
    setPosition(game.width~/2, game.height~/2);
    randomizeDirection();
  }
}