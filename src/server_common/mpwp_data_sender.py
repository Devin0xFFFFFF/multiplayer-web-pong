from . import mpwp_protocol


class MPWPDataSender():
    ID = None
    MSGNUM = 0

    def assign_id(self):
        self.ID = mpwp_protocol.get_uuid()

    def get_packet(self, TO, DATA_TYPE, DATA_CONTENT):
        packet = mpwp_protocol.get_mpwp_data_packet(TO, self.ID, [self.MSGNUM, DATA_TYPE, DATA_CONTENT])
        self.MSGNUM += 1
        return packet
