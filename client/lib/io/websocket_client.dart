import 'dart:html';
import 'package:angular2/core.dart';
import 'package:client/io/client.dart';
import 'package:client/config.dart';

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
      recv(CLIENT_STATUS.CONNECT);
    });

    _ws.onMessage.listen((MessageEvent e){
      recv(e.data);
    });

    _ws.onClose.listen((Event e) {
      print('Connection closed.');
      recv(CLIENT_STATUS.DISCONNECT);
    });

    _ws.onError.listen((Event e){
      print('Connection error occurred!');
      recv(CLIENT_STATUS.ERROR);
    });
  }

  @override
  send(dynamic data)
  {
    _ws.send(data);
  }
}