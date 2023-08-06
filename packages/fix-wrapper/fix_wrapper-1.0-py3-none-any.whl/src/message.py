""" This file defined The classes of different message types, related functions
    message variables are read from one line of the log fine
    fields' name and values based on FIX stantard format
"""
import re


class Header():
    """header is the FIX header
        +   -HEADER
        |   8 @begin_string      = FIX.4.4
        |   9 @body_length       = 178
        |   35 @msg_type         = Logon (A) | Logout (5) |
                                   Heart beat (0) | Execution Report (8)
        |   34 @msg_seq_num      = 1
        |   49 @sender_comp_id   = testusr4109
        |   52 @sending_time     = 20101124-20:27:25.000
        |   56 @target_comp_id   = WIKIPEDIA
    """

    def __init__(self, begin_string, body_length, msg_type,
                 msg_seq_num, target_comp_id, sending_time):
        self.__begin_string = begin_string
        self.__body_length = body_length
        self.__msg_type = msg_type
        self.__msg_seq_num = msg_seq_num
        self.__target_comp_id = target_comp_id
        self.__sending_time = sending_time

    def set_begin_string(self, begin_string):
        """set beginning of new message and protocol version"""
        self.__begin_string = begin_string

    def set_body_length(self, body_length):
        """set Message length, in bytes of the new message"""
        self.__body_length = body_length

    def set_msg_type(self, msg_type):
        """set Message type"""
        self.__msg_type = msg_type

    def set_msg_seq_num(self, msg_seq_num):
        """set Message seq number"""
        self.__msg_seq_num = msg_seq_num

    def set_target_comp_id(self, target_comp_id):
        """set assigned value used to identify receiving firm."""
        self.__target_comp_id = target_comp_id

    def set_sending_time(self, sending_time):
        """set send time of the message"""
        self.__sending_time = sending_time

    def get_begin_string(self):
        """get beginning of new message and protocol version"""
        return self.__begin_string

    def get_body_length(self):
        """get Message length, in bytes of the new message"""
        return self.__body_length

    def get_msg_type(self):
        """get Message type"""
        return self.__msg_type

    def get_msg_seq_num(self):
        """get Message seq number"""
        return self.__msg_seq_num

    def get_target_comp_id(self):
        """get assigned value used to identify receiving firm."""
        return self.__target_comp_id

    def get_sending_time(self):
        """get send time of the message"""
        return self.__sending_time


class Trailer():
    """Trailer is the FIX trailer
        +   -TRAILER
        |   10  @check_sum         = 133
    """

    def __init__(self, check_sum):
        self.__check_sum = check_sum

    def set_check_sum(self, check_sum):
        """set three byte, simple checksum"""
        self.__check_sum = check_sum

    def get_check_sum(self):
        """get three byte, simple checksum"""
        return self.__check_sum


class Message():
    """Message class defined heart beat & log out message
        @header
        @trailer
     """

    def __init__(self, header, trailer):
        self.__header = header
        self.__trailer = trailer

    def get_header(self):
        """get header of the message"""
        return self.__header

    def get_trailer(self):
        """get trailer of the message"""
        return self.__trailer


class LogOnMessage(Message):
    """ LogOnMessage inherit Message
        @header
        +   BODY
        |  108 @heart_beat_int       = 300
        |  141 @reset_seq_num_flag   = Y
        @trailer
    """

    def __init__(self, header, trailer,
                 heart_beat_int, reset_seq_num_flag=True):
        super().__init__(header, trailer)
        self.__heart_beat_int = heart_beat_int
        self.__reset_seq_num_flag = reset_seq_num_flag

    def set_heart_beat_int(self, heart_beat_int):
        """set heart beat interval (seconds)"""
        self.__heart_beat_int = heart_beat_int

    def set_reset_seq_num_flag(self, reset_seq_num_flag):
        """set flag -- indicates that the both sides of the FIX session
            should reset sequence numbers."""
        self.__reset_seq_num_flag = reset_seq_num_flag

    def get_heart_beat_int(self):
        """get heart beat interval (seconds)"""
        return self.__heart_beat_int

    def get_reset_seq_num_flag(self):
        """get flag -- indicates that the both sides of the FIX session
            should reset sequence numbers."""
        return self.__reset_seq_num_flag


