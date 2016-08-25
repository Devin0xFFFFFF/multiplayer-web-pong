import 'package:angular2/core.dart';
import 'package:client/io/mpwp_message.dart';
import 'package:client/io/mpwp_protocol.dart';
import 'package:client/game/core/game.dart';
import 'package:client/io/mpwp_messenger.dart';
import 'dart:async';
import 'dart:convert';
import 'package:client/game/core/command.dart';

enum ClientState
{
  STARTED, WAITING, CONNECTING, SEARCHING, FOUND, LOADING, LAUNCHING, PLAYING, BLOCKED
}

@Injectable()
class MPWPClient
{
  static final int FOUND_TIMEOUT = 10;
  static final int LOADING_TIMEOUT = 10;
  static final int LAUNCH_TIMEOUT = 10;
  static final int BLOCKED_TIMEOUT = 10;

  String CID;
  String GID;
  ClientState state;
  Game game;
  String paddleID;
  MPWPMessenger messenger;
  int _msgnum;
  Timer _timer;

  MPWPClient(this.messenger)
  {
    this.CID = null;
    this.GID = null;

    this._msgnum = 0;

    this.state = ClientState.STARTED;

    this.messenger.listen(handleIncoming);
    this.messenger.connect(sendRegisterClient);
  }

  void init(Game game)
  {
    this.game = game;
    this.game.init([this.paddleID, this.sendGameCommands]);
  }

  int getMsgnum()
  {
    return this._msgnum++;
  }

  void sendRegisterClient()
  {
    sendConnect(MPWPProtocol.CLIENT_HANDLER_ID, "");
  }

  void sendConnect(to, from)
  {
    MPWPMessage msg = MPWPProtocol.getStatusMessage(MPWPProtocol.STATUS_CONNECT,
        to, from);

    this.messenger.send(msg);
  }

  void sendGameCommands(List<Command> commands)
  {
    for(Command cmd in commands)
    {
      MPWPMessage msg = getGameMessage(MPWPProtocol.GAME_INPUT, [cmd.serialize()]);
      this.messenger.send(msg);
    }
  }

  void sendMMEnqueue()
  {
    this.messenger.send(getMatchmakerMessage(MPWPProtocol.MATCHMAKER_ENQUEUE));
    this.state = ClientState.SEARCHING;
  }

  void sendMMDequeue()
  {
    this.messenger.send(getMatchmakerMessage(MPWPProtocol.MATCHMAKER_DEQUEUE));
    this.state = ClientState.WAITING;
  }

  void sendMMAccept()
  {
    this.messenger.send(getMatchmakerMessage(MPWPProtocol.MATCHMAKER_ACCEPT));
    this._timer.cancel(); //cancel found timer
  }

  void sendMMDecline()
  {
    this.messenger.send(getMatchmakerMessage(MPWPProtocol.MATCHMAKER_DECLINE));
    this._timer.cancel(); //cancel found timer
    block();
  }

  void sendDisconnect()
  {
    MPWPMessage msg = MPWPProtocol.getStatusMessage(MPWPProtocol.STATUS_DISCONNECT,
        MPWPProtocol.CLIENT_HANDLER_ID,
        this.CID);
    this.messenger.send(msg);
  }

  void sendGameJoinMatch()
  {
    MPWPMessage msg = MPWPProtocol.getStatusMessage(MPWPProtocol.STATUS_REGISTER,
        this.GID,
        this.CID);
    this.messenger.send(msg);
    this._timer = new Timer(new Duration(seconds: LAUNCH_TIMEOUT), _launchTimeout);
  }

  void block()
  {
    this.state = ClientState.BLOCKED;
    this._timer = new Timer(new Duration(seconds: BLOCKED_TIMEOUT), _blockedTimeout);
  }

  MPWPMessage getMatchmakerMessage(String type)
  {
    return MPWPProtocol.getMessage(MPWPProtocol.STATUS_DATA,
        MPWPProtocol.MATCHMAKER_ID, this.CID, 0, type);
  }

  MPWPMessage getGameMessage(String type, List<dynamic> content)
  {
    return MPWPProtocol.getMessage(MPWPProtocol.STATUS_DATA,
        this.GID, this.CID, getMsgnum(), type, content);
  }

  void launchGame(GID)
  {
    this.GID = GID;
    this.state = ClientState.LAUNCHING;
    this._timer.cancel(); //cancel loading timer
    sendDisconnect();
    sendConnect(MPWPProtocol.GAME_MANAGER_ID, this.CID);
  }

  _foundTimeout()
  {
    block();
  }

  _launchTimeout()
  {
    this.state = ClientState.WAITING;
  }

  _loadingTimeout()
  {
    this.state = ClientState.WAITING;
  }

  _blockedTimeout()
  {
    this.state = ClientState.WAITING;
  }

  handleIncoming(MPWPMessage message)
  {
    if(message.status == MPWPProtocol.STATUS_DATA)
    {
      if(message.from == GID)
      {
        if(message.type == MPWPProtocol.GAME_STATE)
        {
          Map state = JSON.decode(message.content[0]);
          game.applyState(state);
        }
      }
      else if(message.from == MPWPProtocol.MATCHMAKER_ID)
      {
        if(message.type == MPWPProtocol.MATCHMAKER_FOUND)
        {
          this.state = ClientState.FOUND;
          this._timer = new Timer(new Duration(seconds: FOUND_TIMEOUT), _foundTimeout);
        }
        else if(message.type == MPWPProtocol.MATCHMAKER_LOADING)
        {
          this.state = ClientState.LOADING;
          this._timer = new Timer(new Duration(seconds: FOUND_TIMEOUT), _loadingTimeout);
        }
        else if(message.type == MPWPProtocol.MATCHMAKER_LAUNCH)
        {
          launchGame(message.content[0]); //configure GID, connect to Game Manager
        }
      }
    }
    else if(message.status == MPWPProtocol.STATUS_CONNECT_OK)
    {
      if(message.from == MPWPProtocol.CLIENT_HANDLER_ID)
      {
        assert(CID == null);
        this.CID = message.to;
        sendConnect(MPWPProtocol.MATCHMAKER_ID, CID); //connected to Client Handler
      }
      else if(message.from == MPWPProtocol.MATCHMAKER_ID)
      {
        this.state = ClientState.WAITING; //actually connected, ready to queue
      }
      else if(message.from == MPWPProtocol.GAME_MANAGER_ID)
      {
        sendGameJoinMatch(); //connect to game instance and register
      }
    }
    else if(message.status == MPWPProtocol.STATUS_REGISTER_OK)
    {
      if(message.from == this.GID)
      {
        //TODO: set paddle to the REGISTER call OR add another message
        this.paddleID = "paddle1";
        this.state = ClientState.PLAYING;
        this._timer.cancel(); //stop timer, register confirmed, launching done
      }
    }
  }
}