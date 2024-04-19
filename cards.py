# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 13:53:58 2022

@author: Couper
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import random
import numpy as np
import plotly.express as px
from distfit import distfit
import statistics
from scipy.stats import nbinom


def make_deck():
    cards = pd.DataFrame(columns = ["value", "suit"])
    values = ["Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace"]
    suits = ["Clubs","Diamonds","Hearts","Spades"]
    for i in values:
        for z in suits:
            df_len=len(cards)
            cards.loc[df_len]=(i,z)
    return cards
        


def shuffle(deck):
    choices = list(range(0,52))
    random.shuffle(choices)
    shuffled_deck=pd.DataFrame(columns = ["value", "suit"])
    for i in choices:
        df_len=len(shuffled_deck)
        shuffled_deck.loc[df_len]=deck.loc[i]
    return shuffled_deck

def idiots_delight(deck):
    in_game_deck=deck
    active_card=0
    while len(in_game_deck)>=4 and active_card<=len(in_game_deck)-4:
        if in_game_deck.iloc[active_card]["value"]==in_game_deck.iloc[active_card+3]["value"]:
            in_game_deck=in_game_deck.drop(in_game_deck.index[[active_card,active_card+1,active_card+2,active_card+3]]).reset_index(drop=True)
            active_card=0
        elif in_game_deck.iloc[active_card]["suit"]==in_game_deck.iloc[active_card+3]["suit"]:
            in_game_deck=in_game_deck.drop(in_game_deck.index[[active_card+1,active_card+2]]).reset_index(drop=True)
            active_card=0
        else:
            active_card+=1
    return len(in_game_deck),in_game_deck,active_card


new_deck = make_deck()

shuffled = shuffle(new_deck)

score=idiots_delight(shuffled)

results=pd.DataFrame(columns=["score"])
for i in list(range(10000)):
    shuffled = shuffle(new_deck)
    score=idiots_delight(shuffled)
    results.loc[i]=score[0]

dist = distfit()

x=results.score.to_numpy()
X=x/2
dist.fit_transform(X)
dist.plot()

check=sorted(X)

results_mean = statistics.mean(results.score)
results_var = statistics.variance(results.score, xbar=results_mean)
likelihoods={}
p=results_mean / results_var
r=p*results_mean / (1-p)

param = nbinom.fit(results.score)
likelihoods['nbinom']=results.score.map(lambda val: nbinom.pmf(val,r,p)).prod()

d = sorted(results.score.unique())
# np.histogram(results,d)
# fig = px.histogram(results, x="score")
# fig.show()


@app.callback(
    dash.dependencies.Output('market-graph', 'figure'),
    dash.dependencies.Input('update-button-state', 'n_clicks'),
    )
def update_graph(runner_selected, update_click_num):
    global old_update_click_num
    if update_click_num > old_update_click_num: #User clicked Update Data button
        update_data() #Update the data
        old_update_click_num = update_click_num #Set the click counter
    fig = make_market_graph(cfg, cd, co, trds, dd, runner_selected)
    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
f=open('C:/Users/Couper/Desktop/Test.txt','w')
with open('Test.txt','w') as f:
    f.write('readme')

