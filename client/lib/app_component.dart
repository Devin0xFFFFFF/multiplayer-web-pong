// Copyright (c) 2016, <your name>. All rights reserved. Use of this source code
// is governed by a BSD-style license that can be found in the LICENSE file.

import 'package:angular2/core.dart';
import 'package:client/io/websocket_client.dart';
import 'package:client/game/game_component.dart';
import 'package:client/config.dart';
import 'package:client/io/client.dart';

@Component(selector: 'my-app',
    templateUrl: 'app_component.html',
    directives: const [GameComponent],
    providers:  const [GameConfig, WebsocketClient])
class AppComponent
{
  WebsocketClient client;

  bool searching, playing;

  AppComponent(this.client)
  {
    searching = false;
    playing = true;

    client.listen(processServerInput);
  }

  connect()
  {
    searching = true;
    client.connect();
  }

  processServerInput(dynamic input)
  {
    if(input == CLIENT_STATUS.DISCONNECT)
    {
      print('Lost connection to server!');
    }
    print(input);
  }
}
