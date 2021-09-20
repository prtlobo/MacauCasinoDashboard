# Earnings:
#   Past earnings growth
#   past revenue growth
#   Earnings and revenue history
#   Return on equity
#   Return on assets
#   Return on capital Employed

# 5 Past performance:
#   historical annual earnings growth
#   5.1 earnings and revenue history line chart
#   5.2 Past eanings growth analysis (5Y vs 1Y growth)
#   5.3 Return on equity
#   5.4 return on assets
#   5.5 return on capital employed

import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from datetime import datetime
import dash_bootstrap_components as dbc
import dash_daq as daq

from app import app
from API import dashboard_data,companies


layout = dict(
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
        ))

# Compound annual growth rate was modified to allow negative values.
# This was the source for the enhanced formualas:
# http://fortmarinus.com/blog/1214/

def CAGR(df,periods,y_column):
    if periods in [1,3,5]:
        year = periods
    else:
        year = df['year'].iloc[-1]-df['year'].iloc[0]
    end_val = df[y_column].iloc[-1]
    start_val = df[y_column].iloc[-(1+year)]
    start_date = (df['date'].iloc[-(1+year)]).strftime('%Y')
    end_date =  df['date'].iloc[-1].strftime('%Y')
    if start_val > 0 and end_val > 0:
        cagr=((end_val/start_val)**(1/year))-1
    elif start_val < 0 and end_val > 0:
        cagr=((end_val-start_val)/abs(start_val))**(1/year)
    elif start_val > 0 and end_val < 0:
        cagr = ((end_val+2*abs(end_val))/(start_val+2*abs(end_val)))**(1/year)-1
    return (cagr, start_date, end_date)

def make_CAGR_figure(option,periods,y_column,company):
    if option == 'compare':
        figure = go.Figure()
        for (n, df), color in zip(dashboard_data['a_income'].groupby(level=0,sort=False),companies['color']):
            figure.add_trace(
                go.Bar(
                    name=n,
                    x=[n],
                    y = [CAGR(df,periods,y_column)[0]],
                    width=0.5,
                    customdata= [CAGR(df,periods,y_column)],
                    text=[CAGR(df,periods,y_column)[0]],
                    textposition='auto',
                    texttemplate='%{y:.2f}%',
                    hovertemplate='Growth/Decline:%{y:.4f}% <br> From %{customdata[1]} to %{customdata[2]}',
                    marker_color=color))
        figure.update_layout(
            layout,
            xaxis=dict(
                categoryorder='total descending'),
            yaxis=dict(
                showticklabels=False))
    elif option =='single':
        figure=go.Figure()
        for period,name in zip([1,3,5,'IPO'],['1 Year', '3 Years','5 Years','IPO']):
            figure.add_trace(
                go.Bar(
                    name=name,
                    x=[name],
                    width=0.5,
                    y = [CAGR(dashboard_data['a_income'].loc[company],period,y_column)[0]],
                    customdata= [CAGR(dashboard_data['a_income'].loc[company],period,y_column)],
                    text=[CAGR(dashboard_data['a_income'].loc[company],period,y_column)[0]],
                    textposition='auto',
                    texttemplate='%{y:.2f}%',
                    hovertemplate='Growth/Decline:%{y:.4f}% <br> From %{customdata[1]} to %{customdata[2]}',
                    marker_color=companies.loc[companies['name']==company,'color'].item()))
            figure.update_layout(
                layout,
                yaxis=dict(
                    showticklabels=False))
    return (figure)

def make_scatter_figure(option, function, y_column, company):
    if option=='compare':
        figure = go.Figure()
        sorted_df=dashboard_data[function].reindex(index=dashboard_data[function]
                                            .groupby(level=0)[y_column].tail(1) \
                                            .sort_values(ascending=False) \
                                            .index \
                                            .get_level_values(0),level=0)
        for n, df in sorted_df.groupby(level=0,sort=False):
            figure.add_trace(
                go.Scatter(
                    name=n,
                    x = df['year'], 
                    y =df[y_column],
                    mode = 'lines+markers',
                    line=dict(
                        color=companies.loc[companies['name']==n,'color'].item(),
                        shape='spline')))

        figure.update_layout(layout,hovermode = 'x')
    elif option =='single':
        figure = go.Figure()
        figure.add_trace(
            go.Scatter(
                name = y_column,
                x = dashboard_data[function].loc[(company,'year')], 
                y = dashboard_data[function].loc[(company,y_column)],
                mode = 'lines+markers',
                line=dict(
                    color=companies.loc[companies['name']==company,'color'].item(),
                    shape='spline')))
        figure.update_layout(layout, hovermode = 'x')
    return figure

company_selector = html.Div([
        dbc.RadioItems(
            id="change_company_input_earning",
            className="btn-group",
            labelClassName="btn btn-primary",
            labelCheckedClassName="active",
            options=[{"label": c, "value": c} for c in companies['name']],
            value='SJM')],
        className="radio-group"
        )
