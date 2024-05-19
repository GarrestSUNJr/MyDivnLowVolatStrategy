from stock_selector import DataFetcher, DataCleaner, DataHandler, StockSelector
import numpy as np
import pandas as pd
import sys
import os

dataFetcher = DataFetcher()
dataHandler = DataHandler()
data_file_path = os.path.join(os.path.dirname(os.getcwd()), 'data')#specify path
base_pool = pd.read_csv(data_file_path + '//codes_map.csv')#
calender = dataFetcher.get_calender_data('2014-01-01', '2023-08-01', endlevel=[(1,2), (1), (1,2), (1,2)])

mv_data = pd.read_csv(data_file_path + '//daily_avg_mv_data.csv')
mv_data = mv_data.set_index('wind_code')
turnoverV_data = pd.read_csv(data_file_path + '//daily_avg_turnoverV_data.csv')
turnoverV_data = turnoverV_data.set_index('wind_code')
mv_rank = DataHandler().top_rank(mv_data, 0.8)
turnoverV_rank = DataHandler().top_rank(turnoverV_data, 0.8)
dividend_rank = pd.read_csv(data_file_path + '//dividend_index_data.csv')
dividend_rank = dividend_rank.set_index('wind_code')
dividend_rank = dividend_rank.apply(lambda col: col[col==1].index).apply(pd.Series).T
stock_pool = []
for i in range(115):
    common_stocks = np.intersect1d(mv_rank.iloc[:,i].dropna(), np.intersect1d(turnoverV_rank.iloc[:,i].dropna(), dividend_rank.iloc[:,i].dropna()))
    stock_pool.append(common_stocks)
final_result = pd.DataFrame(stock_pool).T

final_result.to_csv("Base_Pool_1.csv")

data_file_path = os.path.join(os.path.dirname(os.getcwd()), 'data')#specify path
payratio_data = pd.read_csv(data_file_path + '//payratio_data.csv')
dividend_delta_data = pd.read_csv(data_file_path + '//dividend_delta_data.csv')

def filter_1(base_pool: pd.DataFrame, payratio_data: pd.DataFrame, dividend_delta_data: pd.DataFrame, ratio: float = 0.05):
    filter_stocks = []
    payratio_data = payratio_data.set_index('wind_code')
    for date in base_pool.columns:
        base_stocks = base_pool[date].dropna()
        positive_dividend_growth = dividend_delta_data[(dividend_delta_data['year'] == int(date[:4])) & (dividend_delta_data['dividendps'] > 0)]['wind_code'].unique()
        filter_1 = np.intersect1d(base_stocks, positive_dividend_growth)
        sorted_stocks = payratio_data[date].dropna().sort_values(ascending=False)
        top_5_percent_count = int(len(sorted_stocks) * ratio)
        payratio_selected_stocks = sorted_stocks.iloc[top_5_percent_count:].index
        filter_2 = np.intersect1d(base_stocks, payratio_selected_stocks)
        final_filter =np.intersect1d(filter_1, filter_2)
        filter_stocks.append(pd.Series(final_filter, name=date))
    df = pd.concat(filter_stocks, axis=1)
    return df

conn = DataFetcher().conn
query = "SELECT TradingDay, DividendRatioLYR, DividendRatio FROM LC_DIndicesForValuation WHERE Innercode = 3"
df = pd.read_sql(query, conn)

'''
df[df['tradingday'] >= '2014-01-30']
show data for pre-viewing
'''