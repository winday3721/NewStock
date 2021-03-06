# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np
import StockFilterWrapper
import StockFilter2
import datetime
import time

@StockFilterWrapper.filtrate_stop_trade
def select(stock_list, x_position=-1, w_x_position= -1, kline_type=StockConfig.kline_type_week, min_item=120):
    """
    均线选股法
    :param stock_list:
    :param kline_type:
    :param avg:
    :return:
    """
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
            w_kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_week)
        except:
            continue
        if kline.shape[0] < min_item:
            continue
        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        sma5, sma10, sma20, sma30= StockIndicator.sma(kline, 5, 10, 20, 30)
        cjl = StockIndicator.cjl(kline)
        w_close = w_kline[:, 2].astype(np.float)
        #if w_sma5[w_x_position] > w_sma10[w_x_position]:
        if close[x_position] > sma5[x_position] > sma10[x_position] and close[x_position] > sma30[x_position]:
                if close[x_position] > np.max(close[x_position - 8: x_position]):
                    if cjl[x_position] > np.max(cjl[x_position - 8: x_position]):
                        count = 0
                        add = False
                        while count < 4:
                            if StockFilter2.is_jx(sma5, sma10, x_position - count):

                                add = True
                                break
                            count += 1

                        if add:
                            print(stock)
                            result.append(stock)

    return result


def get_stock_list(x_position):
    stock_list = []

    stock_list1 = select(StockIO.get_stock('sza'), x_position=x_position, kline_type=StockConfig.kline_type_week)
    stock_list2 = select(StockIO.get_stock('sha'), x_position=x_position, kline_type=StockConfig.kline_type_week)
    for x in stock_list1:
        if x not in stock_list:
            stock_list.append(x)
    for x in stock_list2:
        if x not in stock_list:
            stock_list.append(x)

    return stock_list


def delete_invalid_record():
    with open('{}/{}'.format(StockConfig.path_track, '2_sma_track_w.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open('{}/{}'.format(StockConfig.path_track, '2_sma_track_w.txt'), 'w', encoding='utf-8') as f:
        for line in lines:
            if not line.startswith("#") and not '\n' == line:
                data = line.strip('\n').split(',')
                stock_code = data[0]
                kline = StockIO.get_kline(stock_code, StockConfig.kline_type_week)
                sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
                if sma5[-1] < sma10[-1] and sma5[-1] < sma20[-1]:
                    continue
                f.write(line)
            else:
                f.write(line)


if __name__ == '__main__':
    for i in range(-10, 0):
        stock_list_1 = get_stock_list(i)
        stock_list_2 = get_stock_list(i - 1)
        stock_list_3 = get_stock_list(i - 2)
        stock_list_4 = get_stock_list(i - 3)

        stock_list = [x for x in stock_list_1 if x not in (stock_list_2 + stock_list_3 + stock_list_4)]

        print(stock_list)
        print(len(stock_list))


        with open('data/track/2_sma_track_w.txt', mode='a', encoding='utf-8') as f:
            f.write('\n#2017-12-09\n')
            for key in stock_list:
                f.write("{},{}, , , , ,\n".format(key.stock_code, key.stock_name))

    delete_invalid_record()

    # with open('C:/Users/panha/Desktop/xgfx/1002.txt', mode='w', encoding='utf-8') as f:
    #     for key in stock_list:
    #         f.write("{}\n".format(key.stock_code))



