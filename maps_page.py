import gc
import json
from app import app
import dash
from dash import callback_context, exceptions
from dash import Dash, html, dcc, Output, Input, State, ctx
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
                'position': 'relative', 'scrollbar-height': 'none !important', 'margin-bottom': '1vh',
                'object-fit': 'cover', 'overflow-y': 'hidden', 'max-height': '59vh'
            },
            id='folium_map_frame',
            width='100%', height='100%',
        )
        div_content = html.Div([
            html.Div(style={
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'center'},
                children=[
                    dbc.Button(
                            html.I(className="bi bi-arrow-left"),  # Flecha hacia la izquierda
                            id="decrease-btn", color="primary", outline=True, style={
                                'width': '5vh', 
                                'position': 'relative', 
                                'height': '5vh', 
                                'margin': '0 1% 0 0', 
                                'left':'1%',
                                'backgroundImage': "url('/assets/images/left-arrow-direction-svgrepo-com.svg')",
                                'backgroundSize': 'cover',
                                'backgroundPosition': 'center',
                                'backgroundRepeat': 'no-repeat',
                                'border': 'none',
                                'backgroundColor': 'transparent',
                                'cursor': 'pointer'}
                        ),
                    html.Div(style={'width': '102%'}, children=[
                    dcc.Slider(
                        id='date-slider',
                        min=1, max=31, step=1, value=1,
                        tooltip={'always_visible': True, 'placement': 'top'}
                    )]),
                    dbc.Button(
                        html.I(className="bi bi-arrow-right"),  # Flecha hacia la derecha
                        id="increase-btn", color="primary", outline=True, style={
                                'width': '5vh', 
                                'position': 'relative', 
                                'height': '5vh', 
                                'margin': '0 0 0 1%', 
                                'right':'1%',
                                'backgroundImage': "url('/assets/images/left-arrow-direction-svgrepo-com.svg')",
                                'backgroundSize': 'cover',
                                'backgroundPosition': 'center',
                                'backgroundRepeat': 'no-repeat',
                                'transform': 'rotate(180deg)',
                                'border': 'none',
                                'backgroundColor': 'transparent',
                                'cursor': 'pointer'}
                        ),
                ]),
                
            map_frame
            ], style={
                'display': 'flex', 'flexDirection': 'column',
                'height': '100%', 'gap': '10px', 'overflow': 'hidden'})
        return div_content
    return dash.no_update

# Second callback to update the map when the slider changes
@app.callback(
    [Output('date-slider', 'value'), Output('folium_map_frame', 'srcDoc')],
    [Input('decrease-btn', 'n_clicks'),
     Input('increase-btn', 'n_clicks'),
     Input('date-slider', 'value')],
    [State('date-slider', 'min'),
     State('date-slider', 'max')]
)
def update_slider_and_map(decrease_clicks, increase_clicks, slider_value, slider_min, slider_max):
    # Inicializa clics en 0 si son None
    decrease_clicks = decrease_clicks or 0
    increase_clicks = increase_clicks or 0

    # Determina cuál botón fue presionado
    triggered_id = ctx.triggered_id

    if triggered_id == "decrease-btn" and slider_value > slider_min:
        slider_value -= 1
    elif triggered_id == "increase-btn" and slider_value < slider_max:
        slider_value += 1

    # Lógica para actualizar el mapa
    global day, data_frame, condition
    if slider_value != day:
        day = slider_value
        print(f'Value:{day}')
        folium_map = map_folium(
            data_frame[0], data_frame[1], data_frame[2], data_frame[3],
            data_frame[4][day-1], data_frame[5][day-1], data_frame[6][day-1], data_frame[7][day-1], data_frame[8][day-1], condition
        )
        # Devuelve el nuevo valor del slider y el HTML del mapa
        return slider_value, folium_map

    # Si no hubo cambios en el slider, solo actualiza su valor
    return slider_value, dash.no_update

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