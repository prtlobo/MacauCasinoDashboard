# 7 dividend:
#   current dividend yield
#   7.1 dividend yield vs market
#   7.2 stability and growth of payments line chart
#   7.3 Current payout to shareholders
#   7.4 future payout to shareholders
# Dividend:
#   Dividend stability and growth
#   Dividend payout ratio


import pandas as pd
import plotly.graph_objects as go
#import dash
#import plotly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from datetime import datetime
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import plotly.io as pio
import dash_daq as daq
#import json

from app import app
from API import dashboard_data,companies

dashboard_data['dividend']['quarters']=dashboard_data['dividend']['date'].dt.quarter
dashboard_data['dividend'] = dashboard_data['dividend'].merge(dashboard_data['stock'],
                                                            left_on=['Company','date'], 
                                                            right_on=['Company','date']).set_index(dashboard_data['dividend'].index)
dashboard_data['dividend']['divYield'] = dashboard_data['dividend']['adjDividend']/dashboard_data['dividend']['close']

figure_layout = dict(
    template='plotly_dark',
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_showgrid = False,
    yaxis=dict(
        showgrid = False,
        rangemode='tozero'
        ),
    legend=dict(
        orientation='h',
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        ),
    modebar=dict(
        orientation='v',
        bgcolor='rgba(0,0,0,0)'
        )
    )
def make_payout_scatter_figure(option,company):
    if option == 'compare':
        figure=go.Figure()
        sorted_df=dashboard_data['ratios'].reindex(index=dashboard_data['ratios']
        .groupby(level=0)['payoutRatio'].tail(1)\
        .sort_values(ascending=False)\
        .index\
        .get_level_values(0),level=0
        )

        for n, df in sorted_df.groupby(level=0,sort=False):
            figure.add_trace(
                go.Scatter(
                    name=n,
                    x = df['year'], 
                    y =df['payoutRatio'],
                    mode = 'lines+markers',
                    line=dict(
                        color=companies.loc[companies['name']==n,'color'].item(),
                        shape='spline'
                        )
                    )
                )
        figure.update_layout(figure_layout, hovermode = 'x')
    elif option == 'single':
        figure = go.Figure()
        figure.add_trace(
            go.Scatter(
                name='Payout Ratio',
                x = dashboard_data['ratios'].loc[(company,'date')], 
                y =dashboard_data['ratios'].loc[(company,'payoutRatio')],
                mode = 'lines+markers',
                xperiod='M1',
                xperiodalignment='middle',
                fill='tozeroy',
                line=dict(
                    color=companies.loc[companies['name'] == company,'color'].item(),
                    shape='spline')
                    )
                )
    figure.update_layout(
        figure_layout,
        hovermode = 'x unified'
        )
    return figure
def make_payout_pie_figure(year, company):
    
    #Find company then find row (which is date) then create smaller df of net income and dividends paid.
    df=dashboard_data['a_cash'].xs(company).loc[dashboard_data['a_cash'].xs(company)['date']==year,['netIncome','dividendsPaid']]
    df.reset_index(inplace=True,drop=True)
    #Color section of pie depending if net income was positive or negative
    df['color']= ['crimson' if income <0 else 'forestgreen' for income in df['netIncome']]
    #color of dividends paid section
    color=[df['color'].loc[0],'darkslateblue']
    #get absolute value before plotting or else it won't work
    df=df[['netIncome','dividendsPaid']].abs()
    
    figure = go.Figure()
    figure.add_trace(
        go.Pie(
            labels=df.columns,
            values=df.loc[0],
            textinfo='label+percent',
            textposition='outside',
            sort=False, 
            marker_colors=color
            )
        )
    figure.update_layout(figure_layout)
    return figure

