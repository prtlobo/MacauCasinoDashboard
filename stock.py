import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from datetime import timedelta,datetime
import dash_bootstrap_components as dbc
import dash_daq as daq

from main_app import app
from API import dashboard_data,companies

dashboard_data['quote']['earningsAnnouncement'] = pd.to_datetime(dashboard_data['quote']['earningsAnnouncement'])
dashboard_data['quote'].sort_values(by='price',inplace=True, ascending=False)
figure_layout = dict(
    template='plotly_dark',
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x',
    
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
def create_indicators():
    output=[]
    for n,df in dashboard_data['quote'].groupby(level=0,sort=False):
        fig=go.Figure()
        fig.add_trace(go.Indicator(
                        mode = "number+delta",
                        value = df['price'].item(),
                        delta=dict(
                            reference=df['price'].item()+df['change'].item(),
                            relative=True
                            )
                        ))
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=90,
            width=90,
            margin=dict(
                l=0, 
                r=0, 
                b=0, 
                t=0
            ))
        output.append(dbc.Card([
                        dbc.CardHeader(n),
                        dbc.CardBody([
                            html.Div([
                            dcc.Graph(
                                figure=fig,
                                config={'displayModeBar': False})
                            ],style={'display':'flex','justify-content':'center'})])],className='card text-center'))
    return output
