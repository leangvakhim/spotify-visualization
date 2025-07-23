# Import
import dash
# import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
import plotly.express as px
import pandas as pd

# Loading Data
def load_data():
    spotify = pd.read_csv('spotify-2024.csv')
    spotify['Track Score'] = pd.to_numeric(spotify['Track Score'], errors='coerce') # if any error appear, it will be NaN
    spotify['Release Date'] = pd.to_datetime(spotify['Release Date'])
    spotify['YearMonth'] = spotify['Release Date'].dt.to_period("M")
    return spotify

spotify = load_data()

num_records = len(spotify)
avg_track_score = spotify['Track Score'].mean()

# Creating a Web App
# tailwind_cdn = "https://cdn.tailwindcss.com"
app = dash.Dash(__name__)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Spotify Dashboard</title>
        <link rel="icon" type="image/x-icon" href="/spotify.png">
        {%css%}
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
# print(spotify.columns)
# print(spotify['Artist'].head())
# App Layout and Design
# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col(html.H1("Spotify Dashboard"), width=15, className="text-center my-5 text-red-500")
#     ]),

#     # Spotify Statistics
#     dbc.Row([
#         dbc.Col(html.Div(f"Total Spotify Record: {num_records}", className="text-center my-3 top-text "),
#         width=7),
#         dbc.Col(html.Div(f"Average Track Score: {avg_track_score:,.2f}", className="text-center my-3 top-text"),
#         width=7)
#     ], className="mb-5"),

#     # Singer Demographics
#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     html.H4("Spotify Singer Demographics", className="card-title"),
#                     dcc.Dropdown(
#                         id="singer-filter",
#                         options=[{"label": name, "value": name} for name in spotify['Artist'].dropna().unique()],
#                         value=None,
#                         placeholder="Select Artist",
#                         style={"width": "100%", "color": "black"}
#                     ),
#                     dcc.Graph(id="singer-distribution")
#                 ])
#             ])
#         ], width=7),

#         # dbc.Col([
#         #     dbc.Card([
#         #         dbc.CardBody([
#         #             html.H4("Spotify Popularity Distribution", className="card-title"),
#         #             dcc.Slider(
#         #                 id="spotify-slider",
#         #                 min=spotify['Spotify Popularity'].min(),
#         #                 max=spotify['Spotify Popularity'].max(),
#         #                 value=spotify['Spotify Popularity'].median(),
#         #                 marks={int(value): f"{int(value):,}" for value in spotify["Spotify Popularity"]
#         #                     .quantile([0, 0.25, 0.5, 0.75, 1]).values},
#         #                 step=10
#         #             ), #slider
#         #             dcc.RadioItems(
#         #                 id='chart-type',
#         #                 options=[
#         #                     {'label': 'Line Chart', 'value': 'line'},
#         #                     {'label': 'Bar Chart', 'value': 'bar'}
#         #                 ],
#         #                 value='line',
#         #                 inline=True,
#         #                 className='mb-4'
#         #             ), #use for radio button
#         #             dcc.Graph(id="condition-distribution")
#         #         ])
#         #     ])
#         # ], width=12)
#     ])


# ], fluid=True)

app.layout = html.Div([
    html.Div([
        html.H1("Spotify Dashboard", className="text-center my-5 text-red-500 text-3xl")
    ]),

    html.Div([
        html.Div(f"Total Spotify Record: {num_records}", className="text-center my-3"),
        html.Div(f"Average Track Score: {avg_track_score:,.2f}", className="text-center my-3")
    ], className="grid grid-cols-2 gap-4 mb-5"),

    html.Div([
        html.Div([
            html.Div([
                html.H4("Spotify Singer Demographics", className="text-xl font-bold mb-2"),
                dcc.Dropdown(
                    id="singer-filter",
                    options=[{"label": name, "value": name} for name in spotify['Artist'].dropna().unique()],
                    value=None,
                    placeholder="Select Artist",
                    style={"width": "100%", "color": "black"}
                ),
                dcc.Graph(id="singer-distribution")
            ], className="p-6 shadow-lg bg-white rounded")
        ], className="col-span-1"),
    ], className="grid grid-cols-1 gap-4")
])

# Create our Callbacks
@app.callback(
    Output('singer-distribution', 'figure'),
    Input('singer-filter', 'value'),
)

def update_distribution(selected_singer):
    if selected_singer:
        filtered_df = spotify[spotify['Artist'] == selected_singer]
    else:
        filtered_df = spotify

    if filtered_df.empty:
        return {}

    fig = px.histogram(
        filtered_df,
        x='Artist',
        nbins=5,
        color="Artist",
        title="Singer Distribution by Artist",
        # color_discrete_sequence=["red", 'blue']
    )

    return fig

# @app.callback(
#     Output('condition-distribution', 'figure'),
#     [Input('chart-type', 'value'),
#     Input('spotify-slider', 'value')]
# )

# def update_condition(chart_type, slider_values):


#     return chart_type, slider_values






if __name__ == "__main__":
    app.run(debug=True)