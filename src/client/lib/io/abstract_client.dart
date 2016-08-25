import 'package:angular2/core.dart';

enum CLIENT_STATUS
{
  CONNECT, ERROR, DISCONNECT
}

abstract class AbstractClient
{
  String ip, port;
  EventEmitter<dynamic> received;
  dynamic onConnect;

  AbstractClient(this.ip, this.port)
  {
    received = new EventEmitter();
  }

  connect();

  void setOnConnect(onConnect)
  {
    this.onConnect = onConnect;
  }

  send(dynamic data);

  recv(dynamic data)
  {
    received.add(data);
  }

  listen(onEvent)
  {
    received.listen(onEvent);
  }
}