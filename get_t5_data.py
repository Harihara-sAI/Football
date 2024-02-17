#%%Imports

import pandas as pd
from statsbombpy import sb
# %%
a=sb.competition_events(country='Germany',division='1. Bundesliga', season='2015/2016')
# %%
bundesliga_data=a[(a['type']=='Pass') | (a['type']=='Shot')]
# %%
bundesliga_data
# %%
bvb_data=bundesliga_data[(bundesliga_data['team']=='Borussia Dortmund')]
# %%
bvb_data
# %%
bvb_data.columns
# %%
