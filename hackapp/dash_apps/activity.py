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

def get_steps_by_day(df):
    users_count = df.user.nunique()
    df = df.resample('D', on='datetime').sum()
    df.reset_index(inplace=True)
    #df = df.resample('D', on='datetime')
    df['steps'] = df['steps'].div(users_count)
    df['datetime'] = df['datetime'].dt.day_name()
    #df.index = pd.to_datetime(df.index)
    #df['d'] = df['datetime']
    print(df.info())
    print(df)
    print(type(df))
    fig = px.bar(df, x='datetime', y='steps', title='Steps by Day')
    return fig


df = pd.read_csv('static/data/data_home.csv', parse_dates=['datetime'])
dfs = pd.read_csv('static/data/data-_school.csv', parse_dates=['datetime'])
users = df.user.unique()

# users = df_h.user.unique()
# users_count = df_h.user.nunique()
# print(users)
# print(type(users))
# print(df_h)
# print(df_h.info())
# df_h = df_h.resample('D', on='datetime').sum()
# df_h['steps'] = df_h['steps'].div(users_count)
# print(df_h)

#print(df.head(5))

# dfmy = pd.read_csv('static/data/activity-minutes-1.csv')  # open csv file
# dfmy.loc[:, 'date'] = pd.to_datetime(dfmy['date'].astype(str) + ' ' + dfmy['time'].astype(str))  # join date & time
# dfmy = dfmy.drop('time', 1)  # delete time column
# print(dfmy.head(3))
# print(dfmy.info())
# mycols = [{"name": i, "id": i} for i in dfmy.columns]

# print(f"columns: {mycols}")
# tbl = dt.DataTable(
#     data=dfmy.to_dict('records'),
#     columns=mycols
# )
# print(type(dfmy['date']))
#s = date.fromtimestamp(dfmy['date'].iloc[0])
#e = date.fromtimestamp(dfmy['date'].iloc[-1])
#print(f"start: {s} end {e}")

# start_date =
# end_date =

# date_filter = dbc.FormGroup([
#     dbc.Label('Period', html_for="date-filter"),
#     dcc.DatePickerRange(
#         id='date-filter',
#         min_date_allowed=date(2019, 10, 7),
#         max_date_allowed=date(2021, 3, 1),
#         initial_visible_month=date(2019, 10, 7),
#         end_date=date(2019, 10, 14)
#     ),
# ])



# from datetime import date
# from dash import Dash, dcc, html
# from dash.dependencies import Input, Output

app.layout = html.Div([
    html.Div(id='dd-output-container'),
    dcc.Dropdown(
        id="users-dropdown",
        placeholder='All Users',
        value=None,
        options=[{'label': f'User #{user}', 'value': user} for user in users]),
    dcc.Graph(
         id='dd-output-graph'
    )
])

#
#
# @app.callback(
#     Output('output-container-date-picker-range', 'children'),
#     Input('date-filter', 'start_date'),
#     Input('date-filter', 'end_date'))
# def update_output(start_date, end_date):
#     string_prefix = 'You have selected: '
#     if start_date is not None:
#         start_date_object = date.fromisoformat(start_date)
#         start_date_string = start_date_object.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
#     if end_date is not None:
#         end_date_object = date.fromisoformat(end_date)
#         end_date_string = end_date_object.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'End Date: ' + end_date_string
#     if len(string_prefix) == len('You have selected: '):
#         return 'Select a date to see it displayed here'
#     else:
#         return string_prefix



@app.callback(
    #Output('dd-output-container', 'children'),
    Output('dd-output-graph', 'figure'),
    Input('users-dropdown', 'value')
)
def update_steps_by_day(value):
    return get_steps_by_day(filter_data(value, df))




def filter_data(user, df):
    filtered_df = df.copy()
    if user is not None:
        filtered_df = filtered_df[filtered_df['user'] == user]

    return filtered_df
