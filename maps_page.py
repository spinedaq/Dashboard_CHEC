import gc
import json
from app import app
import dash
from dash import callback_context, exceptions
from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from ui_components.ui_maps import create_layout
from utils.maps_functions import select_data, load_data, map_folium

with open("./options/cond_env.json", "r", encoding='utf-8') as file:
    options_cond_env = json.load(file)

# Layout de la aplicación
layout = create_layout()

total_data = load_data()  # type: ignore

click_count = 0
div_content = None
data_frame = None
day = None
map_frame = None
condition = None

options_dates =  sorted(total_data[0].FECHA.unique())
options_dates = [date.strftime('%Y-%m') for date in options_dates]

options_municipios = sorted(total_data[0].MUN.unique())

layout.children[1]['date-container'].children = dcc.Dropdown(
                id='select-date',
                options=options_dates,
                value=options_dates[0],  # Select the first option as default
                style={'position': 'relative',
                       'width': '100%',
                       'zIndex': 1000,
                       'border': 'none',
                       'color': '#00782b',
                       'font-family': 'DM Sans !important' ,
                       'font-size': '20px'},
                )

layout.children[1]['municipio-container'].children = dcc.Dropdown(
                id='select-municipios',
                options=options_municipios,
                value=options_municipios[0],  # Select the first option as default
                style={'position': 'relative',
                       'width': '100%',
                       'zIndex': 1000,
                       'border': 'none',
                       'color': '#00782b',
                       'font-family': 'DM Sans !important' ,
                       'font-size': '20px'},
                )

layout.children[1]['cond-env-container'].children = dcc.Dropdown(
                id='select-env-condition',
                options=options_cond_env,
                value=options_cond_env[0]['value'],  # Select the first option as default
                style={'position': 'relative',
                       'width': '100%',
                       'zIndex': 1000,
                       'border': 'none',
                       'color': '#00782b',
                       'font-family': 'DM Sans !important' ,
                       'font-size': '20px'},
                )

# First callback to create the map and slider
@app.callback(
    Output('map-container', 'children'),
    [Input('select-date', 'value'), Input('select-municipios', 'value'), Input("select-env-condition","value"), Input("confirm-button", "n_clicks")],
    State('map-container', 'children')
)
def initialize_map(selected_date, selected_municipios, selected_env_condition, n_clicks, current_map_content):
    global click_count, data_frame, day, condition
    condition = selected_env_condition
    if n_clicks > click_count:
        click_count = n_clicks
        data_frame = select_data(
            int(selected_date[:4]), int(selected_date[5:7]), selected_municipios,
            total_data[0], total_data[1], total_data[2], total_data[3], total_data[4], total_data[5], total_data[6], total_data[7], total_data[8]
        )
        folium_map = map_folium(
            data_frame[0], data_frame[1], data_frame[2], data_frame[3],
            data_frame[4][0], data_frame[5][0], data_frame[6][0], data_frame[7][0], data_frame[8][0],condition
        )

        # Create the map and slider
        map_frame = html.Iframe(
            srcDoc=folium_map,
            style={
                'width': '100%%', 'overflow': 'hidden', 'border': 'none',
                '-ms-overflow-style': 'none', 'scrollbar-width': 'none', 'height': '100%',
                'position': 'relative', 'scrollbar-height': 'none !important', 'margin-bottom': '1%',
                'object-fit': 'cover', 'overflow-y': 'hidden', 'max-height': '59vh'
            },
            id='folium_map_frame',
            width='100%', height='100%',
        )
        div_content = html.Div([
            dcc.Slider(
                id='date-slider',
                min=1, max=31, step=1, value=1,  # Initialized to the first day
                tooltip={'always_visible': True, 'placement': 'top'}
            ),
            map_frame
        ], style={
            'display': 'flex', 'flexDirection': 'column',
            'height': '100%', 'gap': '10px', 'overflow': 'hidden'})
        return div_content
    return dash.no_update

# Second callback to update the map when the slider changes
@app.callback(
    Output('folium_map_frame', 'srcDoc'),
    [Input('date-slider', 'value')]
)
def update_map_by_day(slider_date_value):
    global day, data_frame, condition
    if slider_date_value != day:
        day = slider_date_value
        print(f'Value:{day}')
        folium_map = map_folium(
            data_frame[0], data_frame[1], data_frame[2], data_frame[3],
            data_frame[4][day-1], data_frame[5][day-1], data_frame[6][day-1], data_frame[7][day-1], data_frame[8][day-1],condition
        )
        # Return the generated HTML for the new map as `srcDoc` of the `Iframe`
        return folium_map
    return dash.no_update

@app.callback(
    Output('url-maps', 'pathname'),
    [Input('button-chat', 'n_clicks'),
     Input('button-graphs', 'n_clicks')]
)
def redirect_to_pages(n_clicks_chat, n_clicks_graphs):
    # Obtener el contexto del trigger
    ctx = callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate

    # Identificar qué botón disparó el callback
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'button-chat' and n_clicks_chat:
        return "/chat_page"
    elif triggered_id == 'button-graphs' and n_clicks_graphs:
        return "/graphs_page"

    raise exceptions.PreventUpdate