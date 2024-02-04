#%%Imports
import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import numpy as np
import matplotlib.pyplot as plt


#%%Exploratory Data Analysis
#season_id : Season 2015/16 = '27'
#competition_id: Premier League = 2,Ligue 1= 7,Bundesliga= 9,La Liga = 11,Serie A = 12
sb.competitions()


# %%Filtering out matches that I am interested in
bundesliga_matches=sb.matches(competition_id='9',season_id='27')


#%%Checks for proper Series output
bundesliga_matches["home_team"]=="Borussia Dortmund"
bundesliga_matches["away_team"]=="Borussia Dortmund"


#%%Filtering out only BVB matches, but still keeping home and away separate
bvb_away_matches=bundesliga_matches[bundesliga_matches["away_team"]=="Borussia Dortmund"]
bvb_home_matches=bundesliga_matches[bundesliga_matches["home_team"]=="Borussia Dortmund"]
bvb_matches=pd.concat([bvb_home_matches,bvb_away_matches],ignore_index=True)
bvb_matches

#%%
bvb_matches.columns
bvb_matches_list=bvb_matches[['match_id']]
bvb_match_ids=bvb_matches_list['match_id'].to_list()
len(bvb_match_ids)

#%%
m=bvb_match_ids[0]


#%%Checking individual matches
borussia_match=sb.events(match_id=3890347)
borussia_match.columns
#%%
borussia_match=borussia_match[['team','type','pass_type','location','pass_end_location','player','under_pressure','pass_outcome']].reset_index()
borussia_match=borussia_match[(borussia_match['team']=='Borussia Dortmund') & (borussia_match['type']=='Pass') &(borussia_match['under_pressure']==True) ]
#borussia_match=borussia_match[borussia_match['type']=='Pass']
#borussia_match=borussia_match[borussia_match['under_pressure']==True]
borussia_match

#%% Preparing for Visualizations
borussia_match[['x_start', 'y_start']]=pd.DataFrame(borussia_match.location.to_list(), index=borussia_match.index)
borussia_match[['x_end', 'y_end']]=pd.DataFrame(borussia_match.pass_end_location.to_list(), index=borussia_match.index)
x_s=borussia_match['x_start'].to_list()
y_s=borussia_match['y_start'].to_list()
x_e=borussia_match['x_end'].to_list()
y_e=borussia_match['y_end'].to_list()
outcomes=borussia_match['pass_outcome'].to_list()
outcomes


#%% Visualizations
def make_plot():
    pitch=Pitch(pitch_type='statsbomb')
    fig, ax = pitch.draw(figsize=(15,8))

    for i in range(len(x_s)):

        if outcomes[i]== 'Incomplete':
            color='red'
        else:
            color='green'

        pitch.scatter(x_s[i], y_s[i], ax=ax, c=color)
        pitch.lines(x_s[i], y_s[i], x_e[i], y_e[i], ax=ax, comet=True, color=color)

    return(plt.title('Borussia Dortmund: Passes made under Pressure v/s Augsburg, 2015/16'))


# %%
make_plot()
# %%

comps=sb.competitions()
season_needed=comps[comps['season_id']==27]
# %%
season_needed
# %%

