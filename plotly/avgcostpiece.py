import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


df = pd.read_csv('ProductionData.csv')

end_date = datetime.date.today() - relativedelta(days=3)
start_of_week_date = end_date - relativedelta(days=5)
start_of_month_date = end_date - relativedelta(months=6)
date_range_week = str(start_of_week_date) + ' to ' + str(end_date)
df['prod_date'] = pd.to_datetime(df['prod_date'])

df_slice_one = df[(df['prod_date'] >= start_of_week_date) & (df['prod_date'] <= end_date)]
df_slice_two = df[(df['prod_date'] >= start_of_month_date) & (df['prod_date'] <= end_date)]
df_slice_one['last_week_avg'] = df_slice_one.groupby(['machine'])['cost_per_piece'].transform('mean')
df_slice_two['last_six_months_avg'] = df_slice_two.groupby(['machine'])['cost_per_piece'].transform('mean')

x1 = df_slice_one['machine'].unique()
y1 = df_slice_one['last_week_avg'].unique()

x2 = df_slice_two['machine'].unique()
y2 = df_slice_two['last_six_months_avg'].unique()

trace1 = go.Bar(
    x=x1,
    y=y1,
    name='Last Week\'s Cost Per Piece AVG',
    marker=dict(color='#FFD700')
)
trace2 = go.Bar(
    x=x2,
    y=y2,
    name='Last 6 Months AVG Cost Per Piece',
    marker=dict(color='#9EA0A1'),
)

data = [trace1, trace2]
layout = go.Layout(
    title='Cost Per Piece Average',

    xaxis=dict(
        title=date_range_week,
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'
        ),

        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
    ),
    yaxis=dict(
        title='COST',
        tickformat="$,.2f",
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'
        ),
        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
    )
)
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='avgcostpiece.html')
