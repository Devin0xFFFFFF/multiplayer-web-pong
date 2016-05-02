import 'dart:html';
import 'package:angular2/core.dart';
import 'package:client/io/client.dart';
import 'package:client/config.dart';
import 'dart:convert';

@Injectable()
class WebsocketClient extends Client
{
  WebSocket _ws;

  WebsocketClient(GameConfig config) : super(config.IP, config.PORT);

  @override
  connect()
  {
    String url = 'ws://' + ip + ':' + port;

    print('Conntecting to $url...');

    _ws = new WebSocket(url);

    _ws.onOpen.listen((Event e) {
      print('Connected.');
      recvStatus(CLIENT_STATUS.CONNECT);
    });

    _ws.onMessage.listen((MessageEvent e){
      recv(e.data);
    });

    _ws.onClose.listen((Event e) {
      print('Connection closed.');
      recvStatus(CLIENT_STATUS.DISCONNECT);
    });

    _ws.onError.listen((Event e){
      print('Connection error occurred!');
      recvStatus(CLIENT_STATUS.ERROR);
    });
  }

  @override
  send(dynamic data)
  {
    if(_ws != null)
    {
      _ws.send(JSON.encode(data));
    }
  }
}