import 'dart:html';

import 'package:angular2/core.dart';
import 'package:client/config.dart';
import 'package:client/io/abstract_client.dart';

@Injectable()
class WebsocketClient extends AbstractClient
{
  WebSocket _ws;

  WebsocketClient(GameConfig config) : super(config.SERVER_IP, config.SERVER_PORT);

  @override
  connect()
  {
    String url = 'ws://' + ip + ':' + port;

    print('Conntecting to $url...');

    _ws = new WebSocket(url);

    _ws.onOpen.listen((Event e) {
      print('Connected.');
      if(this.onConnect != null)
      {
        this.onConnect();
      }
    });

    _ws.onMessage.listen((MessageEvent e){
      recv(e.data);
    });

    _ws.onClose.listen((Event e) {
      _ws = null;
      print('Connection closed.');
    });

    _ws.onError.listen((Event e){
      print('Connection error occurred!');
    });
  }

  @override
  send(dynamic data)
  {
    if(_ws != null)
    {
      _ws.send(data);
    }
  }
}