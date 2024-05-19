After testing my codes with limited student access on iFinD, I made minor adjustments and migrated them on JoinQunt Platform to run free backtest freely. Here are some examples of changes:

Change the codes like,
...
from iFinDPy import *
import concept_helper as cp
...

into

from jqdata import *
from jqfactor import Factor, calc_factors
import datetime
...

The backtest result could be seen as follow:

![backtest](.\backtesting_Div'n'LowVolat.png)