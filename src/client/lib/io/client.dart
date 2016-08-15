import 'package:angular2/core.dart';
import 'dart:convert';

enum CLIENT_STATUS
{
  CONNECT, ERROR, DISCONNECT
}

abstract class Client
{
  String ip, port;
  EventEmitter<dynamic> received;

  Client(this.ip, this.port)
  {
    received =  new EventEmitter();
  }

  connect();

  send(dynamic data);

  recv(dynamic data)
  {
    received.add(data);
  }

  listen(onEvent)
  {
    received.listen(onEvent);
  }

  recvStatus(CLIENT_STATUS STATUS)
  {
    recv(JSON.encode({'HEAD': STATUS.toString(), 'BODY': {}}));
  }
}