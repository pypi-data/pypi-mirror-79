"""This file defined OrderPool clas and related functions"""
import os
import sys
path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(path)
from order import *


class OrderPool():
    """ The OrderPool stores all orders
        keep track order position after every transaction
        @__orders : hashmap(dic) {order_id: Order} to store Order instances
    """

    def __init__(self):
        self.__orders = {}

    def serach_order(self, order_id):
        """search whether the order is in order pool"""
        if order_id in self.__orders:
            return self.__orders[order_id]
        return False

    def add_order(self, order):
        """add new order to order pool"""
        order_locate = self.serach_order(order.get_order_id())
        if not order_locate:
            order.set_pos()
            self.__orders[order.get_order_id()] = order
        else:
            print("Error orderId, not unique")

    def update_order(self, order):
        """update order in order pool based on the trascations of order"""
        order_locate = self.serach_order(order.get_order_id())
        if order_locate:
            if order_locate.get_left_qty() < order.get_qty():
                print("Error Qty, larger than left quantity")
                return False
            order_locate.set_aver_price(order.get_aver_price())
            order_locate.set_price(order.get_price())
            order_locate.set_cum_qty(
                    order.get_qty() + order_locate.get_cum_qty())
            order_locate.set_left_qty(order.get_left_qty())
            order_locate.set_qty(order.get_qty())
            order_locate.set_pos()
            self.__orders[order.get_order_id()] = order_locate
        return True

    def acct_pos(self):
        """get accounts positions information stored in orders hashmap"""
        order_rows = []
        for order_id in self.__orders:
            if len(order_rows) == 0:
                order_rows.append(self.__orders[order_id].order_head())
            order_rows.append(self.__orders[order_id].order_value())
        return order_rows
