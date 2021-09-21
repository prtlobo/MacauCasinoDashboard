#   Valuation:
#       Fair Value(DCF)
#       Price to Earnings
#       Price to Book
#       Price to earnings Growth

# 3 Valuation:
#   price to earnings ratio
#   3.1 share price vs fair value
#   3.2 Price to earnings ratio
#   3.3 Price to earning growth ratio
#   3.4 Price to book ratio

import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
#import datetime
#from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
#import plotly.io as pio
import dash_daq as daq

from app import app
from API import dashboard_data,companies

dashboard_data['a_DCF']['undervalue'] = ((dashboard_data['a_DCF']['price'] / dashboard_data['a_DCF']['dcf']))
dashboard_data['dcf']['undervalue']=((dashboard_data['dcf']['Stock Price'] / dashboard_data['dcf']['dcf']))
dashboard_data['dcf']['undervalue%']=1-dashboard_data['dcf']['undervalue']
dashboard_data['dcf']['dcfstring'] = ['Undervalued' if x >= 0 else 'Overvalued' for x in dashboard_data['dcf']['undervalue%']]
dashboard_data['dcf'].reset_index(inplace=True)
dashboard_data['dcf'].sort_values(by='undervalue',ascending=False,inplace=True)
dashboard_data['dcf'].rename(columns={'Company':'name'},inplace=True)
dashboard_data['dcf'] = dashboard_data['dcf'].merge(right=companies,on='name')
layout = dict(
    template='plotly_dark',
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode = 'x',
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
#hovertemplate=('Price: %{customdata[1]} <br>'
#                                'DCF: %{customdata[2]} <br>' 
#                                '%{customdata[4]} by: %{customdata[3]:.2%}'),
def make_bullet_figures(company,option):
    if option=='compare':
        output=go.Figure()
        output.add_trace(
            go.Scatter(
                text='DCF',
                x=dashboard_data['dcf']['undervalue'],
                y=dashboard_data['dcf']['name'],
                customdata=dashboard_data['dcf'][['Stock Price','dcf','dcfstring','undervalue%']],
                hovertemplate='Price: %{customdata[0]} <br>DCF: %{customdata[1]:.2f} <br>%{customdata[2]} by: %{customdata[3]:.2%}<extra></extra>',
                mode='markers',
                marker=dict(
                    symbol='152',
                    size=15,
                    color=dashboard_data['dcf']['color']
                )
            )
        )
        output.update_layout(layout)
        output.update_xaxes(
            range=[0,1.5],
            dtick=0.1
        )
        output.add_vline(x=1, line_dash='dash')
        output.add_vrect(
            x0=0, 
            x1=1, 
            line_width=0, 
            fillcolor="green", 
            opacity=0.2, 
            annotation_text='UNDERVALUED', 
            annotation_position='top right',
            layer='below'
            )
        output.add_vrect(
            x0=1, 
            x1=1.5, 
            line_width=0, 
            fillcolor="red", 
            opacity=0.2,
            annotation_text='OVERVALUED', 
            annotation_position='top left',
            layer = 'below'
            )
    elif option == 'single':
        output=go.Figure()
        output.add_trace(go.Indicator(
            mode='gauge',
            gauge = {
                'shape': 'bullet',
                'bar': {
                    'color': 'black',
                    'thickness':0},
                'axis': {
                    'range': [None, 2],
                    'dtick':0.1},
                'threshold': {
                        'line': {'color': 'black', 'width': 2},
                        'thickness': 0.75,
                        'value': dashboard_data['dcf'].loc[dashboard_data['dcf']['name'] == company, 'undervalue'].item()},
                'steps': [
                    {'range': [0, 1], 'color': 'green'},
                    {'range': [1, 2], 'color': 'red'}]}
        ))
        output.add_annotation(
            align='center',
            x = dashboard_data['dcf'].loc[dashboard_data['dcf']['name'] == company, 'undervalue'].item()/2,
            y=1.7,
            yref='paper',
            showarrow=False,
            text=round(dashboard_data['dcf'].loc[dashboard_data['dcf']['name'] == company, 'undervalue'].item(),3),
        )
        output.add_annotation(
            align='center',
            x=0,
            showarrow=False,
            text='Undervalued',
        )
        output.add_annotation(
            align='center',
            x=1,
            showarrow=False,
            text='Overvalued',
        )
        output.update_layout(
            height=70,
            template='plotly_dark',
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(
            l=20, 
            r=20, 
            b=20, 
            t=20
        )
            )
    return output
def make_scatter_figure_dcf(company, option):
    if option == 'compare':
        figure = go.Figure()
        ymax = dashboard_data['a_DCF']['undervalue'].max()*1.05
        figure.add_hline(y=1, line_dash='dash')
        figure.add_hrect(
            y0=0, 
            y1=1, 
            line_width=0, 
            fillcolor="green", 
            opacity=0.2, 
            annotation_text='UNDERVALUED', 
            annotation_position='top left',
            layer='below'
            )
        figure.add_hrect(
            y0=1, 
            y1=ymax, 
            line_width=0, 
            fillcolor="red", 
            opacity=0.2,
            annotation_text='OVERVALUED', 
            annotation_position='bottom left',
            layer = 'below'
            )
        sorted_df=dashboard_data['a_DCF'].reindex(index=dashboard_data['a_DCF']
                                        .groupby(level=0)['undervalue'].tail(1) \
                                        .sort_values(ascending=True) \
                                        .index \
                                        .get_level_values(0),
                                        level=0)
        for n, df in sorted_df.groupby(level=0,sort=False):
            figure.add_trace(
                go.Scatter(
                    name = n,
                    x = df['year'], 
                    y =df['undervalue'],
                    mode = 'lines+markers',
                    line=dict(
                        color=companies.loc[companies['name']==n,'color'].item(),
                        shape='spline'
                        )
                    )
                )
        figure.update_yaxes(zeroline=False)
        figure.update_layout(layout)
    elif option=='single':
        figure = go.Figure()
        figure.add_trace(
            go.Scatter(
                name ='Fair Value',
                x = dashboard_data['a_DCF'].loc[(company,'date')], 
                y = dashboard_data['a_DCF'].loc[(company,'dcf')], 
                mode = 'lines+markers',
                line=dict(
                    color='purple',
                    shape= 'spline'
                    )
                )
            )
        figure.add_trace(
            go.Scatter(
                name ='Price',
                x = dashboard_data['a_DCF'].loc[(company,'date')], 
                y = dashboard_data['a_DCF'].loc[(company,'price')], 
                mode = 'lines+markers',
                line=dict(
                    color=companies.loc[companies['name']==company,'color'].item(),
                    shape='spline'
                    )
                )
            )
        figure.update_layout(layout)
    return figure

def make_scatter_figure(company,y_column,option):
    if option=='compare':
        figure = go.Figure()
        sorted_df=dashboard_data['ratios'].reindex(index=dashboard_data['ratios']
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
                        shape='spline'
                        )
                    )
                )
        figure.update_layout(layout)
    elif option =='single':
        figure = go.Figure()
        figure.add_trace(
            go.Scatter(
                name = y_column,
                x = dashboard_data['ratios'].loc[(company,'year')], 
                y =dashboard_data['ratios'].loc[(company,y_column)],
                mode = 'lines+markers',
                fill='tozeroy',
                line=dict(
                    color=companies.loc[companies['name']==company,'color'].item(),
                    shape= 'spline'
                    )
                )
            )
        figure.update_layout(layout)
    return figure

