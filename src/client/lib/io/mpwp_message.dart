import 'package:client/io/mpwp_protocol.dart';

class MPWPMessage
{
  List message;

  MPWPMessage(List message)
  {
    this.message = message;
  }

  bool statusMessage()
  {
    return this.message.length == 4;
  }

  String get version => message[MPWPProtocol.MSG_VERSION];
  String get status => message[MPWPProtocol.MSG_STATUS];
  String get to => message[MPWPProtocol.MSG_TO];
  String get from => message[MPWPProtocol.MSG_FROM];
  String get msgnum => message[MPWPProtocol.MSG_MSGNUM];
  String get type => message[MPWPProtocol.MSG_TYPE];
  List get content => message.sublist(MPWPProtocol.MSG_CONTENT);
}