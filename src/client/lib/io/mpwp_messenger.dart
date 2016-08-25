import 'dart:convert';

import 'package:angular2/core.dart';
import 'package:client/io/mpwp_message.dart';
import 'package:client/io/websocket_client.dart';

enum MessengerState
{
  OPEN, CLOSED
}

@Injectable()
class MPWPMessenger
{
  EventEmitter<MPWPMessage> received;

  MessengerState state;
  WebsocketClient client;

  MPWPMessenger(this.client)
  {
    this.state = MessengerState.CLOSED;
    this.received = new EventEmitter<MPWPMessage>();
    this.client.listen(handleIncoming);
  }

  connect(onConnect)
  {
    this.client.connect();
    this.client.setOnConnect(onConnect);
  }

  handleIncoming(dynamic data)
  {
    MPWPMessage message;
    dynamic decoded;

    try
    {
      decoded = JSON.decode(data);
    }
    catch(e){
      throw new Exception("Failed to Decode Incoming Message: " + data);
    }

    assert(decoded is Map);
    decoded = decoded['data'];
    assert(decoded is List);
    message = new MPWPMessage(decoded);

    this.received.add(message);
  }

  listen(onEvent)
  {
    this.received.listen(onEvent);
  }

  send(MPWPMessage msg)
  {
    Map packed = {"data": msg.message};
    String serialized = JSON.encode(packed);
    this.client.send(serialized);
  }
}