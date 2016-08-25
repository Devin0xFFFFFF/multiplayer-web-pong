import 'package:angular2/core.dart';
import 'dart:html';
import 'package:client/game/core/game.dart';
import 'package:client/game/core/game_canvas.dart';
import 'package:client/game/core/game_event_manager.dart';
import 'package:client/io/websocket_client.dart';
import 'package:client/mpwp_client.dart';

@Component(selector: 'my-game',
    templateUrl: 'game_component.html',
    directives: const [],
    providers: const [])
class GameComponent implements AfterViewInit
{
  CanvasElement canvas;
  GameCanvas gameCanvas;
  GameEventManager eventManager;

  Game game;
  MPWPClient client;

  GameComponent(this.client)
  {

  }

  @override
  ngAfterViewInit()
  {
    canvas = querySelector('#canvas')..focus();

    this.gameCanvas = new GameCanvas(canvas);
    this.eventManager = new GameEventManager();

    this.game = new Game(this.gameCanvas, this.eventManager);

    this.client.init(this.game);
  }
}