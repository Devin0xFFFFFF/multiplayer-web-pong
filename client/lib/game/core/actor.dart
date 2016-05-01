import 'dart:math';
import 'package:client/game/core/game_image.dart';
import 'package:client/game/core/game.dart';

abstract class Actor
{
  Game game;

  Point position;
  double rotation;
  bool visible;

  GameImage image;
  int collisionBuffer;

  int get X => position.x;
  int get Y => position.y;

  Actor([this.position = const Point(0, 0), this.rotation = 0.0])
  {
    visible = true;
    collisionBuffer = 10;
  }

  init();

  act();

  setPosition(int x, int y)
  {
    position = new Point(x, y);
  }

  setRotation(double angle)
  {
    //Maintain an angle within 360 degrees
    rotation = angle % 360;
  }

  setImageByUrl(String url)
  {
    this.image = new GameImage.fromUrl(url);
  }

  setImage(GameImage image)
  {
    this.image = new GameImage.from(image);
  }

  move(int speed)
  {
    double angle = rotation * (PI / 180.0);
    int x = (X + cos(angle) * speed).round();
    int y = (Y + sin(angle) * speed).round();

    setPosition(x, y);
  }

  Rectangle getBoundingBox()
  {
    //Add a buffer to give some space for collisions
    return new Rectangle(
        X - collisionBuffer,
        Y - collisionBuffer,
        image.width + collisionBuffer,
        image.height + collisionBuffer);
  }

  bool intersecting(Actor other)
  {
    return getBoundingBox().intersects(other.getBoundingBox());
  }

  bool intersectingPosition(Point pos)
  {
    return getBoundingBox().containsPoint(pos);
  }

  atGameTopEdge()
  {
    return Y < collisionBuffer;
  }

  atGameBottomEdge()
  {
    return Y > game.height - collisionBuffer;
  }

  atGameLeftEdge()
  {
    return X < collisionBuffer;
  }

  atGameRightEdge()
  {
    return X > game.width - collisionBuffer;
  }
}