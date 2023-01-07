# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 21:47:06 2022

@author: steven.luera
"""
import dash
#import dash_core_components as dcc
#import dash_html_components as html
from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px
from datetime import date

today = date.today()    
year = today.year
month = today.month
day  = today.day

#main = pd.read_csv('H://Norcross//CC Restricted//WFA//App_data//Data//Attendance//OLA_metrics/total_KPI.csv')
main = pd.read_csv('C:/Users/steve/Desktop/My_code/Data/Data/Attendance/OLA_metrics/total_KPI_dashboard.csv')
df1m = pd.DataFrame(main)

KPI = df1m['StatusKey'].unique()
agent = df1m['UserId'].unique()
code = df1m['Code'].unique()
df1 = df1m.loc[(df1m['UserId']=='AVANYUSH')]
print(df1)

fig = px.scatter(df1, x='UserId', y='Min', orientation='h',title='OLA Metrics',color = 'StatusKey',template='ggplot2',color_continuous_scale='Bluered_r', range_color=[40,100])
fig2 = px.scatter(df1, x='UserId', y='Min', orientation='h',title='OLA Metrics',color = 'StatusKey',template='ggplot2',color_continuous_scale='Bluered_r', range_color=[40,100])




app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.Div(
        html.H1('Shrinkage Tracker'),
        style={'text-align': 'center'}
    ),
    
    html.Div([
        dcc.DatePickerRange(
            id='picker',
            min_date_allowed=date(2022, 10,1),
            start_date = date(2022,10,1),
            end_date = date(2022,12,20), 
            calendar_orientation='vertical',
            ),
    ],
    style ={'width': '50%', 'display':'inline-block'}),    
        
    html.Br(),   
    html.Div([
        dcc.RadioItems(
            id='xaxis',
            value='Bjork',
            options=[{'label': i, 'value': i} for i in code],
            labelStyle={'display': 'inline-block'}
        )
        
        
    ],
    style ={'width': '50%', 'display':'inline-block'}),    
    

    html.Div([
        dcc.Graph(id='dd-output-container',
        figure = fig
                  )
        ]),

  
    html.Div([
        dcc.Dropdown(
            id="dropdown_agent",
            options=[{'label': i, 'value': i} for i in agent],
            value='acw'   
        ),
    ],
    style ={'width': '21%'}),# 'display':'inline-block'}),  

    

    html.Div([
        dcc.Graph(id='dd-output-container2',
        figure = fig2
                  )
        ])
    ])



@app.callback(
    dash.dependencies.Output('dd-output-container', 'figure'),
    [dash.dependencies.Input("xaxis", 'value'),
     dash.dependencies.Input("dropdown_agent", 'value'), 
     dash.dependencies.Input('picker', 'start_date'),
     dash.dependencies.Input('picker', 'end_date')])
   



def update_output(xaxis, dropdown_agent, start_date, end_date):

        global df1m
        print(dropdown_agent)
           
    
        df1a = df1m.loc[(df1m['Code']== xaxis)]
        mask = (df1a['Date'] > start_date) & (df1a['Date'] <= end_date)
        df1 = df1a.loc[mask]
        
        #df1 = df1.loc[(df1['StatusKey']==dropdown_kpi)]
        
        y_data = 'Min'
        hover_data = ['UserId', 'Min']
        
        fig = px.scatter(df1, x  = 'Date',y = y_data ,color = 'StatusKey', hover_data=hover_data)
        return(fig)






@app.callback(
    dash.dependencies.Output('dd-output-container2', 'figure'),
    [dash.dependencies.Input("dropdown_agent", 'value'), 
     dash.dependencies.Input('picker', 'start_date'),
     dash.dependencies.Input('picker', 'end_date')])
   



def update_output2(dropdown_agent, start_date, end_date):

        global df1m
        print(dropdown_agent)
           
    
        df1a = df1m.loc[(df1m['UserId']== dropdown_agent)]
        mask = (df1a['Date'] > start_date) & (df1a['Date'] <= end_date)
        df1 = df1a.loc[mask]
        
        #df1 = df1.loc[(df1['StatusKey']==dropdown_kpi)]
        
        y_data = 'Min'
        hover_data = ['UserId', 'Min']
        
        fig2= px.line(df1, x  = 'Date',y = y_data ,color = 'StatusKey', hover_data=hover_data)
        return(fig2)



    
if __name__ == '__main__':
    #app.run_server(debug=False, dev_tools_ui=False,dev_tools_props_check=False)
    app.run_server(port ='8011', host='192.168.86.242',debug=False)
    #app.run_server(app,host = '172.28.89.75', port =8090)
    

    
    
'''







def update_output(dropdown_kpi, dropdown_agent, start_date, end_date):
        global df1
        df1a = df1.loc[(df1['UserId']== dropdown_agent)]
        mask = (df1a['Date'] > start_date) & (df1a['Date'] <= end_date)
        df1 = df1a.loc[mask]
        
        
        y_data = 'Min'
        hover_data = ['Date', 'Min']
        
        fig = px.scatter(df1, x  = 'UserId',y = y_data ,color = 'UserId', hover_data=hover_data)
        return(fig)

  	 
	html.Div([
		dcc.Graph(figure=fig)
	],
	style ={'width': '48%', 'display':'inline-block'}),
	





fig1 = px.timeline(df1, width=1200, height=600,x_start=df1["Date"], x_end=df1["Due"], y=df1["Course"],text= 'Pct',color = 'Pct',template='ggplot2',color_continuous_scale='Bluered_r', range_color=[0,100])
fig1.update_yaxes(autorange="reversed")

fig3 = px.bar(PHP, x='Pct', y='Course',  orientation='h',title='PH On Phone Completion Rate',color = 'Pct',template='ggplot2',color_continuous_scale='Bluered_r', range_color=[40,100])

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.Div(
        html.H1('Compliance Tracker'),
        style={'text-align': 'center'}
    ),
    html.Div([
        dcc.Graph(figure=fig1)
    ]),
		 
	html.Div([
		dcc.Graph(figure=fig2)
	],
	style ={'width': '48%', 'display':'inline-block'}),
	
	html.Div([
		dcc.Graph(figure=fig3)
	],
	style ={'width': '48%', 'display':'inl
         html.Div([
             dcc.Dropdown(
                 id="demo-dropdown2",
                 options=[{'label': i, 'value': i} for i in managers2],
                 value='Team Gilbert'   
             )
         ],
         style ={'width': '25%', 'display':'inline-block'}),

         html.Div([
             dcc.Graph(id='dd-output-container2')
             ])
        
     com = dfm.loc[dfm['Status']=='complete']
     tot_E = len(dfm)
     tot_C = len(com)
     pct = (tot_C/tot_E)*100
     pct2 = "%.2f" % pct    
         
@app.callback(
    dash.dependencies.Output('dd-output-container2', 'figure'),
    [dash.dependencies.Input("demo-dropdown2", 'value')])
    
def update_output2(value):

    dfm_off = df3_off[df3_off['Supervisor Name'] == value]
    com1 = dfm_off.loc[dfm_off['Status']=='complete']
    tot_E = len(dfm_off)
    tot_C = len(com1)
    pct = (tot_C/tot_E)*100
    pct2 = "%.2f" % pct
    mgr_pct = (value +": " +str(pct2))
    print(pct)
    
    fig2 = px.bar(dfm_off, x="Course", y="Lawson_y",title=mgr_pct, 
            color='Status',hover_name="Team_Member",
            height=500)

    
    return (fig2)

'''
'''
    html.Div([
        dcc.Dropdown(
            id="dropdown_kpi",
            options=[{'label': i, 'value': i} for i in KPI],
            value='acw'   
        ),
    ],
    style ={'width': '21%'}),# 'display':'inline-block'}),    
    



'''

'''
            #end_date = date(year,month,day),
'''







