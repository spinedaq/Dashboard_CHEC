from dash import Dash

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@700&display=swap',
        'https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap'])

server = app.server