import 'package:client/io/mpwp_message.dart';

class MPWPProtocol
{
  static final int MSG_VERSION = 0;
  static final int MSG_STATUS = 1;
  static final int MSG_TO = 2;
  static final int MSG_FROM = 3;
  static final int MSG_MSGNUM = 4;
  static final int MSG_TYPE = 5;
  static final int MSG_CONTENT = 6;

  static final String VERSION = "mpwp_v1.0";

  static final String STATUS_DATA = "100";
  static final String STATUS_PING = "101";

  static final String STATUS_CONNECT = "200";
  static final String STATUS_CONNECT_OK = "201";
  static final String STATUS_DISCONNECT = "202";
  static final String STATUS_REGISTER = "203";
  static final String STATUS_REGISTER_OK = "204";
  static final String STATUS_RESYNC = "205";
  static final String STATUS_RESYNC_OK = "206";

  static final String STATUS_LOG = "300";

  static final String STATUS_SERVER_ERROR = "500";
  static final String STATUS_VERSION_MISMATCH_ERROR = "501";
  static final String STATUS_INCORRECT_ID_ERROR = "502";

  static final String MATCHMAKER_ID = "0";
  static final String GAME_MANAGER_ID = "1";
  static final String CLIENT_HANDLER_ID = "2";
  static final String LOGGER_ID = "3";


  static final String GAME_CREATE = "0";
  static final String GAME_STATE = "1";
  static final String GAME_INPUT = "2";

  static final String MATCHMAKER_ENQUEUE = "0";
  static final String MATCHMAKER_DEQUEUE = "1";
  static final String MATCHMAKER_FOUND = "2";
  static final String MATCHMAKER_ACCEPT = "3";
  static final String MATCHMAKER_DECLINE = "4";
  static final String MATCHMAKER_LOADING = "5";
  static final String MATCHMAKER_LAUNCH = "6";
  static final String MATCHMAKER_SYNC = "7";

  static MPWPMessage getMessage(String status, String to, String from, int msgnum, String type, [content=null])
  {
    List messageParts = [VERSION, status, to, from, msgnum.toString(), type];

    if(content != null)
    {
      if(content is List)
      {
        messageParts.addAll(content);
      }
      else if(content is String)
      {
        messageParts.add(content);
      }
    }

    return new MPWPMessage(messageParts);
  }

  static MPWPMessage getStatusMessage(String status, String to, String from)
  {
    List messageParts = [VERSION, status, to, from];
    return new MPWPMessage(messageParts);
  }
}