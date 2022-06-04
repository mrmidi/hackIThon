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
import sqlite3
import pdfkit

app = DjangoDash('activity', external_stylesheets=[dbc.themes.BOOTSTRAP])

def get_steps_by_day(df, dfs):
    users_count = df.user.nunique()
    df = df.resample('D', on='datetime').sum()
    dfs = dfs.resample('D', on='datetime').sum()
    df.reset_index(inplace=True)
    dfs.reset_index(inplace=True)
    dfs.rename(columns={'steps': 'steps_s'}, inplace=True)
    df['steps'] = df['steps'].div(users_count)
    dfs['steps_s'] = dfs['steps_s'].div(users_count)
    df['datetime'] = df['datetime'].dt.day_name()
    fig = px.bar(df, x='datetime', y='steps', title='Steps by Day', barmode='group')
    fig.add_bar(x=df['datetime'], y=dfs['steps_s'], name='Days at School')
    return fig


db = sqlite3.connect('static/data/Gadgetbridge')  # make sqlite connection
df_complete = pd.read_sql("SELECT * FROM MI_BAND_ACTIVITY_SAMPLE", db)  # put sql data to pandas dataframe

df_complete = df_complete.rename(lambda x: x.lower(), axis=1)  #rename column names to lowercase
df_complete['timestamp'] = pd.to_datetime(df_complete['timestamp'], unit='s')  #convert timestamp to datetime object

complete_users_count = df_complete.user_id.nunique()  # count unique users
df_complete = df_complete.resample('W', on='timestamp').sum() / complete_users_count
# print(df_complete.head())
df_complete.reset_index(inplace=True)
fig_month = px.bar(df_complete, x=df_complete['timestamp'].astype(str), y='steps', title='Steps by Weeks')

df = pd.read_csv('static/data/data_home.csv', parse_dates=['datetime'])  # read csv for day analysis
dfs = pd.read_csv('static/data/data_school.csv', parse_dates=['datetime'])
users = df.user.unique()

# graph weekly totals by users

info_df = pd.read_csv('static/data/info.csv')

home_df = pd.read_csv('static/data/data_home.csv', parse_dates=['datetime'])

school_df = pd.read_csv('static/data/data_school.csv', parse_dates=['datetime'])

sched_df = pd.read_csv('static/data/schedule.csv')
sched_df['zacatek'] = pd.to_datetime(sched_df['from'], format='%H:%M')
sched_df['konec'] = pd.to_datetime(sched_df['to'], format='%H:%M')
del sched_df['from'], sched_df['to']

school_df['weekday'] = school_df['datetime'].dt.day_name()
#school_df.info()

school_df['time'] = pd.to_datetime(pd.to_datetime(school_df['datetime']).dt.strftime("%H:%M"),format="%H:%M")

df_merge = school_df.merge(sched_df, how = 'cross')
df_merge = df_merge.query('time >= zacatek and time <= konec')
df_merge.info()
df_all=df_merge.merge(school_df,how='outer')
df_all.day[df_all.day.isnull()]=df_all.weekday[df_all.day.isnull()]

hod20 = pd.to_datetime("22:00",format="%H:%M")
po20hod = df_all[df_all['time']>hod20]

df_all['subject'][df_all.subject.isnull()] = "out of school"
df_vse = df_all[df_all.weekday == df_all.day]

df_user = df_vse[['steps', 'user']].groupby('user').sum()
df_user.reset_index(inplace=True)

df_user_home = home_df[['steps', 'user']].groupby('user').sum()
df_user_home.reset_index(inplace=True)

fig_weekly = px.bar(x = df_user_home['user'].astype(str), y=df_user_home['steps'], barmode='group', title="Total steps by user")
fig_weekly.add_bar(x = df_user['user'].astype(str), y=df_user['steps'], name='School week')


app.layout = html.Div([
    html.Div(id='dd-output-container'),
    dcc.Dropdown(
        id="users-dropdown",
        placeholder='All Users',
        value=None,
        options=[{'label': f'User #{user}', 'value': user} for user in users]),
    dcc.Graph(
         id='dd-output-graph'
    ),
    dcc.Graph(
        id='week-graph',
        figure=fig_weekly,
    ),
    dcc.Graph(
        id='month-graph',
        figure=fig_month,
    )
])




@app.callback(
    #Output('dd-output-container', 'children'),
    Output('dd-output-graph', 'figure'),
    Input('users-dropdown', 'value')
)
def update_steps_by_day(value):
    return get_steps_by_day(filter_data(value, df), filter_data(value, dfs))




def filter_data(user, df):
    filtered_df = df.copy()
    if user is not None:
        filtered_df = filtered_df[filtered_df['user'] == user]

    return filtered_df
