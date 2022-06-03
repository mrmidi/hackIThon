# from dash_co import Dash, html, dcc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from django.contrib.staticfiles.storage import staticfiles_storage
from datetime import date
from dash.dependencies import Input, Output

app = DjangoDash('activity', external_stylesheets=[dbc.themes.BOOTSTRAP])



dfmy = pd.read_csv('static/data/activity-minutes-1.csv')  # open csv file
dfmy.loc[:, 'date'] = pd.to_datetime(dfmy['date'].astype(str) + ' ' + dfmy['time'].astype(str))  # join date & time
dfmy = dfmy.drop('time', 1)  # delete time column
print(dfmy.head(3))
print(dfmy.info())
mycols = [{"name": i, "id": i} for i in dfmy.columns]

print(f"columns: {mycols}")
tbl = dt.DataTable(
    data=dfmy.to_dict('records'),
    columns=mycols
)
print(type(dfmy['date']))
#s = date.fromtimestamp(dfmy['date'].iloc[0])
#e = date.fromtimestamp(dfmy['date'].iloc[-1])
#print(f"start: {s} end {e}")

# start_date =
# end_date =

date_filter = dbc.FormGroup([
    dbc.Label('Period', html_for="date-filter"),
    dcc.DatePickerRange(
        id='date-filter',
        min_date_allowed=date(2019, 10, 7),
        max_date_allowed=date(2021, 3, 1),
        initial_visible_month=date(2019, 10, 7),
        end_date=date(2019, 10, 14)
    ),
])



# from datetime import date
# from dash import Dash, dcc, html
# from dash.dependencies import Input, Output

app.layout = html.Div([
    date_filter,
    html.Div(id='output-container-date-picker-range'),
    html.Div(
        tbl
    )
])



@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix



