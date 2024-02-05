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


#%%Making function to filter out leagues that I am interested in
def get_league_data(i):
    league_matches=sb.matches(competition_id=str(i),season_id='27')
    return league_matches

#premier_leagu_matches=get_league_data(2)
#ligue_1=get_league_data(7)
bundesliga=get_league_data(9)
#la_liga=get_league_data(11)
#serie_a=get_league_data(12)



#%%Checks for proper Series output
#bundesliga_matches["home_team"]=="Borussia Dortmund"
#bundesliga_matches["away_team"]=="Borussia Dortmund"

#%%Making function to filter out matches that I am interested in
def get_team_matches(league,team):
    away_matches=league[league["away_team"]==str(team)]
    home_matches=league[league["home_team"]==str(team)]
    matches=pd.concat([home_matches,away_matches],ignore_index=True)
    return(matches)



#%%Filtering out only BVB matches, but still keeping home and away separate
#bvb_away_matches=bundesliga_matches[bundesliga_matches["away_team"]=="Borussia Dortmund"]
#bvb_home_matches=bundesliga_matches[bundesliga_matches["home_team"]=="Borussia Dortmund"]
#bvb_matches=pd.concat([bvb_home_matches,bvb_away_matches],ignore_index=True)

bvb_matches=get_team_matches(bundesliga, "Borussia Dortmund")
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
            n=20
            t=True
        else:
            color='green'
            n=100
            t=False

        pitch.scatter(x_s[i], y_s[i], ax=ax, c=color)
        pitch.lines(x_s[i], y_s[i], x_e[i], y_e[i], ax=ax, comet=True, color=color, lw=1.5, n_segments=n, transparent=t)

    return(plt.title('Borussia Dortmund: Passes made under Pressure v/s Augsburg, 2015/16'))


# %%
make_plot()


# %%
