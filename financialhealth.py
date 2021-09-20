#   Financial health:
#       Profit Margin
#       Assets to liabilities
#       Cash Flow
# 6 financial health:
#   6.1 financial position short term & long term assest vs liabilites bar chart
#   6.2 Debt to equity history (debt vs equity line chart)
#   6.3 balance sheet marimekko charts

import pandas as pd
import plotly.graph_objects as go
import dash
#import plotly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
#import datetime
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
#import plotly.io as pio
import dash_daq as daq

from app import app
from API import dashboard_data, companies


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

def make_scatter_figure(function , y_column):
    figure = go.Figure()
    sorted_df=dashboard_data[function].reindex(index=dashboard_data[function]
                                    .groupby(level=0)[y_column].tail(1) \
                                    .sort_values(ascending=False) \
                                    .index \
                                    .get_level_values(0),
                                        level=0)
    for n, df in sorted_df.groupby(level=0,sort=False):
        figure.add_trace(
            go.Scatter(
                x = df['year'], 
                y =df[y_column],
                mode = 'lines+markers',
                name=n,
                line=dict(
                    color=companies.loc[companies['name']==n,'color'].item(),
                            shape='spline')
                            )
                        )
    figure.update_layout(figure_layout, hovermode='x')
    return figure

company_selector = html.Div(
    [
        dbc.RadioItems(
            id="change_company_input_health",
            className="btn-group",
            labelClassName="btn btn-primary",
            labelCheckedClassName="active",
            options=[{"label": c, "value": c} for c in companies['name']],
            value='SJM',
        )
    ],className="radio-group",
)

profit_radio = html.Div(
    [
        dbc.RadioItems(
            id='profit_radio_input',
            className="btn-group",
            labelClassName="btn btn-secondary",
            labelCheckedClassName="active",
            value=1,
            options=[
                {"label": "Profit Margin", "value": 1},
                {"label": "Revenue", "value": 2},
                {"label": "Net Income", "value": 3},
                ],
        ),
    ],className="radio-group"
)
debt_equity_radio = html.Div(
    [
        dbc.RadioItems(
            id='debt_equity_input',
            className="btn-group",
            labelClassName="btn btn-secondary",
            labelCheckedClassName="active",
            value=1,
            options=[
                {"label": "Debt to Equity", "value": 1},
                {"label": "Total Assets", "value": 2},
                {"label": "Total Liabilities", "value": 3},
            ],
        ),
    ],className="radio-group"
)
cash_flow_radio = html.Div(
    [
        dbc.RadioItems(
            id='cash_flow_input',
            className="btn-group",
            labelClassName="btn btn-secondary",
            labelCheckedClassName="active",
            value=1,
            options=[
                {"label": "Operating Activities", "value": 1},
                {"label": "Investing Activities", "value": 2},
                {"label": "Financing Activities", "value": 3},
                ],
        ),
    ],className="radio-group"
)

compare_mode = daq.BooleanSwitch(
    id = 'compare_switch_health',
    on = True,
    label = 'Compare Mode',
    labelPosition = 'bottom'
)
@app.callback(
    Output('profit_radio_output', 'figure'), 
    [Input('profit_radio_input', 'value')]
    )
def profit_margin_type(value):
    if value == 1:
        figure=make_scatter_figure('ratios','netProfitMargin')
    elif value == 2:
        figure=make_scatter_figure('a_income','revenue')
    elif value == 3:
        figure=make_scatter_figure('a_income', 'netIncome')
    return figure
@app.callback(
    Output('debt_equity_output', 'figure'), 
    [Input('debt_equity_input', 'value')]
    )
def debt_equity_type(value):
    if value == 1:
        figure=make_scatter_figure('ratios','debtEquityRatio')
    elif value == 2:
        figure= make_scatter_figure('a_balance','totalAssets')
    elif value == 3:
        figure=make_scatter_figure('a_balance','totalLiabilities')
    return figure
@app.callback(
    Output('hide_companies_health', 'style'),
    [Input('compare_switch_health', 'on')]
    )
def hide_unhide(on):
    if on == True:
        hide = {'visibility':'hidden'}
    elif on == False:
        hide ={'visibility':'visible'}
    return hide

@app.callback(
    Output('cash_flow_output', 'figure'), 
    [Input('cash_flow_input', 'value')]
    )
def cash_flow_type(value):
    if value == 1:
        figure=make_scatter_figure('a_cash','netCashProvidedByOperatingActivities')
    elif value == 2:
        figure= make_scatter_figure('a_cash','netCashUsedForInvestingActivites')
    elif value == 3:
        figure=make_scatter_figure('a_cash','netCashUsedProvidedByFinancingActivities')
    return figure

@app.callback(
    [
        Output("change_company_output_profit", "figure"),
        Output("change_company_output_debt", "figure"),
        Output("change_company_output_cash", "figure")
        ],
    Input("change_company_input_health", "value")
    )
