# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 16:06:02 2022

@author: steven.luera
"""


import webbrowser
from threading import Timer
import plotly.express as px
#import plotly
import dash
from dash import dcc
from dash import html #, Output, Input
import pandas as pd 
import datetime
from datetime import date




port =8011
#test = ('H:/Norcross/CC Restricted/WFA/App_data/Data/test_data.csv')
test = ('C:/Users/steve/Desktop/My_code/Data/Data/test_data.csv')

app = dash.Dash(__name__)
app.title = 'NAVEX IDP'
#server = app.server


                
now = (datetime.datetime.now())

minDate = now - datetime.timedelta(days=5)
minday = int(minDate.strftime('%d'))
minmon = int(minDate.strftime('%m'))
minyr = int(minDate.strftime('%Y'))

print (minday, " ", minmon, " ", minyr, " ")
day = int(now.strftime('%d'))
month = int(now.strftime('%m'))
year = int(now.strftime('%Y'))

maxDay = now + datetime.timedelta(days=30)
Nday = int(maxDay.strftime('%d'))
Nmon = int(maxDay.strftime('%m'))

#nEnteredAcd

today = now.strftime('%Y-%m-%d')
print (today)


NCD1a = pd.read_csv('C:/Users/steve/Desktop/My_code/Data/Data/NC1_DOM.csv')
NCD1a['Start']= pd.to_datetime(NCD1a['START_TIME'], format='%m/%d/%Y', exact= False)#' %H:%M:%S')
NCD1a['Period'] = NCD1a['HOUR'].astype(str) + ':' + NCD1a['MINUTE'].astype(str)
NCD1a['Date'] = pd.to_datetime(NCD1a['Period'], format='%H:%M').dt.time



NCG1a = pd.read_csv('C:/Users/steve/Desktop/My_code/Data/Data/NC1_GLB.csv')
NCG1a['Start']= pd.to_datetime(NCG1a['START_TIME'], format='%m/%d/%Y', exact = False)#' %H:%M:%S')
NCG1a['Period'] = NCG1a['HOUR'].astype(str) + ':' + NCG1a['MINUTE'].astype(str)
NCG1a['Date'] = pd.to_datetime(NCG1a['Period'], format='%H:%M').dt.time
NCG1a.to_csv(test)

NC2a = pd.read_csv('C:/Users/steve/Desktop/My_code/Data/Data/NC2.csv')
NC2a['Start']= pd.to_datetime(NC2a['START_TIME'], format='%m/%d/%Y', exact = False)#' %H:%M:%S')
NC2a['Period'] = NC2a['HOUR'].astype(str) + ':' + NC2a['MINUTE'].astype(str)
NC2a['Date'] = pd.to_datetime(NC2a['Period'], format='%H:%M').dt.time



'''
year = int(now.strftime('%Y'))
month = int(now.strftime('%m'))
months= month +2

'''

NC2a['Dom'] = NCD1a.loc[:,'Net']
NC2a['Glb'] = NCG1a.loc[:,'Net']
NC2a['NC2']  = NC2a.loc[:,'Net']
NC2a.to_csv(test)


NC2a['Dom_dif'] = NC2a['NC2'] + NC2a['Dom']
NC2a['Glb_dif'] = NC2a['Dom']  + NC2a['Glb']
              


# ---- figs here ------
NCD1c = NCD1a.loc[NCD1a['Start']== today]
NCG1c = NCG1a.loc[NCG1a['Start']== today]
NC2c  = NC2a.loc[NC2a['Start']== today]
#print(NCD1c.dtypes)
#print(NCD1)
#print(NCD1.iloc[2:9,:15])

fig = px.scatter(NCD1c, x='Period', y = 'Sch', color ='Sch' )
fig2 = px.scatter(NCG1c, x='Period', y = 'Sch', color ='Sch' )
fig3 = px.scatter(NC2c, x='Period', y = 'Sch', color ='Sch' )
fig4 = px.scatter(NC2c, x='Period', y = 'Sch', color ='Sch' )


#----------------------





app.layout = html.Div([
    
    html.Div([
       dcc.DatePickerSingle(
           id = 'Cal',
           min_date_allowed=date(2022,11,1),
           max_date_allowed=date(2022,11,30),
           initial_visible_month=date(2022, 11, 1),
           date=datetime.date(2022,11,1),
           ) 
        ]
        ),

    html.Div([
        dcc.Graph(
            id='NC1 Domestic',
            figure=fig) 
        ],
        style={'width':'50%','display':'inline-block'}
        ),
        
    
    html.Div([
        dcc.Graph(
            id='NC1 Global',
            figure = fig2)
        ],
        style={'width':'50%','display':'inline-block'}
        ),

    html.Div([
        dcc.Graph(
            id='NC2',
            figure = fig3)
        ],
        style={'width':'50%','display':'inline-block'}
        ),

    html.Div([
        dcc.Graph(
            id='All_Net',
            figure = fig4)
        ],
        style={'width':'50%','display':'inline-block'}
        )
    
])


@app.callback([dash.Output('NC1 Domestic','figure'),
               dash.Output('NC1 Global','figure'),
               dash.Output('NC2','figure'),
               dash.Output('All_Net','figure'),
               ],
              [dash.Input('Cal', 'date')])


def update_output(date):
    NCD1d = NCD1a.loc[NCD1a['Start']== date]
#    NCD1d = NCD1c.loc[NCD1c['Start']== date]    

    #print(NCD1d['Start'])
    
    fig ={
        'data':[
            {'x':NCD1d['Period'],'y':NCD1d['Sch'],'type':'scatter','name':'Scheduled'},
            {'x':NCD1d['Period'],'y':NCD1d['Req'],'type':'scatter','name':'Required'},
            {'x':NCD1d['Period'],'y':NCD1d['Net'],'type':'scatter','name':'Net'}        
            ],
        'layout':{
            'title':'NC1 Domestic Staff Forecast over Actual',
            'height':500
            }
        }
    
    
    NCG1d = NCG1a.loc[NCG1a['Start']== date]
    
    fig2 ={
        'data':[
            {'x':NCG1d['Period'],'y':NCG1d['Sch'],'type':'scatter','name':'Scheduled'},
            {'x':NCG1d['Period'],'y':NCG1d['Req'],'type':'scatter','name':'Required'},
            {'x':NCG1d['Period'],'y':NCG1d['Net'],'type':'scatter','name':'Net'}       
            ],
        'layout':{
            'title':'NC1 Global Staff Forecast over Actual',
            'height':500
            }
        }    
        
    NC2d = NC2a.loc[NC2a['Start']== date]
  
    fig3 ={
        'data':[
            {'x':NC2d['Period'],'y':NC2d['Sch'],'type':'scatter','name':'Scheduled'},
            {'x':NC2d['Period'],'y':NC2d['Req'],'type':'scatter','name':'Required'},
            {'x':NC2d['Period'],'y':NC2d['Net'],'type':'scatter','name':'Net'}            
            ],
        'layout':{
            'title':'NC2 Staff Forecast over Actual',
            'height':500
            }
        }    
    
    fig4 ={
        'data':[
            {'x':NC2d['Period'],'y':NC2d['Dom_dif'],'type':'scatter','name':'NC2 Cover NC1 Dom'},
            {'x':NC2d['Period'],'y':NC2d['Glb_dif'],'type':'scatter','name':'NC1 Dom Cover NC1 GLB '},
            {'x':NC2d['Period'],'y':NC2d['Net'],'type':'scatter','name':'NC2 Net'}            
            ],
        'layout':{
            'title':'All NET',
            'height':500
            }
        } 
        

    
    return fig, fig2, fig3, fig4








def open_browser():
    webbrowser.open_new('http://localhost:{}'.format(port))



if __name__=='__main__':
    Timer(1, open_browser).start();
    app.run_server( debug = False, port = port)
   



'''
    html.Div([
       dcc.DatePickerSingle(
           id = 'Cal',
           min_date_allowed=date(minyr,minmon,minday),
           max_date_allowed=date(minyr,Nmon,Nday),
           initial_visible_month=date(year, month, day),
           date=datetime.date(year,month,day),
           ) 
        ]
        ),


'''
