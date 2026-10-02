import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output




external_stylesheet = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
        'rel': 'stylesheet'
    }
]




patients = pd.read_csv('data/state_wise_daily.csv')




total = patients.shape[0]

active = patients[patients['Status'] == 'Confirmed'].shape[0]

recovered = patients[patients['Status'] == 'Recovered'].shape[0]

deaths = patients[patients['Status'] == 'Deceased'].shape[0]




options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]


options1 = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Mask', 'value': 'Mask'},
    {'label': 'Sanitizer', 'value': 'Sanitizer'},
    {'label': 'Oxygen', 'value': 'Oxygen'}
]


options2 = [
    {'label': 'Red Zone', 'value': 'Red Zone'},
    {'label': 'Blue Zone', 'value': 'Blue Zone'},
    {'label': 'Green Zone', 'value': 'Green Zone'},
    {'label': 'Orange Zone', 'value': 'Orange Zone'}
]



app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheet
)




app.layout = html.Div([

    # Main heading
    html.H1(
        "Coronavirus Pandemic",
        style={
            'color': '#fff',
            'text-align': 'center'
        }
    ),



    html.Div([

        # Total Cases
        html.Div([
            html.Div([
                html.Div([
                    html.H3(
                        "Total Cases",
                        className='text-light'
                    ),
                    html.H4(
                        total,
                        className='text-light'
                    )
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),

        # Active Cases
        html.Div([
            html.Div([
                html.Div([
                    html.H3(
                        "Active Cases",
                        className='text-light'
                    ),
                    html.H4(
                        active,
                        className='text-light'
                    )
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),

        # Recovered
        html.Div([
            html.Div([
                html.Div([
                    html.H3(
                        "Recovered Cases",
                        className='text-light'
                    ),
                    html.H4(
                        recovered,
                        className='text-light'
                    )
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-3'),

        # Deaths
        html.Div([
            html.Div([
                html.Div([
                    html.H3(
                        "Total Deaths",
                        className='text-light'
                    ),
                    html.H4(
                        deaths,
                        className='text-light'
                    )
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3')

    ], className='row'),




    html.Div([

        # Commodity graph
        html.Div([
            html.Div([
                html.Div([

                    dcc.Dropdown(
                        id='plot-graph',
                        options=options1,
                        value='All'
                    ),

                    dcc.Graph(
                        id='graph'
                    )

                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-6'),


        # Pie chart
        html.Div([
            html.Div([
                html.Div([

                    dcc.Dropdown(
                        id='my_dropdown',
                        options=options2,
                        value='Red Zone',
                        style={'width': '100%'}
                    ),

                    dcc.Graph(
                        id='the_graph'
                    )

                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-6')

    ], className='row'),




    html.Div([

        html.Div([
            html.Div([
                html.Div([

                    dcc.Dropdown(
                        id='picker',
                        options=options,
                        value='All'
                    ),

                    dcc.Graph(
                        id='bar'
                    )

                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-12')

    ], className='row')

], className='container')




@app.callback(
    Output('bar', 'figure'),
    Input('picker', 'value')
)
def update_graph(selected_type):

    if selected_type == 'All':

        return {
            'data': [
                go.Bar(
                    x=patients['State'],
                    y=patients['Total']
                )
            ],
            'layout': go.Layout(
                title='State Total Count',
                plot_bgcolor='orange'
            )
        }

    elif selected_type == 'Hospitalized':

        return {
            'data': [
                go.Bar(
                    x=patients['State'],
                    y=patients['Hospitalized']
                )
            ],
            'layout': go.Layout(
                title='State Hospitalized Count',
                plot_bgcolor='orange'
            )
        }

    elif selected_type == 'Recovered':

        return {
            'data': [
                go.Bar(
                    x=patients['State'],
                    y=patients['Recovered']
                )
            ],
            'layout': go.Layout(
                title='State Recovered Count',
                plot_bgcolor='orange'
            )
        }

    elif selected_type == 'Deceased':

        return {
            'data': [
                go.Bar(
                    x=patients['State'],
                    y=patients['Deceased']
                )
            ],
            'layout': go.Layout(
                title='State Deceased Count',
                plot_bgcolor='orange'
            )
        }




@app.callback(
    Output('graph', 'figure'),
    Input('plot-graph', 'value')
)
def generate_graph(selected_type):

    if selected_type == 'All':

        y_column = 'Total'

    elif selected_type == 'Mask':

        y_column = 'Mask'

    elif selected_type == 'Sanitizer':

        y_column = 'Sanitizer'

    elif selected_type == 'Oxygen':

        y_column = 'Oxygen'

    else:

        y_column = 'Total'


    return {
        'data': [
            go.Scatter(
                x=patients['Status'],
                y=patients[y_column],
                mode='lines'
            )
        ],
        'layout': go.Layout(
            title='Commodities Total Count',
            plot_bgcolor='pink'
        )
    }




@app.callback(
    Output('the_graph', 'figure'),
    Input('my_dropdown', 'value')
)
def generate_pie_chart(selected_zone):

    piechart = px.pie(
        data_frame=patients,
        names='Status',
        values='Total',
        hole=0.3,
        title=selected_zone
    )

    return piechart




if __name__ == '__main__':
    app.run(debug=True)
