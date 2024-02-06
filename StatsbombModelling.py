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
#x_s=borussia_match['x_start'].to_list()
#y_s=borussia_match['y_start'].to_list()
#x_e=borussia_match['x_end'].to_list()
#y_e=borussia_match['y_end'].to_list()
#outcomes=borussia_match['pass_outcome'].to_list()
#outcomes


#%% Visualizations
def make_pass_plot(pass_data):
    pitch=Pitch(pitch_type='statsbomb')
    fig, ax = pitch.draw(figsize=(15,8))
    success=pd.isnull(pass_data['pass_outcome'])
    s_passes=borussia_match[success]
    us_passes=borussia_match[~success]
    s_x_start=s_passes['x_start'].to_list()
    s_x_end=s_passes['x_end'].to_list()
    s_y_start=s_passes['y_start'].to_list()
    s_y_end=s_passes['y_end'].to_list()
    us_x_start=us_passes['x_start'].to_list()
    us_x_end=us_passes['x_end'].to_list()
    us_y_start=us_passes['y_start'].to_list()
    us_y_end=us_passes['y_end'].to_list()

    pitch.scatter(s_x_start,s_y_start,c='green',ax=ax,label='Origin of successful pass')
    pitch.scatter(us_x_start,us_y_start,c='red',ax=ax,label='Origin of unsuccessful pass')
    lc1=pitch.lines(s_x_start, s_y_start, s_x_end, s_y_end, lw=3, comet=True, color='green', ax=ax, label='Successful Passes',transparent=True)
    lc2=pitch.lines(us_x_start, us_y_start, us_x_end, us_y_end, lw=3, comet=True, color='red', ax=ax, label='Unsuccessful Passes',transparent=True)
    ax.legend(facecolor='white', edgecolor='black', fontsize=10, loc='upper left', handlelength=7)
    ax.set_title('Borussia Dortmund: Passes made under Pressure v/s Augsburg, 2015/16', fontsize=18)
    n='Borussia Dortmund Passes made under Pressure vs Augsburg'
    fig.savefig(f'{n}.png')



    return(fig.show)

# %%
make_pass_plot(borussia_match)


# %%
bvb_matches
m_id=3890275
bor_dor_match=sb.events(match_id=3890347)
bor_dor_match.columns

# %%
bor_dor_match_shot_data=bor_dor_match[['team','type','shot_type','shot_technique','location','player','shot_outcome','shot_statsbomb_xg']].reset_index()
bor_dor_match_shot_data['type'].unique()
# %%
shots=bor_dor_match_shot_data[(bor_dor_match_shot_data['team']=='Borussia Dortmund') & (bor_dor_match_shot_data['type']=='Shot') & (bor_dor_match_shot_data['shot_outcome']=='Goal') ]
shots
shots[['x_start', 'y_start']]=pd.DataFrame(shots.location.to_list(), index=shots.index)
# %%

from mplsoccer import VerticalPitch

def make_shot_plot(shot_data):
    pitch = VerticalPitch(pad_bottom=0.5,  half=True,  goal_type='box')
    fig , ax =pitch.draw(figsize=(15,8))
    penalty=shot_data['shot_outcome']=='Penalty'
    open_play_goals=shot_data[~penalty]
    penalty_goals=shot_data[penalty]
    x_s=open_play_goals['x_start'].to_list()
    y_s=open_play_goals['y_start'].to_list()
    s_x_g=open_play_goals['shot_statsbomb_xg']

    sc=pitch.scatter(x_s, y_s,s=((s_x_g*500)+100), marker='football',ax=ax, label='Goals')
    ax.legend(facecolor='white', edgecolor='black', fontsize=20, loc='upper left')
    ax.set_title('(Greater size refers to greater xG)', fontsize=10)
    fig.suptitle('Borussia Dortmund: Goals scored v/s Augsburg, 2015/16', fontsize=18)
    n='Borussia Dortmund Goals vs Augsburg'
    fig.savefig(f'{n}.png')

    return(fig.show)
    

# %%
make_shot_plot(shots)

# %%
