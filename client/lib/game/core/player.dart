import 'package:client/game/core/abstract/game_commander.dart';
import 'package:client/game/core/game.dart';
import 'dart:html';
import 'package:client/game/actors/paddle.dart';
import 'package:client/game/core/abstract/command_router.dart';
import 'package:client/game/core/command.dart';

class Player extends GameCommander
{
  Game game;
  Paddle paddle;

  Player(CommandRouter endpoint, this.paddle) : super(endpoint)
  {

  }

  run()
  {
    handleInput();
  }

  handleInput()
  {
    if (game.keyboard.isPressed(KeyCode.UP) && !paddle.atGameTopEdge())
    {
      sendCommand(new Command(paddle.ID, 'setPosition', [paddle.X, paddle.Y - paddle.speed]));
      //paddle.setPosition(paddle.X, paddle.Y - paddle.speed);
    }
    else if (game.keyboard.isPressed(KeyCode.DOWN) && !paddle.atGameBottomEdge())
    {
      sendCommand(new Command(paddle.ID, 'setPosition', [paddle.X, paddle.Y + paddle.speed]));
//      paddle.setPosition(paddle.X, paddle.Y + paddle.speed);
    }
  }
}