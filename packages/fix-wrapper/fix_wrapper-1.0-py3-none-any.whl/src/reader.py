"""this file defined class Reader and related function"""
from message import *


class Reader():
    """ Reader read the input log file
        process each line and create Message
    """

    def __init__(self, file_path):
        self.__file_path = file_path

    def read_log(self):
        """read log contents line by line"""
        log_file = open(self.__file_path, "r")
        lines = log_file.readlines()
        log_file.close()
        return lines

    def create_message(self, mess):
        """grap values instruct by FIX standard
            created different Message type"""
        begin_string = mess['8']
        body_length = int(mess['9'])
        msg_type = mess['35']
        msg_seq_num = mess['34']
        target_comp_id = mess['49']
        sending_time = mess['52']
        head = Header(begin_string, body_length, msg_type,
                      msg_seq_num, target_comp_id, sending_time)
        check_sum = mess['10']
        trail = Trailer(check_sum)
        if msg_type in ('0', '5'):
            # heartbeat / logout
            return Message(head, trail)
        if msg_type == 'A':
            # logon
            heart_beat_int = mess['108']
            return LogOnMessage(head, trail, heart_beat_int)
        # trade
        account = mess['1']
        price = mess['31']
        qty = int(mess['32'])
        side = mess['54']
        code = str(mess['55'])
        time = mess['60']
        exec_type = mess['150']
        order_id = mess['11']
        aver_price = mess['6']
        left_qty = int(mess['151'])
        sum_qty = int(mess['14'])
        return TradeMessage(head, trail, account, price, qty, side, code,
                            time, exec_type, order_id, aver_price,
                            left_qty, sum_qty)

    def read_line(self, line):
        """process each line to -> {feild : value} hashmap"""
        messages = (line.split("|\n")[0]).split("|")
        dict_mess = {}
        for field in messages:
            (key, value) = field.split("=")
            dict_mess[key] = value
        mess = self.create_message(dict_mess)
        return mess
