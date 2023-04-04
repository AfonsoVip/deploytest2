import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


######################################################Data##############################################################

df_1 = pd.read_excel("C:/Users/Afonso/PycharmProjects/pythonProject2/champions_league_dashy/data/datafinalchampions.xlsx")
df_2 = pd.read_csv("C:/Users/Afonso/PycharmProjects/pythonProject2/champions_league_dashy/data/PlayerGoalTotals.csv")
df_3 = pd.read_csv("C:/Users/Afonso/PycharmProjects/pythonProject2/champions_league_dashy/data/PlayerAppearTotals.csv")
df_4 = pd.merge(df_2, df_3, on='Player')
df_5 = pd.read_csv("C:/Users/Afonso/PycharmProjects/pythonProject2/champions_league_dashy/data/AllTimeRankingByClubDef.csv")
df_6 = df_5.groupby(['Country', 'Club'])['Win'].sum().reset_index()
df_7 = pd.read_excel('C:/Users/Afonso/PycharmProjects/pythonProject2/champions_league_dashy/data/concat.xlsx')
df_8 = pd.read_csv('C:/Users/Afonso/PycharmProjects/pythonProject2/champions_league_dashy/data/CoachesAppearTotals.csv')
df_9 = pd.read_csv('C:/Users/Afonso/PycharmProjects/pythonProject2/champions_league_dashy/data/CoachesAppearDetails.csv')

seasons = df_1['SEASON'].to_list()
players = df_7["Player"].to_list()
coaches = df_8['Coach']
coaches1= df_9['Coach'].unique()

seasons_options = [dict(label=Season, value=Season) for Season in seasons]
player_options = [dict(label=Player, value=Player) for Player in players]
seasons_info = {str(row['SEASON']): {'country': row['COUNTRY'], 'city': row['CITY'], 'referee': row['REFEREE']} for index, row in df_1.iterrows()}
coaches_options = [dict(label=Coach, value=Coach) for Coach in coaches]
coaches_options1 = [dict(label=Coach, value=Coach) for Coach in coaches1]
# Essential Functions For the pie chart visualization
def update_sunburst_chart(hover_data, click_data):
    if click_data:
        # User clicked on a segment in the sunburst chart
        country = click_data['points'][0]['label']
        club = click_data['points'][0]['parent']
        df_filtered = df_6[(df_6['Country'] == country) & (df_6['Club'] == club)]
        fig = px.sunburst(df_filtered, path=['Country', 'Club'], values='Win')
        fig.update_traces(visible=True)
    elif hover_data:
        # User is hovering over a segment in the sunburst chart
        country = hover_data['points'][0]['label']
        df_filtered = df_6[df_6['Country'] == country]
        fig = px.sunburst(df_filtered, path=['Country', 'Club'], values='Win')
    else:
        # Initial figure with all data
        fig = px.sunburst(df_6, path=['Country', 'Club'], values='Win')

    fig.update_layout(
        title='Team Wins by Country and Club',
        height=600,
        width=600,
        margin=dict(t=50, b=0, l=0, r=0),
    )

    return fig


fig = px.sunburst(df_6, path=['Country', 'Club'], values='Win')
country_list = df_6['Country'].unique()
##################################################APP###################################################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Starting the server
server = app.server

