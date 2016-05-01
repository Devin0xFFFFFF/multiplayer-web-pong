import 'dart:html';
import 'package:client/game/core/abstract/actor.dart';
import 'package:client/game/core/assets/game_image.dart';

class GameCanvas
{
  int width, height;

  CanvasElement canvas;
  CanvasRenderingContext2D ctx;

  GameCanvas(this.canvas)
  {
    width = canvas.width;
    height = canvas.height;

    ctx = canvas.getContext('2d');
  }

  draw(List<Actor> actors)
  {
    //TODO: draw background

    //Draw each actor
    for(Actor actor in actors)
    {
      drawActor(actor);
    }
  }

  clear()
  {
    ctx..fillStyle = "white"
      ..fillRect(0, 0, canvas.width, canvas.height);
  }

  drawActor(Actor actor)
  {
    if(actor.visible)
    {
      drawImage(actor.image, actor.position);
    }
  }

  drawImage(GameImage image, Point location)
  {
    if(image.loaded)
    {
      var imageData = canvas.context2D.createImageData(image.image.width, image.image.height);
      imageData.data.setRange(0, imageData.data.length, image.image.getBytes());
      // Draw the buffer onto the canvas.
      canvas.context2D.putImageData(imageData, location.x, location.y);
    }
  }
}