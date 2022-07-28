from jupyter_dash import JupyterDash
import dash
from dash import dcc
from dash import html
from dash.exceptions import PreventUpdate
from dash import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None,
                     plot_bgcolor="rgba( 0, 0, 0, 0)",
                     paper_bgcolor="rgba( 0, 0, 0, 0)",)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    return fig

df = pd.read_csv('dummy_data.csv')



month_dict = {"JANUARY": 1,
              "FEBRUARY": 2,
              "MARCH": 3,
              "APRIL": 4,
              "MAY": 5,
              "JUNE": 6,
              "JULY": 7,
              "AUGUST": 8,
              "SEPTEMBER": 9,
              "OCTOBER": 10,
              "NOVEMBER": 11,
              "DECEMBER": 12}

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(
                'Circular Medical Textiles Dashboard',
                id = 'title'
            )
        ], id = 'title-area'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div(dcc.Dropdown(id = 'g1dd-a', 
                    options = list(df.columns[6:9]), 
                    multi=True, 
                    clearable = False,
                    value = list(df.columns[6:9])), className = 'hlf')
                ], className = 'dropdown-area', id = 'dd-area1'),
            html.Div([
                dcc.Graph(id = 'graph1', figure = blank_fig())
            ], id = 'g1', className = 'graph-container'),
            ], id = 'q1', className = 'container-a1'),
            

            html.Div([
                html.Div([
                    html.Div(dcc.Dropdown(id = 'g2dd-a', options = list(df.columns[1:9]), clearable = False, value = list(df.columns[1:9])[0]), className = 'thrd'),
                    html.Div(dcc.Dropdown(id = 'g2dd-b', options = list(df['Months'].unique()), multi=True, clearable = False, value = list(df['Months'].unique())), className = 'thrd'),
                    html.Div(dcc.Dropdown(id = 'g2dd-c', options = list(df['Item'].unique()), multi=True, clearable=False, value = list(df['Item'].unique())), className = 'thrd')
                ], className = 'dropdown-area', id = 'dd-area2'),
                html.Div([
                dcc.Graph(id = 'graph2', figure = blank_fig())
                ], id = 'g2', className = 'graph-container'),

            ], id = 'h2', className = 'container-a2'),
            html.Div([
                html.Div([
                    html.Div(dcc.Dropdown(
                        id = 'g3dd-a',
                        options = list(df.columns[1:9]),
                        clearable = False,
                        value = list(df.columns[1:9])[0],
                        multi = False
                    ), className = 'g3-dd'),
                    html.Div(dcc.Dropdown(
                        id = 'g3dd-b',
                        options = list(df['Item'].unique()), 
                        multi=True, 
                        clearable=False, 
                        value = list(df['Item'].unique())
                    ), className = 'g3-dd'),
                    html.Img(src = app.get_asset_url('logo.jpg'), className = 'logo')
                    
                ], className = 'v-dropdown-area'),
                html.Div([
                dcc.Graph(id = 'graph3', figure = blank_fig())
                ], id = 'g3', className = 'graph-container'),
            ], id = 'q3', className = 'container-b'),

        ], id = 'main')
    ], id = 'dashboard')
], id = 'layout')


@app.callback(
    Output('graph1', 'figure'),
    Input('g1dd-a', 'value')
)
def update_g1(variables):
    if len(variables) == 0:
        raise PreventUpdate
    dff = df[['Months', 'Carbon Savings - Kg', 'Water Savings - Litres', 'Waste Savings - Kg']]
    dff = dff.groupby('Months', as_index = False).sum()
    dff['month_numeric'] = dff['Months'].map(month_dict)
    dff = dff.sort_values('month_numeric')
    dff = dff.melt(id_vars = 'Months', value_vars=list(dff.columns[1:]))
    dff = dff[dff['variable'].isin(variables)]
    
    fig = px.line(
        dff, 
        x = 'Months', 
        y = 'value', 
        color = 'variable', 
        color_discrete_sequence = ['#e6701d', '#3566c1', '#ffc61c', '#a7a6a7'],
        title = "<b>Savings trend over time<b>",
        #add template here
        # template = 'plotly_dark'
        )
    fig.update_layout(
        title = dict(font_size = 25, x = 0.5, xanchor = 'center'),
        margin = dict(t = 55),
        #comment these 2 lines
        plot_bgcolor = 'rgba(0, 0, 0, 0)', 
        paper_bgcolor = 'rgba(0, 0, 0, 0)', 
        ####################################
        font = dict(color = 'white'), 
        legend = dict(orientation = 'h', title = '', x = 0.5, xanchor = 'center', y = -0.2))
    fig.update_xaxes(title = "<b>MONTHS<b>", showgrid = False, ticks = 'outside', ticklen = 5, tickcolor = 'rgba(0, 0, 0, 0)')
    fig.update_yaxes(title = "<b>SAVINGS<b>", gridcolor = 'grey', ticks = 'outside', ticklen = 5, tickcolor = 'rgba(0, 0, 0, 0)')
    return fig