CAGR_type = html.Div(
    [
        dbc.RadioItems(
            id='CAGR_radio_input',
            className="btn-group",
            labelClassName="btn btn-secondary",
            labelCheckedClassName="active",
            value=1,
            options=[{'label': '1 Year', 'value': 1},
                {'label': '3 Years', 'value': 3},
                {'label': '5 Years', 'value': 5},
                {'label': 'IPO', 'value': 'IPO'}
                ],
            
            )
        ],className="radio-group",
    )

compare_mode = daq.BooleanSwitch(
    id = 'compare_switch_earning',
    on = True,
    label = 'Compare Mode',
    labelPosition = 'bottom'
)

@app.callback(
    [
        Output('CAGR_output_revenue', 'figure'),
        Output('CAGR_output_netincome', 'figure')], 
        [Input('CAGR_radio_input', 'value')]
)
def revenue_CAGR(value):
    if value == 1:
        revenueCAGR=make_CAGR_figure('compare',1,'revenue',None)
        incomeCAGR=make_CAGR_figure('compare',1,'netIncome',None)
    elif value == 3:
        revenueCAGR=make_CAGR_figure('compare',3,'revenue',None)
        incomeCAGR=make_CAGR_figure('compare',3,'netIncome',None)
    elif value == 5:
        revenueCAGR=make_CAGR_figure('compare',5,'revenue',None)
        incomeCAGR=make_CAGR_figure('compare',5,'netIncome',None)
    elif value == 'IPO':
        revenueCAGR=make_CAGR_figure('compare','IPO','revenue',None)
        incomeCAGR=make_CAGR_figure('compare','IPO','netIncome',None)
    return revenueCAGR,incomeCAGR

@app.callback(
    [
        Output('change_company_output_CAGR_r', 'figure'),
        Output('change_company_output_CAGR_i', 'figure'),
        Output('change_company_output_ROE', 'figure'),
        Output('change_company_output_ROA', 'figure'),
        Output('change_company_output_ROCE', 'figure')],
        [Input('change_company_input_earning', 'value')]
)
def change_company(radio_items_value):
    CAGR_r = make_CAGR_figure('single',None,'revenue',radio_items_value)
    CAGR_i = make_CAGR_figure('single',None,'netIncome',radio_items_value)
    ROE = make_scatter_figure('single','ratios','returnOnEquity',radio_items_value)
    ROA = make_scatter_figure('single','ratios','returnOnAssets',radio_items_value)
    ROCE = make_scatter_figure('single','ratios','returnOnCapitalEmployed',radio_items_value)
    return CAGR_r,CAGR_i,ROE, ROA, ROCE

@app.callback(
    Output('hide_companies_earning', 'style'),
    [Input('compare_switch_earning', 'on')])
def hide_unhide(on):
    if on == True:
        hide = {'visibility':'hidden'}
    elif on == False:
        hide ={'visibility':'visible'}
    return hide

@app.callback(
    [Output('compare_layout_earning', 'children')],
    [Input('compare_switch_earning', 'on')])
def update_layout(on):
    if on == True:
        output_layout = [(
            dbc.Row([
                dbc.Col(
                    html.H3('Past Revenue Growth'),width=6),
                dbc.Col(
                    html.H3('Past Net Income Growth'),width=6)]),
                dbc.Row(
                    dbc.Col(CAGR_type)),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='CAGR_output_revenue'),width=6),
                    dbc.Col(
                        dcc.Graph(id='CAGR_output_netincome'),width=6)]),
                dbc.Row(
                    dbc.Col(
                        html.H3('Return on Equity'))),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=make_scatter_figure('compare','ratios','returnOnEquity',None)))),
                dbc.Row(
                    dbc.Col(
                        html.H3('Return on Assets'))),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=make_scatter_figure('compare','ratios','returnOnAssets',None)))),
                dbc.Row(
                    dbc.Col(
                        html.H3('Return on Capital Employed'))),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=make_scatter_figure('compare','ratios','returnOnCapitalEmployed',None)))),
                    )]
    elif on == False:
        output_layout = [(
            dbc.Row([
                dbc.Col(
                    html.H3('Past Revenue Growth'),width=6),
                dbc.Col(
                    html.H3('Past Net Income Growth'),width=6)]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='change_company_output_CAGR_r'),width=6),
                dbc.Col(
                    dcc.Graph(id='change_company_output_CAGR_i'),width=6)]),
            dbc.Row(
                dbc.Col(
                    html.H3('Return on Equity'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_ROE'))),
            dbc.Row(
                dbc.Col(
                    html.H3('Return on Assets'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_ROA'))),
            dbc.Row(
                dbc.Col(
                    html.H3('Return on Capital Employed'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_ROCE')))
                    )]
    return output_layout

earninglayout = html.Div(
    dbc.Spinner(children=[
        dbc.Row([
            dbc.Col(id='hide_companies_earning',children=company_selector),
            dbc.Col(
                html.Div(compare_mode,style={'float':'right'}))],justify='between'),
        html.Div(id='compare_layout_earning')]),id='loading-output')