company_selector = html.Div(
    [
        dbc.RadioItems(
            id="change_company_input_valuation",
            className="btn-group",
            labelClassName="btn btn-primary",
            labelCheckedClassName="active",
            options=[{"label": c, "value": c} for c in companies['name']],
            value='SJM',
            )
        ],className="radio-group",
    )
compare_mode = daq.BooleanSwitch(
    id = 'compare_switch_valuation',
    on = True,
    label = 'Compare Mode',
    labelPosition = 'bottom'
)
@app.callback(
    Output('hide_companies_valuation', 'style'),
    Input('compare_switch_valuation', 'on')
    )
def hide_unhide(on):
    if on == True:
        hide = {'visibility':'hidden'}
    elif on == False:
        hide ={'visibility':'visible'}
    return hide

@app.callback(
    [
        Output("change_company_output_fairdcf", "figure"),
        Output("change_company_output_PEG", "figure"),
        Output("change_company_output_P/B", "figure"),
        Output("change_company_output_P/E", "figure"),
        Output("change_company_output_bullet", "figure")
        ],
    Input("change_company_input_valuation", "value")
    )
def change_company(radio_items_value):
    fair_DCF = make_scatter_figure_dcf(radio_items_value,'single')
    PEG = make_scatter_figure(radio_items_value,'priceEarningsToGrowthRatio','single')
    P2B = make_scatter_figure(radio_items_value,'priceToBookRatio','single')
    P2E = make_scatter_figure(radio_items_value,'priceEarningsRatio','single')
    bullet = make_bullet_figures(radio_items_value,'single')
    return fair_DCF,PEG, P2B, P2E, bullet
@app.callback(
    [Output('compare_layout_valuation', 'children')],
    [Input('compare_switch_valuation', 'on')],
    )
def update_layout(on):
    if on == True:
        output_layout = [(
            dbc.Row(
                dbc.Col(
                    html.H3('Current Fair Value Ratio'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(figure=make_bullet_figures(None,'compare'))
                    )),
            dbc.Row(
                dbc.Col(
                    html.H3('Historic Fair Value (Discounted Cash Flow)'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(figure=make_scatter_figure_dcf(None,'compare')))),
            dbc.Row(
                dbc.Col(
                    html.H3('Price to Earnings Growth'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(figure=make_scatter_figure(None,'priceEarningsToGrowthRatio','compare')))),
            dbc.Row(
                dbc.Col(
                    html.H3('Price to Book'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(figure=make_scatter_figure(None,'priceToBookRatio','compare')))),
            dbc.Row(
                dbc.Col(
                    html.H3('Price to Earnings'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(figure=make_scatter_figure(None,'priceEarningsRatio','compare'))))
                    )]
    elif on == False:
        output_layout = [(
            dbc.Row(
                dbc.Col(
                    html.H3('Current Fair Value Ratio'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_bullet',config = {'displayModeBar': False})
                    )),
            dbc.Row(
                dbc.Col(
                    html.H3('Fair Value (Discounted Cash Flow)'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_fairdcf'))),
            dbc.Row(
                dbc.Col(
                    html.H3('Price to Earning Growth'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_PEG'))),
            dbc.Row(
                dbc.Col(
                    html.H3('Price to Book'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_P/B'))),
            dbc.Row(
                dbc.Col(
                    html.H3('Price to Earnings'))),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='change_company_output_P/E')))
                        )]
    return output_layout

valuationlayout = html.Div(
    dbc.Spinner(children=[
        dbc.Row([
            dbc.Col(id='hide_companies_valuation',children=company_selector),
            dbc.Col(
                html.Div(compare_mode,style={'float':'right'}))],justify='between'),
        html.Div(id='compare_layout_valuation')
        ]),id='loading-output')

