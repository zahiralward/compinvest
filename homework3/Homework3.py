import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math 

# Set the Start Date
dt_startdate = dt.datetime(2010,1,1)
# Set the End Time
dt_enddate = dt.datetime(2010,12,31)
# Set the Symbols
#trial_symbols = ["AXP", "HPQ", "IBM", "HNZ"]
trial_symbols = ["C", "GS", "IBM", "HNZ"]
# Setup Allocations
optimum_sharp_ratio=0.0
optimum_alloc = []
optimum_std = 0.0
optimum_avg = 0.0
optimum_com = 0.0
def assess_portfolio (startdate, enddate, symbols, allocations):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)
    
    # Clear the Cash
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    case_ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, case_ls_keys)
    d_data = dict(zip(case_ls_keys, ldf_data))
    # Portfolio 
    na_price = d_data['close'].values
    na_price_norm = na_price/na_price[0:1]
    len_portfolio_history = len(na_price)  
    daily_portfolio = na_price_norm * allocations
    commulative_daily_portfolio = daily_portfolio.sum(axis=1)
    
    net_return = np.zeros(len_portfolio_history)
    for i in range (1, len_portfolio_history):
        net_return[i] = commulative_daily_portfolio[i] - commulative_daily_portfolio[i-1]
    average_return = np.average(net_return)
    std_return = np.std(net_return)
    sharp_ratio = math.sqrt(252)*average_return/std_return
    comu_return = commulative_daily_portfolio[len_portfolio_history-1]    
    return average_return, std_return,sharp_ratio,comu_return;
allsteps = np.arange(0,1.1,0.1)
trial_alloc=[]
for alloc1 in allsteps:
    for alloc2 in allsteps:
        for alloc3 in allsteps:
            alloc4 = 1 - alloc1 - alloc2 - alloc3
            if alloc4 > 0:
                trial_alloc = [alloc1, alloc2, alloc3, alloc4]
                average_return, std_return,sharp_ratio,comu_return = assess_portfolio (dt_startdate,dt_enddate,trial_symbols,trial_alloc)
                if (sharp_ratio > optimum_sharp_ratio):
                    optimum_sharp_ratio = sharp_ratio
                    optimum_alloc = trial_alloc
                    optimum_std = std_return
                    optimum_avg = average_return
                    optimum_com = comu_return

print "Start Date: ", dt_startdate
print "End Date: ", dt_enddate
print "Symbols" , trial_symbols
print "Optimal Allocation", optimum_alloc
print "Sharpe Ratio :", optimum_sharp_ratio
print "Standard Deviation: ", optimum_std
print "Average Daily Return: ", optimum_avg
print "Commulative Return :", optimum_com
                                    