@app.callback(
    Output('graph2', 'figure'),
    [Input('g2dd-a', 'value'),
     Input('g2dd-b', 'value'),
     Input('g2dd-c', 'value')]
)
def update_g3(variable, months, items):
    if len(months) == 0 or len('items') == 0:
        raise PreventUpdate
    df_bar = df.melt(id_vars = ['Item', 'Months'], value_vars=df.columns[1:-1])
    df_bar = df_bar[df_bar['variable'] == variable]
    df_bar = df_bar[df_bar['Months'].isin(months)]
    df_bar = df_bar[df_bar['Item'].isin(items)]
    fig = px.bar(
        df_bar, 
        x = 'value', 
        y = 'Months', 
        color = 'Item',
         barmode = 'group', 
         orientation = 'h',
         color_discrete_sequence = ['#e6701d', '#3566c1', '#ffc61c', '#a7a6a7'],
         title = f"<b>Monthly {variable} per item<b>",
         #add template here
        #  template = 'plotly_dark'
         )
    fig.update_layout(
            title = dict(font_size = 25, x = 0.5, xanchor = 'center'),
            margin = dict(t = 55, b = 10),
            # comment these 2 lines 
            plot_bgcolor = 'rgba(0, 0, 0, 0)', 
            paper_bgcolor = 'rgba(0, 0, 0, 0)', 
            ###################################
            font = dict(color = 'white'), 
            legend = dict(orientation = 'h', title = '', x = 0.5, xanchor = 'center', y = -0.099))
    fig.update_xaxes(title = "<b>PROCESSING EFFICIENCY PER ITEM<b>", showgrid = True, gridcolor = 'grey', ticks = 'outside', ticklen = 5, tickcolor = 'rgba(0, 0, 0, 0)')
    fig.update_yaxes(title = "<b>MONTHS<b>", gridcolor = 'grey', showgrid = False, ticks = 'outside', ticklen = 5, tickcolor = 'rgba(0, 0, 0, 0)')
    return fig



@app.callback(
    Output('graph3', 'figure'),
    [Input('g3dd-a', 'value'),
     Input('g3dd-b', 'value')]
)
def update_g3(variable, items):
    if len(items) == 0:
        raise PreventUpdate
    df_donut = df.groupby('Item', as_index = False).sum()
    df_donut = df_donut[df_donut['Item'].isin(items)]
    fig = px.pie(
        df_donut, 
        names= 'Item', 
        values = variable, 
        hole = 0.5, 
        color_discrete_sequence = ['#e6701d', '#3566c1', '#ffc61c', '#a7a6a7'],
        title = "<b>Sum of Carbon Savings / item<b>",
        # add template here 
        # template = 'plotly_dark'
        )

    fig.update_layout(
            title = dict(font_size = 25, x = 0.5, xanchor = 'center'),
            margin = dict(t = 55, b = 30),
            # comment these 2 lines 
            plot_bgcolor = 'rgba(0, 0, 0, 0)', 
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            ###################################
            font = dict(color = 'white'), 
            legend = dict(orientation = 'h', title = '', x = 0.5, xanchor = 'center', y = -0.1))
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

if __name__ == "__main__":
    app.run_server(debug = False)