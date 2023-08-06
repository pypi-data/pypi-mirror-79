""" This file defined The class order and related functions"""
import re


class Order():
    """ each order request by client has a unique @order_id
    each Trade Message is one "0"(add) /
                              "F" (Trade - partial fill or fill) for one order
    get/set all related values
    @__position defined wherther the order is open/closed
    """

    def __init__(self, order_id, code, qty, side, account_num,
                 cum_qty, aver_price, left_qty, price):
        self.__order_id = order_id
        self.__account_num = account_num
        self.__code = code
        self.__last_qty = qty
        self.__left_qty = left_qty
        self.__cum_qty = cum_qty
        self.__aver_price = aver_price
        self.__last_price = price
        self.__side = side
        self.__position = ''

    def set_pos(self):
        """change order position (open/close) based on the stock left qty"""
        if self.__left_qty == 0:
            self.__position = 'closed'
        else:
            self.__position = 'open'

    def get_pos(self):
        """get order position (open/close) """
        return self.__position

    def get_price(self):
        """get order last recently shares' price"""
        return self.__last_price

    def set_price(self, price):
        """set order last recently shares' price"""
        self.__last_price = price

    def get_account_num(self):
        """get the account num which send the order"""
        return self.__account_num

    def set_account_num(self, account_num):
        """set the account num which send the order"""
        self.__account_num = account_num

    def set_aver_price(self, aver_price):
        """set the stock average price of all fills on this order"""
        self.__aver_price = aver_price

    def get_aver_price(self):
        """get the stock average price of all fills on this order"""
        return self.__aver_price

    def set_qty(self, qyt):
        """set order last recently shares' qty"""
        self.__last_qty = qyt

    def get_qty(self):
        """get order last recently shares' qty"""
        return self.__last_qty

    def set_cum_qty(self, cum_qyt):
        """set the sum qty of all execuated fills on this order"""
        self.__cum_qty = cum_qyt

    def get_cum_qty(self):
        """get the sum qty of all execuated fills on this order"""
        return self.__cum_qty

    def get_code(self):
        """get the stock code"""
        return str(self.__code)

    def set_code(self, code):
        """set the stock code"""
        self.__code = code

    def get_side(self):
        """get the order side buy/sell"""
        return self.__side

    def set_side(self, side):
        """set the order side buy/sell (1/2)"""
        if side == '1':
            self.__side = "buy"
        elif side == '2':
            self.__side = "sell"
        else:
            self.__side = side

    def get_order_id(self):
        """set customer's order id"""
        return self.__order_id

    def set_order_id(self, order_id):
        """get customer's order id"""
        self.__order_id = order_id

    def get_left_qty(self):
        """get remaining stock qty of the order"""
        return self.__left_qty

    def set_left_qty(self, left_qty):
        """set remaining stock qty of the order"""
        self.__left_qty = left_qty

    def order_head(self):
        """class variables' names list(csv file header) """
        name_space = self.__dict__.keys()
        names = []
        for name in name_space:
            name = re.sub('^__', '', name.split('__')[1])
            names.append(name)
        return names

    def order_value(self):
        """get all values of an order (write into csv file row)"""
        return [self.get_order_id(), self.get_account_num(), self.get_code(),
                self.get_qty(), self.get_left_qty(), self.get_cum_qty(),
                self.get_aver_price(), self.get_price(),
                self.get_side(), self.get_pos()]

    def print_order(self):
        """field name and correspoding value
            keep track order position after every fill"""
        headers = self.order_head()
        out_values = self.order_value()
        out_str = ""
        for i in range(len(headers)):
            out_str += (headers[i] + " : " + str(out_values[i]) + " | ")
        return out_str
