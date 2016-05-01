import 'package:image/image.dart';
import 'dart:html';

class GameImage
{
  Image image;
  bool loaded;

  int get width => loaded ? image.width : 0;
  int get height => loaded ? image.height : 0;

  GameImage.fromUrl(String url)
  {
    loaded = false;

    //Create an ImageElement to use built in image loading
    ImageElement imgElement = new ImageElement(src: url);
    imgElement.onLoad.listen((e) {

      //When the image is loaded, render it to a canvas
      CanvasElement renderCanvas =
      new CanvasElement();

      renderCanvas.width = imgElement.width;
      renderCanvas.height = imgElement.height;

      CanvasRenderingContext2D ctx = renderCanvas.getContext("2d");
      ctx.drawImage(imgElement, 0, 0);

      //Get the ImageData from the canvas
      ImageData imageData = renderCanvas.context2D.
      getImageData(0, 0, renderCanvas.width, renderCanvas.height);

      //Create a new image from the canvas data
      image = new Image.fromBytes(renderCanvas.width, renderCanvas.height, imageData.data);

      loaded = true;
    });
  }

  GameImage.from(GameImage other)
  {
    image = new Image.from(other.image);

    loaded = true;
  }

  GameImage.fromRectangle(int width, int height, [int r = 0, int g = 0, int b = 0])
  {
    CanvasElement renderCanvas =
    new CanvasElement();

    CanvasRenderingContext2D ctx = renderCanvas.getContext("2d");

    renderCanvas.width = width;
    renderCanvas.height = height;
    ctx.setFillColorRgb(r, g, b);
    ctx.fillRect(0, 0, width, height);

    //Get the ImageData from the canvas
    ImageData imageData = renderCanvas.context2D.
    getImageData(0, 0, renderCanvas.width, renderCanvas.height);

    //Create a new image from the canvas data
    image = new Image.fromBytes(renderCanvas.width, renderCanvas.height, imageData.data);

    loaded = true;
  }
}