class TradeMessage(Message):
    """ TradeMessage inherit Message
        @header
        +   BODY
        |   1    @account        = TEST1234
        |   31   @price          = 25
        |   32   @quantity       = 3
        |   54   @side           = 1 (Buy) | 2 (Sell)
        |   55   @code           = 0700
        |   60   @time           = 20180109-07:01:07
        |   150  @exec_type      = 0 (New) | F (Trade -- partial fill or fill)
        |   11   @order_id       = 30636510780671786000
        |   6    @aver_price     = 25
        |   151  @left_qty       = 50
        |   14   @sum_qty        = 50
        @trailer
    """

    def __init__(self, header, trailer, account, price, quantity, side, code,
                 time, exec_type, order_id, aver_price, left_qty, sum_qty):
        super().__init__(header, trailer)
        self.__account = account
        self.__price = price
        self.__quantity = quantity
        if side == '1':
            self.__side = "buy"
        elif side == '2':
            self.__side = "sell"
        else:
            self.__side = side
        # save start '0' in csv file
        self.__code = re.sub('^', r"\t", code)
        self.__time = time
        self.__exec_type = exec_type
        self.__order_id = order_id
        self.__aver_price = aver_price
        self.__left_qty = left_qty
        self.__sum_qty = sum_qty

    def get_aver_price(self):
        """get average price of all fills on this order"""
        return self.__aver_price

    def set_aver_price(self, aver_price):
        """set average price of all fills on this order"""
        self.__aver_price = aver_price

    def get_left_qty(self):
        """get remaining stock qty of the order"""
        return self.__left_qty

    def set_left_qty(self, left_qty):
        """set remaining stock qty of the order"""
        self.__left_qty = left_qty

    def get_sum_qty(self):
        """get the sum qty of all execuated fills on this order"""
        return self.__sum_qty

    def set_sum_qty(self, sum_qty):
        """set the sum qty of all execuated fills on this order"""
        self.__sum_qty = sum_qty

    def get_order_id(self):
        """get customer's order id"""
        return self.__order_id

    def set_order_id(self, order_id):
        """set customer's order id"""
        self.__order_id = order_id

    def set_exec_type(self, exec_type):
        """set exec type to identify the current order status"""
        self.__exec_type = exec_type

    def get_exec_type(self):
        """get exec type to identify the current order status"""
        return self.__exec_type

    def set_account(self, account):
        """set the account num which send the order"""
        self.__account = account

    def set_price(self, price):
        """set order last recently shares' price"""
        self.__price = price

    def set_quantity(self, quantity):
        """set order last recently shares' qty"""
        self.__quantity = quantity

    def set_side(self, side):
        """set the order side buy/sell"""
        if side == '1':
            self.__side = "buy"
        elif side == '2':
            self.__side = "sell"
        else:
            self.__side = side

    def set_code(self, code):
        """set the stock code"""
        self.__code = code

    def set_time(self, time):
        """set the transcatio time"""
        self.__time = time

    def get_account(self):
        """get the account num which send the order"""
        return self.__account

    def get_price(self):
        """get order last recently shares' price"""
        return self.__price

    def get_quantity(self):
        """get order last recently shares' qty"""
        return self.__quantity

    def get_side(self):
        """get the order side buy/sell"""
        return self.__side

    def get_code(self):
        """get the stock code"""
        return self.__code

    def get_time(self):
        """get the transcatio time"""
        return self.__time

    def exec_message_format(self):
        """all feilds' value of fill on this order"""
        return [str(self.get_code()), self.get_quantity(),
                self.get_price(), self.get_side(), self.get_account(),
                self.get_order_id(), self.get_time()]

    def order_message_format(self):
        """"all feilds' value of customer order"""""
        return [str(self.get_code()), self.get_account(),
                self.get_left_qty(), self.get_side(),
                self.get_order_id(), self.get_time()]
