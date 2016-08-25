import 'dart:html';

import 'package:client/game/actors/ball.dart';
import 'package:client/game/actors/paddle.dart';
import 'package:client/game/core/abstract/actor.dart';
import 'package:client/game/core/abstract/command_router.dart';
import 'package:client/game/core/abstract/game_object.dart';
import 'package:client/game/core/assets/game_image.dart';
import 'package:client/game/core/game_canvas.dart';
import 'package:client/game/core/game_event_manager.dart';
import 'package:client/game/core/player.dart';
import 'package:client/game/core/command.dart';

class Game extends GameObject
{
  static const num GAME_SPEED = 15;
  num _lastTimeStamp = 0;

  GameCanvas canvas;
  GameEventManager eventManager;

  dynamic sendCommandsCB;

  List<Player> players;
  List<Actor> actors;

  Player player;
  Paddle paddle1, paddle2;
  Ball ball;

  int paddle1Score, paddle2Score;

  GameEventManager get keyboard => eventManager;

  int get width => canvas.width;
  int get height => canvas.height;

  Game(this.canvas, this.eventManager) : super('game')
  {
    players = new List<Player>();
    actors = new List<Actor>();

    //TODO: remove this test code

    ball = new Ball('ball');
    ball.setImageByUrl('assets/images/cat.png');
    addActor(ball);

    paddle1 = new Paddle('paddle1');
    paddle1.setImage(new GameImage.fromRectangle(20, 200, 0, 0, 0));
    addActor(paddle1, 20, height~/2);

    paddle2 = new Paddle('paddle2');
    paddle2.setImage(new GameImage.fromRectangle(20, 200, 0, 0, 0));
    addActor(paddle2, width - 20, height~/2);

    paddle1Score = paddle2Score = 0;

    run();
  }

  @override
  init([dynamic args=null])
  {
    assert(args != null);
    assert(args is List);
    String paddle = args[0];
    this.sendCommandsCB = args[1];
    if(paddle == paddle1.ID)
    {
      this.player = new Player(paddle1);
    }
    else
    {
      this.player = new Player(paddle2);
    }

    addPlayer(player);
  }

  addPlayer(Player player)
  {
    player.game = this;
    players.add(player);
  }

  addActor(Actor actor, [int width = 0, int height = 0])
  {
    actor.game = this;
    actors.add(actor);
    actor.setPosition(width, height);
    actor.init(null);
  }

  getActor(String ID)
  {
    Actor actor = null;
    int  i = 0;

    while(i < actors.length && actor == null)
    {
      if(actors[i].ID == ID)
      {
        actor = actors[i];
      }
      i++;
    }

    return actor;
  }

  run()
  {
    window.animationFrame.then(update);
  }

  void update(num delta) {
    final num diff = delta - _lastTimeStamp;
    List<Command> commands;

    if (diff > GAME_SPEED) {
      _lastTimeStamp = delta;

      canvas.clear();

      commands = [];

      //Handle player commands
      for(Player player in players)
      {
        player.run();
        commands.addAll(player.getCommands());
      }

      //Make the world act
      act();

      //Make each actor act
      for(Actor actor in actors)
      {
        actor.update(delta);
      }

      canvas.draw(actors);

      this.sendCommandsCB(commands);
    }

    // keep looping
    run();
  }

  act()
  {
    if(ball.atGameLeftEdge())
    {
      paddle1Score++;
      ball.reset();
    }
    else if(ball.atGameRightEdge())
    {
      paddle2Score++;
      ball.reset();
    }
  }

  void applyState(Map states)
  {
    //TODO: make the state easier to read, include proper data
    states.forEach((String id, List state){
      Actor actor = this.getActor(id);
      actor.visible = state[0];
      actor.position = new Point(state[1], state[2]);
      actor.rotation = state[5].toDouble();
    });
  }
}