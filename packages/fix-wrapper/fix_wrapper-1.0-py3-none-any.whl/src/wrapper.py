"""This file defined wrapper class and related functions"""
import csv
import os
import sys
path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(path)
from reader import *
from order_pool import *
from const import *


class Wrapper():
    """Wrapper class read each line form log file ,
        create Message ,
        update order pool ,
        output all results to csv files
        |   @file           = log file full path
        |   @reader         = Reader()
        |   @mess           = Message()
        |   @order_pool     = OrderPool()
        |   @out_execu      = csv file -- store all  executed transactions
        |   @out_order      = csv file -- store all  customer order
        |   @out_account    = csv file -- store all  account position
    """

    def __init__(self, file_path, out_dir):
        self.__file = file_path
        self.__reader = Reader(self.__file)
        self.__mess = {}
        self.__order_pool = OrderPool()
        self.__out_execu = os.path.abspath(os.path.join(out_dir, EXECUFILE))
        self.__out_order = os.path.abspath(os.path.join(out_dir, ORDERFILE))
        self.__out_account = os.path.abspath(os.path.join(
            out_dir, ACCOUNTFILE))

    def get_order_pool(self):
        return self.__order_pool

    def start(self):
        """continuing read and process message,
            update orders till end of log,
            output results to csv files
        """

        lines = self.__reader.read_log()
        self.csv_write(self.__out_execu, HEADEREXECU, "w")
        self.csv_write(self.__out_order, HEADERORDER, "w")
        for line in lines:
            if line[0] == '#':
                continue
            self.__mess = self.__reader.read_line(line)
            order = self.update_order()
            if order is not None:
                self.update_order_pool(order)
                order.set_pos()
                print((self.__order_pool.serach_order(
                    order.get_order_id())).print_order())
        self.order_pool_out()

    def update_order(self):
        """create order based on trade message"""
        if self.__mess.__class__.__name__ == 'TradeMessage':
            # add order into customer order and orderpool
            order = Order(self.__mess.get_order_id(), self.__mess.get_code(),
                          self.__mess.get_quantity(), self.__mess.get_side(),
                          self.__mess.get_account(), self.__mess.get_sum_qty(),
                          self.__mess.get_aver_price(),
                          self.__mess.get_left_qty(),
                          self.__mess.get_price())
            return order
        return None

    def update_order_pool(self, order):
        """add or update orders in order pool based on trade message"""
        if self.__mess.get_exec_type() == '0':
            self.__order_pool.add_order(order)
            print("receive order mesaage :{}".format(
                self.__mess.order_message_format()))
            self.csv_write(self.__out_order,
                           self.__mess.order_message_format(), "a+")

        elif self.__mess.get_exec_type() == 'F':
            self.__order_pool.update_order(order)
            print("execu order message :{}".format(
                self.__mess.exec_message_format()))
            self.csv_write(self.__out_execu,
                           self.__mess.exec_message_format(), "a+")

    def order_pool_out(self):
        """wrap order information and write to csv files"""
        rows = self.__order_pool.acct_pos()
        self.csv_write(self.__out_account, [], "w")
        for row in rows:
            self.csv_write(self.__out_account, row, "a+")
            # print(row)

    def csv_write(self, filepath, row, writer):
        """write results to csv files"""
        with open(filepath, writer) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
