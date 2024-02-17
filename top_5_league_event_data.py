#%%Imports
import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import numpy as np
import matplotlib.pyplot as plt


#%%Exploratory Data Analysis
#season_id : Season 2015/16 = '27'
#competition_id: Premier League = 2,Ligue 1= 7,Bundesliga= 9,La Liga = 11,Serie A = 12
data=sb.competitions()
data
# %%
comps=data[(data['season_id']==27)]
# %%
comps
# %%
bl=sb.competition_events(country='Germany',division='1. Bundesliga', season='2015/2016')
bl
# %%
ll=sb.competition_events(country='Spain',division='La Liga', season='2015/2016')
ll
# %%
l1=sb.competition_events(country='France',division='Ligue 1', season='2015/2016')
l1
# %%
epl=sb.competition_events(country='England',division='Premier League', season='2015/2016')
epl
# %%
sa=sb.competition_events(country='Italy',division='Serie A', season='2015/2016')
sa
# %%
t_5=[bl,ll,l1,epl,sa]
t_5_leagues=pd.concat(t_5)
# %%
event_data=t_5_leagues[(t_5_leagues['type']=='Pass') | (t_5_leagues['type']=='Shot')]
# %%
type(event_data)
# %%
event_data.to_csv('top_5_leagues_2015_2016.csv', index=False)
# %%