tab_loc_play = html.Div([
    ### choose circuit main information
    html.Div([
        html.Div([
            html.H2('Choose a Season:', style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='season_dropdown',
                options=seasons_options,
                value='1992-1993'
            ),
            html.Br(),
            dcc.Graph(
                id='world_map_champions'),
            html.Br(),
            html.H3(id='check_update', style={'font-weight': 'bold', 'margin-down': '0%'})],
            className='box',
            style={'margin-top': '3%'})
    ], style={'margin-left': '3%'}),
    html.Br(),
    html.Br(),
    ### first part of the page
    html.Div([
        html.Div([
            html.Div([
                html.H4('Country', style={'font-weight': 'bold'}),
                html.H3(id='country')
            ]),
            html.Div([
                html.H4('City', style={'font-weight': 'bold'}),
                html.H3(id='city')
            ]),
            html.Div([
                html.H4('Year', style={'font-weight': 'bold'}),
                html.H3(id='year')
            ]),
            html.Div([
                html.H4('Referee', style={'font-weight': 'bold'}),
                html.H3(id='referee')
            ]),
        ], style={'width': '50%','display': 'flex', 'flex-direction': 'column', 'margin-right': '20px','justify-content': 'center'}),
        html.Div([
            html.H2('Teams', style={'text-align': 'center'}),
            html.Br(),
            html.Div(id='team-scores')
        ], className='box_circ_info', style={'width': '50%'}),
    ], className='box_circ_info', style={'display': 'flex'}),
    ### Winning teams by country.
    html.Div([
        html.Div(children=[
            html.H2(children='Soccer Team Wins'),
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(id='winning_by_team', figure=fig)
                ], style={'width': '70%', 'display': 'inline-block'})
             ])
         ], className='box', style={'margin-top': '3%', 'margin-bottom': '10px',
                                      'margin-left': '3%',
                                      'box-shadow': '0px 0px 0px'})
    ], className='box', style={'margin-top': '3%',
                                'margin-left': '3%',
                                'display': 'table-cell',
                                'width': '70%', 'box-shadow': '0px 0px 0px'}),
    #### head to head
    html.Div([
        html.H2('Head to Head', style={'font-weight': 'bold'}),
        html.Label('Analyse Players '),
        dcc.Dropdown(
            id='players_names',
            options=[{'label': p, 'value': p} for p in df_7['Player']],
            value=['Lionel Messi'],
            multi=True,
            style={'color': 'black', 'background-color': '#d3d3d3'}
        ),
    ], className='box', style={'margin-top': '3%', 'margin-left': '3%'}),

    html.Div([
            html.Div([
                html.Br(),
                html.Br(),
                html.H2('Points and Appearances Comparison'),
                html.Br(),
                dcc.Graph(id='scatter_chart')
            ], className='box', style={'margin-top': '3%',
                                        'margin-left': '3%',
                                        'display': 'table-cell',
                                        'width': '65%',
                                        'box-shadow': '0px 0px 0px'}),
        ], className='box', style={'margin-top': '3%',
                                    'margin-left': '3%',
                                    'display': 'table', })
    ], className='main')



