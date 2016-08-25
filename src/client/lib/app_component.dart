// Copyright (c) 2016, <your name>. All rights reserved. Use of this source code
// is governed by a BSD-style license that can be found in the LICENSE file.

import 'package:angular2/core.dart';
import 'package:client/config.dart';
import 'package:client/game/game_component.dart';
import 'package:client/io/websocket_client.dart';
import 'package:client/io/mpwp_messenger.dart';
import 'package:client/mpwp_client.dart';

@Component(selector: 'my-app',
    templateUrl: 'app_component.html',
    directives: const [GameComponent],
    providers:  const [GameConfig, WebsocketClient, MPWPMessenger, MPWPClient])
class AppComponent
{
  MPWPClient client;

  AppComponent(this.client)
  {

  }

  bool get started => client.state == ClientState.PLAYING;
  bool get waiting => client.state == ClientState.WAITING;
  bool get searching => client.state == ClientState.SEARCHING;
  bool get found => client.state == ClientState.FOUND;
  bool get loading => client.state == ClientState.LOADING;
  bool get launching => client.state == ClientState.LAUNCHING;
  bool get playing => client.state == ClientState.PLAYING;
  bool get blocked => client.state == ClientState.BLOCKED;

  enqueueMM()
  {
    client.sendMMEnqueue();
  }

  dequeueMM()
  {
    client.sendMMDequeue();
  }

  acceptMM()
  {
    client.sendMMAccept();
  }

  declineMM()
  {
    client.sendMMDecline();
  }
}
