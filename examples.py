
#link zoom and pan to another figure
""" app=dash.Dash()

app.layout = html.Div([
                dcc.Graph(id='graph',figure=fig),
                html.Pre(id='relayout-data', style=styles['pre']),
                dcc.Graph(id='graph2', figure=fig)])

# Just to see what values are captured.
@app.callback(Output('relayout-data', 'children'),
              [Input('graph', 'relayoutData')])
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


@app.callback(Output('graph2', 'figure'),
             [Input('graph', 'relayoutData')], 
             [State('graph2', 'figure')])
def graph_event(select_data,  fig):
    try:
       fig['layout'] = {'xaxis':{'range':[select_data['xaxis.range[0]'],select_data['xaxis.range[1]']]}}
    except KeyError:
       fig['layout'] = {'xaxis':{'range':[zoomed out value]}}
return fig

app.run_server() """


""" fig= go.Figure()
#fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(name='Dividends', x=AAPL[5]['date'], y= AAPL[5]['adjDividend'], xperiod='M1',xperiodalignment='middle'))
#,secondary_y=False
#fig.add_trace(go.Scatter(x = AAPL[1]['date'], y =AAPL[1]['dividendYield'],
#                  mode = 'lines+markers',
#                  line_shape= 'spline',
#                  name='Dividend Yield', 
#                  xperiod='M1',
#                  xperiodalignment='middle'),secondary_y=True)
#.dt.strftime('%m-%Y')

fig.show() """

