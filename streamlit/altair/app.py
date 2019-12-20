import streamlit as st
import altair as alt
from vega_datasets import data as  vdata

import pandas as pd
import numpy as np 

alt.themes.enable('default')
alt.data_transformers.enable('json')


# Scatterplot and time series
# ---- 
st.header("Exploring interactive visualizations")
st.subheader("Multiple point selection")

np.random.seed(0)
n_objects = 20
n_times = 50

# (x, y) pair of metadata per object
locations = pd.DataFrame({
    'id': range(n_objects),
    'x':  np.random.randn(n_objects),
    'y': np.random.randn(n_objects)
})


# a 50 x 20 time series table
timeseries = pd.DataFrame(
    np.random.randn(n_times, n_objects).cumsum(0),
    columns=locations['id'],
    index=pd.RangeIndex(0, n_times, name="time")
)


# Melt the wide-form ts into a long-form view
timeseries = timeseries.reset_index().melt('time')
timeseries['id'] = timeseries['id'].astype(int)


# Join the two tables (source data)
data = pd.merge(timeseries, locations, on="id")


# Making an interactive chart (selection_simple for a single TS)
# on="mouseover", toggle=False,  (mouseover, "paint it, black")
selector = alt.selection_multi(empty="all", fields=['id'])

# the base for the chart
base = alt.Chart(data).properties(
    width=250,
    height=250
).add_selection(selector)

points = base.mark_point(filled=True, size=200).encode(
    x='mean(x)',
    y='mean(y)',
    color=alt.condition(selector, 'id:O', alt.value('lightgray'), legend=None),
    tooltip=[
        alt.Tooltip('id:O'),
        alt.Tooltip('x:N', format=".2f"),
        alt.Tooltip('y:N', format=".2f")
    ]
).interactive().properties(title="Relationship between X, Y")

tsplot = base.mark_line().encode(
    x="time",
    y=alt.Y('value', scale=alt.Scale(domain=(-15, 15))),
    color=alt.Color('id:O', legend=None), 
    tooltip=["id:O", "time:N"]
).transform_filter(selector).interactive().properties(title="Evolution of X")

st.write(points | tsplot)



# A cutoff example 
# ---- 
st.subheader("A cutoff example")

rand = np.random.RandomState(42)
df = pd.DataFrame({
    'xval': range(100), 
    'yval': rand.randn(100).cumsum()
})

slider = alt.binding_range(min=0, max=100, step=1, name="cutoff: ")
selector = alt.selection_single(name="SelectorName", fields=['cutoff'],
    bind=slider, init={'cutoff': 50})


chart_cutoff = alt.Chart(df).mark_point(filled=True, size=30).encode(
    x='xval',
    y='yval',
    color=alt.condition(
        alt.datum.xval < selector.cutoff,  # accesses the data explicitly
        alt.value('darkred'), alt.value('steelblue')
    )
).add_selection(selector).properties(width=500, height=300)

st.write(chart_cutoff)



# More interactive scatterplots
# ---- 
st.subheader("Interactive scatterplots")
cars = vdata.cars.url


brush = alt.selection_interval(
    encodings=['x'], empty="all", 
    mark=alt.BrushConfig(fill="#fdbb84", fillOpacity=0.2, stroke="#e34a33"), 
    # on="[mousedown[event.altKey], mouseup] > mousemove",
)  # x vertical selection


select_legend = alt.selection_multi(fields=["Origin"])
color = alt.condition(select_legend | brush, # or brush
    alt.Color('Origin:N', legend=None),
    alt.value('lightgray')
)
legend = alt.Chart(cars).mark_point().encode(
    y = alt.Y('Origin:N', axis=alt.Axis(orient="right")),
    color=color
).add_selection(select_legend)

base_cars = alt.Chart(cars).mark_point().encode(
    y="Horsepower:Q",
    color=color,
    tooltip=["Origin:N"]
).properties(width=250, height=250).add_selection(brush, select_legend)

chart_side = base_cars.encode(x="Acceleration:Q") | \
    base_cars.encode(x="Miles_per_Gallon:Q") | legend

st.write(chart_side)



source = vdata.population.url
boxplot_chart = alt.Chart(source).mark_boxplot().encode(
    x='age:O',
    y='people:Q'
).properties(
    width=600,
    height=300
)

st.write(boxplot_chart)


iris = vdata.iris.url

chart1 = alt.Chart(iris).mark_point().encode(
    x='petalLength:Q',
    y='petalWidth:Q',
    color='species:N'
).properties(
    height=300,
    width=300
)

chart2 = alt.Chart(iris).mark_bar().encode(
    x='count()',
    y=alt.Y('petalWidth:Q', bin=alt.Bin(maxbins=30)),
    color='species:N'
).properties(
    height=300,
    width=100
)

st.write(alt.hconcat(chart1, chart2))



base = alt.Chart(iris).mark_point().encode(
    alt.X(alt.repeat("column"), type='quantitative'),
    alt.Y(alt.repeat("row"), type='quantitative'),
    color='species:N'
).properties(
    width=200,
    height=200
).repeat(
    row=['petalLength', 'petalWidth'],
    column=['sepalLength', 'sepalWidth']
).configure_axis(grid=False).configure_view(strokeWidth=0)


st.write(base)


df = pd.DataFrame({'local': ['2018-01-01T00:00:00'],
                   'utc': ['2018-01-01T00:00:00Z']})