def make_dividend_figure(company,y_column,option):
    if option=='compare':
        figure = go.Figure()
        sorted_df=dashboard_data['dividend'].reindex(index=dashboard_data['dividend']
                        .groupby(level=0)[y_column].tail(1) \
                        .sort_values(ascending=False) \
                        .index \
                        .get_level_values(0),
                level=0)
        for n, df in sorted_df.groupby(level=0,sort=False):
            figure.add_trace(
                go.Scatter(
                    x = df['date'], 
                    y =df[y_column],
                    mode = 'lines+markers',
                    name=n,
                    xperiod='M3',
                    line=dict(
                        color=companies.loc[companies['name']==n,'color'].item(),
                        shape='spline'
                        )
                    )
                )
        figure.update_layout(
            figure_layout,
            hovermode = 'x',
            yaxis_showgrid = False,
            xaxis=dict(
                showgrid=False,
                tickangle = 0,
                dtick = 'M3',
                tickformat="Q%q\n%Y",
                ticklabelmode="period"
                )
            )
    elif option =='single':
        figure = go.Figure()
        figure = make_subplots(specs=[[{"secondary_y": True}]])
        figure.add_trace(
            go.Bar(
                name='Dividends', 
                x = dashboard_data['dividend'].loc[(company,'date')], 
                y = dashboard_data['dividend'].loc[(company,'adjDividend')],
                xperiod='M1',
                xperiodalignment = 'middle'
                ),secondary_y=False
            )
        figure.add_trace(
            go.Scatter(
                name='Dividend Yield', 
                x = dashboard_data['dividend'].loc[(company,'date')], 
                y = dashboard_data['dividend'].loc[(company,'divYield')],
                mode = 'lines+markers',
                xperiod = 'M1',
                xperiodalignment = 'middle',
                line=dict(
                    color=companies.loc[companies['name'] == company,'color'].item(),
                    shape='spline'
                    )
                ),secondary_y=True
            )
        figure.update_layout(
            figure_layout,
            hovermode = 'x unified',
            yaxis=dict(
                title='Dividend per share (DPS)',
                tickprefix='$',
                showgrid=False,
                rangemode='tozero'
            ),
            yaxis2=dict(
                title='Dividend Yield',
                anchor='y',
                overlaying='y',
                side='right',
                tickformat='.2%',
                rangemode='tozero',
                showgrid=False
            ),
            xaxis=dict(
                tickangle = 0,
                dtick = 'M3',
                tickformat="Q%q\n%Y",
                ticklabelmode="period")
                            )
    return figure

company_selector = html.Div(
    [
        dbc.RadioItems(
            id="change_company_input_dividend",
            className="btn-group",
            labelClassName="btn btn-primary",
            labelCheckedClassName="active",
            options=[{"label": c, "value": c} for c in companies['name']],
            value='SJM',
        ),
    ],
    className="radio-group",
)

compare_mode = daq.BooleanSwitch(
    id = 'compare_switch_dividend',
    on = True,
    label = 'Compare Mode',
    labelPosition = 'bottom'
)

@app.callback(
    Output('hide_companies_dividend', 'style'),
    [Input('compare_switch_dividend', 'on')]
    )
def hide_unhide(on):
    if on == True:
        hide = {'visibility':'hidden'}
    elif on == False:
        hide ={'visibility':'visible'}
    return hide

@app.callback(
    [
        Output('change_company_output_dividend', "figure"),
        Output('change_company_output_payout', "figure")
        ],
    Input("change_company_input_dividend", "value")
    )
def change_company(radio_items_value):
    dividend=make_dividend_figure(radio_items_value,None,'single')
    payout = make_payout_scatter_figure('single', radio_items_value)
    return dividend,payout

@app.callback(
       Output('hover_pie_figure_output', 'figure'),
    [
        Input('change_company_output_payout', 'hoverData'),
        Input('change_company_input_dividend', "value")
        ]
    )
def change_pie_on_hover(hoverData,radio_items_value,):
    if hoverData==None:
        figure = make_payout_pie_figure(dashboard_data['ratios']['date'].max(),
                                        radio_items_value)
    else:
        date = datetime.strptime(hoverData['points'][0]['x'],'%Y-%m-%d')
        figure = make_payout_pie_figure(date,radio_items_value)
    return figure
@app.callback(
    [Output('compare_layout_dividend', 'children')],
    [Input('compare_switch_dividend', 'on')]
    )
def update_layout(on):
    if on == True:
        output_layout = [(
            dbc.Row(
                dbc.Col(
                    html.H3('Adjusted Dividend'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(figure=make_dividend_figure(None,'adjDividend','compare')))),
            dbc.Row(
                dbc.Col(
                    html.H3('Dividend Yield'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(figure=make_dividend_figure(None,'divYield','compare')))),
            dbc.Row(
                dbc.Col(
                    html.H3('Payout Ratio'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(figure=make_payout_scatter_figure('compare', None)))),
                    )]
    elif on == False:
        output_layout = [(
            dbc.Row(
                dbc.Col(
                    html.H3('Dividend'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_dividend'))),
            dbc.Row(
                dbc.Col(
                    html.H3('Payout Ratio'))),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id='change_company_output_payout'),width=8),
                    dbc.Col(
                        dcc.Graph(id='hover_pie_figure_output'),width=4)
                        ])
                    )]
    return output_layout
# add spinner to individual divs
dividendlayout = html.Div(
    [
        dbc.Row([
            dbc.Col(id='hide_companies_dividend',children=company_selector),
            dbc.Col(
                html.Div(compare_mode,style={'float':'right'}))],justify='between'),
        html.Div(id='compare_layout_dividend')])