def make_scatter_figure(option, function, y_column, company):
    if option=='compare':
        sorted_df=dashboard_data[function].reindex(index=dashboard_data[function]
                                            .groupby(level=0)[y_column].tail(1) \
                                            .sort_values(ascending=False) \
                                            .index \
                                            .get_level_values(0),
                                    level=0)
        figure = go.Figure()
        for n, df in sorted_df.groupby(level=0,sort=False):
            figure.add_trace(
                go.Scatter(
                    name=n,
                    x = df['date'], 
                    y =df[y_column],
                    mode = 'lines',
                    line=dict(
                        color=companies.loc[companies['name']==n,'color'].item(),
                        shape='spline'
                        )
                    )
                )
        figure.update_layout(
            figure_layout,
            height=730,
            yaxis=dict(
                showgrid =False,
                rangemode='tozero'
                ),
            xaxis=dict(
                showgrid=False,
                ticks ='outside',
                ticklen = 10,
                rangeslider_visible=True,
                rangeselector=dict(
                    bgcolor='rgba(0,0,0,0)',
                    activecolor='rgba(71,71,71,1)',
                    buttons=list([
                        dict(count=0, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(count=5, label="5y", step="year", stepmode="backward"),
                        dict(step="all")
                        ])
                    )
                )
            )
    elif option =='single':
        figure = go.Figure()
        figure.add_trace(
            go.Scatter(
                name = y_column,
                x = dashboard_data[function].loc[(company,'date')], 
                y =dashboard_data[function].loc[(company,y_column)],
                mode = 'lines',
                line=dict(
                    color=companies.loc[companies['name']==company,'color'].item(),
                    shape='spline'
                    ),
                )
            )
        figure.add_trace(go.Indicator(
                        mode = "number+delta",
                        value = dashboard_data['quote'].loc[(company,'price')].item(),
                        delta=dict(
                            reference=dashboard_data['quote'].loc[(company,'price')].item()+dashboard_data['quote'].loc[(company,'change')].item(),
                            relative=True
                            ),
                        domain = {'x': [0.9, 1],'y': [0.8, 1]},
                        title= dict(
                            text='Latest Price',
                            font_size=10
                            )
                        ))
        figure.update_layout(
            figure_layout,
            height=730,
            yaxis=dict(
                showgrid =False,
                rangemode='tozero'
                ),
            xaxis=dict(
                showgrid=False,
                ticks ='outside',
                ticklen = 10,
                rangeslider_visible=True,
                rangeselector=dict(
                    bgcolor='rgba(0,0,0,0)',
                    activecolor='rgba(71,71,71,1)',
                    buttons=list([
                        dict(count=0, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(count=5, label="5y", step="year", stepmode="backward"),
                        dict(step="all")
                        ])
                    )
                )
            )
            
    return figure

def make_cumilative_figure(option, function, y_column, company, period):
    # Periods to calculate daily returns for
    periods={
                '6M':timedelta(days=182.5),
                'YTD':timedelta(days=365),
                '3Y':timedelta(days=365*3),
                }
    if option=='compare':
        figure = go.Figure()
        for n, df in dashboard_data[function].groupby(level=0,sort=False):
            #Update periods to include period of since IPO
            periods['IPO']=df['date'].iloc[-1]-df['date'].iloc[0]
            mask=(df['date']>df['date'].iloc[-1]-periods[period]) & (df['date']<=df['date'].iloc[-1])
            df2=df.loc[mask].copy()
            # Calculated daily cumilative returns for each perod using formula from here:
            # https://www.oreilly.com/library/view/learning-pandas/9781787123137/3105cd10-4928-4219-8444-25a502b46c60.xhtml
            df2['dailyReturn{}'.format(period)] = df2['close'].pct_change()
            df2['return%{}'.format(period)] = ((1 + df2['dailyReturn{}'.format(period)]).cumprod()) * 100
            sorted_df2=df2.reindex(index=df2.groupby(level=0)[y_column+period].tail(1) \
                                            .sort_values(ascending=False) \
                                            .index \
                                            .get_level_values(0),
                                            level=0)
            figure.add_trace(
                go.Scatter(
                    name=n,
                    x = sorted_df2['date'], 
                    y = sorted_df2['return%{}'.format(period)],
                    mode = 'lines',
                    line=dict(
                        color=companies.loc[companies['name']==n,'color'].item(),
                        shape='spline'
                        ),
                    )
                )
        figure.update_layout(
            figure_layout,
            
            yaxis=dict(
                showgrid =False,
                rangemode='tozero',
                ),
            xaxis=dict(
                showgrid=False,
                ticks ='outside',
                ticklen = 10,
                )
            )
    elif option =='single':
        figure = go.Figure()
        df=dashboard_data[function].loc[company]
        periods['IPO']=df['date'].iloc[-1]-df['date'].iloc[0]
        mask=(df['date']>df['date'].iloc[-1]-periods[period]) & (df['date']<=df['date'].iloc[-1])
        df2=df.loc[mask].copy()
        df2.loc[:,'dailyReturn{}'.format(period)] = df2['close'].pct_change()
        df2.loc[:,'return%{}'.format(period)] = ((1 + df2['dailyReturn{}'.format(period)]).cumprod()) * 100
        figure.add_trace(
            go.Scatter(
                name = y_column,
                x = df2['date'], 
                y = df2['return%{}'.format(period)],
                mode = 'lines',
                fill='tozeroy',
                line=dict(
                    color=companies.loc[companies['name']==company,'color'].item(),
                    shape='spline'
                    )
                )
            )
        figure.update_layout(figure_layout, xaxis_showgrid=False,yaxis_showgrid=False,)
    return figure
def create_carddecks(option,company):
    cardcontent_dict={
        'marketCap':'Market Capitalization (HKD)',
        'priceAvg50':'Average Price (50D)',
        'priceAvg200':'Average Price (200D)',
        'volume':'Volume',
        'avgVolume':'Average Volume',
        'eps':'EPS',
        'earningsAnnouncement':'Next Earnings Announcement'
    }
    if option=='compare':
        list_of_carddecks=[]
        for column in cardcontent_dict.keys():
            deck=[]
            for c in companies['name']:
                info=dashboard_data['quote'].loc[(c,column)].item()
                if column=='marketCap':
                    deck.append(dbc.Card([
                            dbc.CardHeader(c),
                            dbc.CardBody([
                                html.H5('{:.2f}B'.format(info/1000000000))
                                            ])
                                        ],className='card text-center'))
                elif column == 'earningsAnnouncement':
                    deck.append(dbc.Card([
                            dbc.CardHeader(c),
                            dbc.CardBody([
                                html.H5('{}'.format(info.strftime('%d-%m-%Y')))
                                            ])
                                        ],className='card text-center'))
                else:
                    deck.append(dbc.Card([
                            dbc.CardHeader(c),
                            dbc.CardBody([
                                html.H5('{:,}'.format(info))
                                            ])
                                        ],className='card text-center'))
            list_of_carddecks.append(deck)
    if option == 'single':
        list_of_carddecks=[]
        list_of_cards=[]
        for column,title in cardcontent_dict.items():
            info=dashboard_data['quote'].loc[(company,column)].item()
            if column=='marketCap':
                card=dbc.Card([
                        dbc.CardHeader(title),
                        dbc.CardBody([
                            html.H5('{:.2f}B'.format(info/1000000000))
                                        ])
                                    ],className='card text-center')
            elif column == 'earningsAnnouncement':
                card = dbc.Card([
                        dbc.CardHeader(title),
                        dbc.CardBody([
                            html.H5('{}'.format(info.strftime('%d-%m-%Y')))
                                        ])
                                    ],className='card text-center')
            else:
                card = dbc.Card([
                        dbc.CardHeader(title),
                        dbc.CardBody([
                            html.H5('{:,}'.format(info))
                                        ])
                                    ],className='card text-center')
            list_of_cards.append(card)
        list_of_carddecks.append([list_of_cards[0],list_of_cards[1],list_of_cards[2]])
        list_of_carddecks.append([list_of_cards[3],list_of_cards[4],list_of_cards[5]])
        list_of_carddecks.append([list_of_cards[6]])
    return(list_of_carddecks)


company_selector = html.Div([
    dbc.RadioItems(
        id="change_company_input_stock",
        className="btn-group",
        labelClassName="btn btn-primary",
        labelCheckedClassName="active",
        options=[{"label": c, "value": c} for c in companies['name']],
        value='SJM',
        )
        ],className="radio-group",
    )
compare_mode = daq.BooleanSwitch(
    id = 'compare_switch_stock',
    on = True,
    label = 'Compare Mode',
    labelPosition = 'bottom'
    )
cumilative_selector = html.Div([
    dbc.RadioItems(
        id='cumilative_change_input',
        className="btn-group",
        labelClassName="btn btn-secondary",
        labelCheckedClassName="active",
        options=[
            {'label':'6 Month','value':'6M'},
            {'label':'YTD','value':'YTD'},
            {'label':'3 Year','value':'3Y'},
            {'label':'IPO','value':'IPO'}
        ],
        value='6M',
        )
        ],className="radio-group",
    )


@app.callback(
    Output('hide_companies_stock', 'style'),
    Input('compare_switch_stock', 'on')
    )
def hide_unhide(on):
    if on == True:
        hide = {'visibility':'hidden'}
    elif on == False:
        hide ={'visibility':'visible'}
    return hide

@app.callback(
    [
        Output("change_company_output_stock", "figure"),
        Output('change_company_output_cards1','children'),
        Output('change_company_output_cards2','children'),
        Output('change_company_output_cards3','children'),
    ],
    [   
        Input('change_company_input_stock', "value"),
    ]
)
def change_company(radio_items_value):
    stock = make_scatter_figure('single','stock','close', radio_items_value)
    list_of_carddecks=create_carddecks('single',radio_items_value)
    deck1=list_of_carddecks[0]
    deck2 = list_of_carddecks[1]
    deck3 = list_of_carddecks[2]
    return stock,deck1,deck2,deck3

@app.callback(
    
        Output('cumilative_change_output', "figure"),
    
    [   
        Input('change_company_input_stock', "value"),
        Input('cumilative_change_input', "value"),
        Input('compare_switch_stock', 'on')
    ]
)
def cumilative_type(company,period,on):
    if on== True:
        figure=make_cumilative_figure('compare', 'stock', 'return%', None, period)
    elif on ==False:
        figure=make_cumilative_figure('single', 'stock', 'return%', company, period)
    return figure

@app.callback(
    [Output('compare_layout_stock', 'children')],
    [Input('compare_switch_stock', 'on'),]
    )
def update_layout(on):
    if on == True:
        list_of_carddecks=create_carddecks('compare',None)
        output_layout = [(
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([
                            dbc.CardDeck(create_indicators())]))),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dcc.Graph(figure=make_scatter_figure('compare','stock','close', None))]))),
            dbc.Row(
                dbc.Col(
                    html.H3('Daily Cumilative Growth'))),
            dbc.Row(
                dbc.Col(
                    html.Div(cumilative_selector))),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dcc.Graph(id='cumilative_change_output')]))),
            dbc.Row(
                dbc.Col(
                    html.H4('Market Capitalization (HKD)',style={'padding-bottom':'10px'}),width='auto'), justify='center'),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(list_of_carddecks[0])]))),
            dbc.Row(
                dbc.Col(
                    html.H4('Average Price (50D)',style={'padding-bottom':'10px','padding-top':'20px'}),width='auto'), justify='center'),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(list_of_carddecks[1])]))),
            dbc.Row(
                dbc.Col(
                html.H4('Average Price (200D)',style={'padding-bottom':'10px','padding-top':'20px'}),width='auto'), justify='center'),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(list_of_carddecks[2])]))),
            dbc.Row(
                dbc.Col(
                html.H4('Volume',style={'padding-bottom':'10px','padding-top':'20px'}),width='auto'), justify='center'),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(list_of_carddecks[3])]))),
            dbc.Row(
                dbc.Col(
                html.H4('Average Volume',style={'padding-bottom':'10px','padding-top':'20px'}),width='auto'), justify='center'),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(list_of_carddecks[4])]))),
            dbc.Row(
                dbc.Col(
                html.H4('EPS',style={'padding-bottom':'10px','padding-top':'20px'}),width='auto'), justify='center'),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(list_of_carddecks[5])]))),
            dbc.Row(
                dbc.Col(
                html.H4('Next Earnings Announcement',style={'padding-bottom':'10px','padding-top':'20px'}),width='auto'), justify='center'),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(list_of_carddecks[6])]))),
                    )]
    elif on == False:
        output_layout = [(
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dcc.Graph(id='change_company_output_stock')]))),
            dbc.Row(
                dbc.Col(
                    html.H3('Daily Cumilative Growth'))),
            dbc.Row(
                dbc.Col(
                    html.Div(cumilative_selector))),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dcc.Graph(id='cumilative_change_output')]))),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(id='change_company_output_cards1',style={'padding-bottom':'10px'})]))),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(id='change_company_output_cards2',style={'padding-bottom':'10px'})]))),
            dbc.Row(
                dbc.Col(
                    dbc.Spinner([dbc.CardDeck(id='change_company_output_cards3',style={'padding-bottom':'10px'})]))),
                    )]
    return output_layout

stocklayout= html.Div(
    [
        dbc.Row([
            dbc.Col(id='hide_companies_stock',children=company_selector),
            dbc.Col(
                html.Div(compare_mode,style={'float':'right'}))],justify='between'),
        html.Div(id='compare_layout_stock')])
