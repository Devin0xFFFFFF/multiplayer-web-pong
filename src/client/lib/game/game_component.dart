import 'package:angular2/core.dart';
import 'dart:html';
import 'package:client/game/core/game.dart';
import 'package:client/game/core/game_canvas.dart';
import 'package:client/game/core/game_event_manager.dart';
import 'package:client/io/websocket_client.dart';
import 'package:client/game/core/routers/client_router.dart';
import 'package:client/game/core/routers/game_router.dart';

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
  GameRouter gameRouter;

  ClientRouter clientRouter;
  WebsocketClient client;

  GameComponent(this.client)
  {

  }

  @override
  ngAfterViewInit()
  {
    canvas = querySelector('#canvas')..focus();

    gameCanvas = new GameCanvas(canvas);
    eventManager = new GameEventManager();

    game = new Game(gameCanvas, eventManager);

    gameRouter = new GameRouter(game);
    clientRouter = new ClientRouter(gameRouter, client);

    game.init(clientRouter);
  }
}