tab_coaches = html.Div([
    html.Div([
            html.Div([
                html.H2('Choose Coaches:', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='coaches',
                    options=coaches_options,
                    value='Sir Alex Ferguson',
                    multi=True
                ),
                dcc.Graph(id='histogram_ramp_comparison'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.H2('Champions League Appearances per Club',style={'font-weight':'bold'}),
                dcc.Dropdown(
                    id='coaches',
                    options=coaches_options1,
                    value='Sir Alex Ferguson',
                ),
                dcc.Graph(
                    id='pie_chart_coach')],
                className='box',
                style={'margin-top': '3%'})
        ], style={'margin-left': '3%'},className='main')]

)


app.layout = dbc.Container([
    html.Div([
        html.Img(src=app.get_asset_url('champions.jpg'), style={'width': '100%', 'margin-top': '3%'}),


        html.Br(),
        html.Br(),
        html.Br(),
        html.Label(
            'A Dashboard with insightfull information about every Champions League Edition from 1992-2022.',
            style={'color': '#e1e2df'}),
        html.H3('Dashboard by: Marta Antunes, Pedro Peças and Tiago Figueiredo.',
                style={'color': '#e1e2df', 'position': 'absolute', 'bottom': '0', 'left': '0'})
    ], className='side_bar'),

    html.Div([
        dbc.Tabs([
            dbc.Tab(tab_loc_play, label="Locations+Players", labelClassName='labels', tabClassName='tabs'),
            dbc.Tab(tab_coaches,label='Coaches',labelClassName='labels',tabClassName='tabs')
        ])
    ], className='boxtabs', style={'margin-top': '3%', 'margin-left': '15%'}),
],
    fluid=True,
)

# 1st Callback
@app.callback(
    dash.dependencies.Output('world_map_champions', 'figure'),
    [dash.dependencies.Input('season_dropdown', 'value')]
)

def update_map(season):
    # Filter the data based on the selected season
    filtered_df = df_1[df_1["SEASON"] == season]

    # Create the map using Plotly Express
    fig = px.scatter_mapbox(
        filtered_df,
        lat="LATITUDE",
        lon="LONGITUDE",
        hover_name="STADIUM",
        zoom=10,
        height=500,
    )

    # Customize the appearance of the markers
    fig.update_traces(
        marker=dict(size=10, color="#ff6f69", opacity=0.8),
        selector=dict(mode='markers')
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":0,"l":0,"b":0},
        hovermode='closest',
        font=dict(family="Open Sans", size=12, color="#636363"),
        paper_bgcolor="#f7f7f9",
        plot_bgcolor="#f7f7f9",
        geo=dict(bgcolor="#ffffff", showcoastlines=False, showland=True, landcolor="#f4f4f4", lakecolor="#ffffff", oceancolor="#ffffff", projection_type="equirectangular"),
    )

    return fig


# 2nd callback

@app.callback(
    [Output(component_id='country', component_property='children'),
     Output(component_id='city', component_property='children'),
     Output(component_id='year', component_property='children'),
     Output(component_id='referee', component_property='children')],
     [Input(component_id="season_dropdown", component_property='value')]
)
def update_final_info(season):
    info = seasons_info.get(season, {})
    country = info.get('country')
    city = info.get('city')
    referee = info.get('referee')

    # Return the updated information for each div
    return f'Country: {country}', f'City: {city}', f'Season: {season}', f'Referee: {referee}'

# 3rd callback

@app.callback(Output('winning_by_team', 'figure'),
              [Input('winning_by_team', 'clickData')],
              [State('winning_by_team', 'figure')])
def update_pie_chart(clickData, n_clicks, figure=None):
    if clickData:
        selected_country = clickData['points'][0]['parent']
        selected_club = clickData['points'][0]['label']
        df_filtered = df_6[df_6['Club'] == selected_club]
        fig = px.sunburst(df_filtered, path=['Country', 'Club'], values='Win')
        fig.update_layout(title=f'{selected_club} Wins in {selected_country}', height=600, width=600)
        return fig
    elif n_clicks:
        fig = px.sunburst(df_6, path=['Country', 'Club'], values='Win')
        fig.update_layout(title='Team Wins by Country', height=600, width=600)
        return fig
    else:
        return figure


#4rth Callback

@app.callback(
    Output('team-scores', 'children'),
    Input('season_dropdown', 'value')
)

def update_team_scores(season):
    df = pd.DataFrame(df_1)
    season_data = df.query('SEASON == @season')
    teams = []
    for i in range(len(season_data)):
        winner = season_data.iloc[i]['WINNER']
        loser = season_data.iloc[i]['LOSER']
        score = season_data.iloc[i]['SCORE']
        team = html.Div([
            html.H3('{}-{}'.format(winner, loser), style={'color': 'white'}),
            html.H4(score, style={'font-size': '24px', 'color': 'green'})
        ])
        teams.append(team)
    return teams

#5th callback

@app.callback(
    Output('scatter_chart', 'figure'),
    Input('players_names', 'value')
)

def update_scatter_plot(selected_players):
    # Filter the DataFrame by the selected players
    filtered_df = df_7[df_7['Player'].isin(selected_players)]

    # Create a trace for each player with their goals and appearances
    data = []
    for player in filtered_df['Player'].unique():
        player_data = filtered_df[filtered_df['Player'] == player]
        trace = go.Scatter(
            x=player_data['Goals'],
            y=player_data['Appearances'],
            mode='markers',
            name=player,
            marker=dict(
                size=10,
                line=dict(width=1),
                opacity=0.8
            )
        )
        data.append(trace)

    # Define the layout of the scatter plot
    layout = go.Layout(
        title='Goals vs Appearances for Selected Players',
        xaxis=dict(title='Goals'),
        yaxis=dict(title='Appearances'),
        hovermode='closest'
    )

    # Create the scatter plot figure
    fig = go.Figure(data=data, layout=layout)

    return fig


# 6th callback
@app.callback(
    dash.dependencies.Output('histogram_ramp_comparison', 'figure'),
    [dash.dependencies.Input('coaches', 'value')]
)
def update_histogram(selected_coaches):
    traces = []
    for coach in selected_coaches:
        filtered_df = df_8[df_8["Coach"] == coach]
        trace = go.Bar(
            x=filtered_df["Appearance"].value_counts().values,
            y=filtered_df["Appearance"].value_counts().index,
            name=coach,
            marker=dict(line=dict(width=1, color='white')),
            opacity=0.8
        )
        traces.append(trace)

    return {
        "data": traces,
        "layout": {
            "title": "Bar Chart for Total Career Appearances",
            "barmode": "group",
            "bargap": 0.5
        }
    }

#7th callback

@app.callback(
    Output('pie_chart_coach', 'figure'),
    [Input('coaches', 'value')]
)

def update_pie_chart(selected_coach):
    filtered_df = df_9[df_9['Coach'] == selected_coach]
    fig = px.pie(
        filtered_df,
        values='Appearance',
        names='Club',
        title=f"Champions League Appearances per Club for {selected_coach}",
        hole=0.5,
        labels={'Club': 'Club Name', 'Appearance': 'Appearances'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1))
    )
    fig.update_layout(
        title={
            'font': {'size': 24, 'family': 'Arial'},
            'x': 0.5,
            'y': 0.9
        },
        font=dict(size=14),
        legend=dict(title='Club'),
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#f9f9f9',
        margin=dict(l=50, r=50, b=50, t=100, pad=4)
    )
    return fig







if __name__ == '__main__':
    app.run_server(debug=True)