def change_company(radio_items_value):
    profit_margin=go.Figure()
    profit_margin = make_subplots(specs=[[{"secondary_y": True}]])
    profit_margin.add_trace(
        go.Bar(
            name='Revenue', 
            x=dashboard_data['a_income'].loc[(radio_items_value,'year')], 
            y= dashboard_data['a_income'].loc[(radio_items_value,'revenue')],
            marker_color='darkgreen'
            ),secondary_y=False
        )
    profit_margin.add_trace(
        go.Bar(
            name='Net Income', 
            x=dashboard_data['a_income'].loc[(radio_items_value,'year')], 
            y=dashboard_data['a_income'].loc[(radio_items_value,'netIncome')],
            marker_color='orange'
            ),secondary_y=False
            )
    profit_margin.add_trace(
        go.Scatter(
            x = dashboard_data['ratios'].loc[(radio_items_value,'year')], 
            y =dashboard_data['ratios'].loc[(radio_items_value,'netProfitMargin')],
            mode = 'lines',
            name='Net Profit Margin',
            line=dict(
                color=companies.loc[companies['name']==radio_items_value,'color'].item(),
                shape='spline'
                )
            ),secondary_y=True
        )

    profit_margin.update_layout(
        figure_layout, 
        hovermode='x unified',
        xaxis=dict(
            spikedash='solid',
            spikemode='across+marker'
            )
        )

    A_to_L = make_subplots(specs=[[{"secondary_y": True}]])
    A_to_L.add_trace(
        go.Bar(
            name='Assets', 
            x=dashboard_data['a_balance'].loc[(radio_items_value,'year')], 
            y= dashboard_data['a_balance'].loc[(radio_items_value,'totalAssets')],
            marker_color='navy'
            ),secondary_y=False
        )
    A_to_L.add_trace(
        go.Bar(
            name='Liabilities', 
            x=dashboard_data['a_balance'].loc[(radio_items_value,'year')], 
            y=dashboard_data['a_balance'].loc[(radio_items_value,'totalLiabilities')],
            marker_color='crimson'
            ),secondary_y=False
        )
    A_to_L.add_trace(
        go.Scatter(
            x = dashboard_data['ratios'].loc[(radio_items_value,'year')], 
            y =dashboard_data['ratios'].loc[radio_items_value,'debtEquityRatio'],
            mode = 'lines',
            name='Debt to Equity Ratio',
            line=dict(
                color=companies.loc[companies['name']==radio_items_value,'color'].item(),
                shape='spline')
                ),secondary_y=True
            )
    A_to_L.update_layout(
        figure_layout, 
        hovermode='x unified', 
        xaxis=dict(
            spikedash='solid',
            spikemode='across+marker'
            ),
        )

    cash_flow = go.Figure()
    cash_flow.add_trace(
        go.Bar(
            name='Operating', 
            x=dashboard_data['a_cash'].loc[(radio_items_value,'year')], 
            y= dashboard_data['a_cash'].loc[(radio_items_value,'netCashProvidedByOperatingActivities')]
            )
        )
    cash_flow.add_trace(
        go.Bar(
            name='Investing', 
            x=dashboard_data['a_cash'].loc[(radio_items_value,'year')], 
            y=dashboard_data['a_cash'].loc[(radio_items_value,'netCashUsedForInvestingActivites')]
            )
        )
    cash_flow.add_trace(
        go.Bar(
            name='Financing', 
            x=dashboard_data['a_cash'].loc[(radio_items_value,'year')], 
            y=dashboard_data['a_cash'].loc[(radio_items_value,'netCashUsedProvidedByFinancingActivities')]
            )
        )
    cash_flow.update_layout(
        figure_layout, 
        hovermode='x unified',
        xaxis=dict(
            spikedash='solid',
            spikemode='across+marker'
            )
        )
    return profit_margin, A_to_L, cash_flow

@app.callback(
    [Output('compare_layout_health', 'children')],
    [Input('compare_switch_health', 'on')]
    )
def update_layout(on):
    if on == True:
        output_layout = [(
            dbc.Row(
                dbc.Col(
                    html.H3('Profit Margin'))),
            dbc.Row(
                dbc.Col(profit_radio)),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='profit_radio_output'))),
            dbc.Row(
                dbc.Col(
                   html.H3('Assets & Liabilites'))),
            dbc.Row(
                dbc.Col(
                    html.Div(debt_equity_radio))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='debt_equity_output'))),
            dbc.Row(
                dbc.Col(
                   html.H3('Cash Flows'))),
            dbc.Row(
                dbc.Col(
                    html.Div(cash_flow_radio))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='cash_flow_output')))
                    )]
    elif on == False:
        output_layout = [(
            dbc.Row(
                dbc.Col(
                    html.H3('Profit Margin'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_profit'))),
            dbc.Row(
                dbc.Col(
                    html.H3('Assets & Liabilites'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_debt'))),
            dbc.Row(
                dbc.Col(
                    html.H3('Cash Flow'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_cash')))
                    )]
    return output_layout

financialhealthlayout= html.Div(
    dbc.Spinner(children=[
        dbc.Row([
            dbc.Col(id='hide_companies_health',children=company_selector),
            dbc.Col(
                html.Div(compare_mode,style={'float':'right'}))],justify='between'),
        html.Div(id='compare_layout_health')],id='loading-output'))
