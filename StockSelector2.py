# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np
import StockFilterWrapper

@StockFilterWrapper.filtrate_stop_trade
def select(stock_list, x_position=-1, kline_type=StockConfig.kline_type_week, min_item=120):
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
        except:
            continue
        if kline.shape[0] < min_item:
            continue
        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
        if not sma5[x_position] > sma10[x_position] > sma20[x_position]:
            continue

        if not close[x_position] > sma10[x_position]:
            continue

        print(stock)
        result.append(stock)

    return result


if __name__ == '__main__':
    result={}
    for x in range(-10, 0):
        print('x = ', x)
        stock_list = select(StockIO.get_stock('sha'), x_position=x, kline_type=StockConfig.kline_type_week)
        print(stock_list)

        for stock in stock_list:
            result[stock] = result.get(stock, 0) + 1

    with open('{}/{}'.format(StockConfig.path_stock, 'wsma10'), 'w', encoding='utf-8') as f:
        for key in result:
            if result[key] >= 7:
                f.write("{},{}\n".format(key.stock_code, key.stock_name))

    print(sorted(result.items(), key=lambda d: d[1], reverse=True))



