
# coding: utf-8

# In[87]:

import bt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import io
#matplotlib.style.use('ggplot')
get_ipython().magic(u'matplotlib inline')


# In[76]:

bloom = pd.read_csv("~/quantsph/BLOOM.csv")
plc = pd.read_csv("~/quantsph/PLC.csv")
bloom_d = bloom.set_index('Date')
plc_d = plc.set_index('Date')
bloom_d.head()
plc_d.head()


# In[93]:

#df = pd.concat({'BLOOM' : bloom_d['Close'], 'PLC' : plc_d['Close']})
df = pd.DataFrame(dict(BLOOM = bloom_d['Close'], PLC = plc_d['Close'])).dropna()
df.index = pd.to_datetime(df.index)
df.tail()


# In[94]:

df.plot()


# In[95]:

s = bt.Strategy('s1', [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])


# In[96]:

# create a backtest and run it
test = bt.Backtest(s, df)
res = bt.run(test)


# In[97]:

# first let's see an equity curve
res.plot()


# In[ ]:



