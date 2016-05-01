import 'package:client/game/core/actor.dart';
import 'package:client/game/paddle.dart';
import 'package:client/game/ball.dart';
import 'package:client/game/core/game_canvas.dart';
import 'package:client/game/core/game_event_manager.dart';
import 'dart:html';

class Game
{
  static const num GAME_SPEED = 15;
  num _lastTimeStamp = 0;

  GameCanvas canvas;
  GameEventManager eventManager;
  List<Actor> actors;

  Paddle paddle1, paddle2;
  Ball ball;

  GameEventManager get keyboard => eventManager;

  int get width => canvas.width;
  int get height => canvas.height;

  Game(this.canvas, this.eventManager)
  {
    actors = new List<Actor>();


    //TODO: remove this test code
    ball = new Ball();
    ball.setImageByUrl('assets/images/cat.png');
    addActor(ball);

    run();
  }

  addActor(Actor actor)
  {
    actor.game = this;
    actors.add(actor);
    actor.init();
  }

  run()
  {
    window.animationFrame.then(update);
  }

  void update(num delta) {
    final num diff = delta - _lastTimeStamp;

    if (diff > GAME_SPEED) {
      _lastTimeStamp = delta;

      canvas.clear();

      //Make the world act
      act();

      //Make each actor act
      for(Actor actor in actors)
      {
        actor.act();
      }

      canvas.draw(actors);
    }

    // keep looping
    run();
  }

  act()
  {

  }
}