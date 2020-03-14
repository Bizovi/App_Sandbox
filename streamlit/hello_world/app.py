import streamlit as st
import pandas as pd
import numpy as np
import time

import altair as alt  # out of the box
import matplotlib.pyplot as plt  # out of the box
import plotly.figure_factory as ff  # requires scipy
import graphviz
from PIL import Image

import datetime 

# Adding a title
st.title('A very basic streamlit app \n')

# markdown magic
"""
A lightweight and fast framework for interactive visualization:
* Showcase the results of **ML models**
* Write clean code without _callbacks_

```bash
streamlit run my_app.py
```

The markdown also supports LaTeX (more exactly KaTeX):

$$y_i \sim N(\mu_i, \sigma^2)$$
"""

st.latex(r'''
     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
     \sum_{k=0}^{n-1} ar^k =
     a \left(\frac{1-r^{n}}{1-r}\right)
     ''')

st.sidebar.markdown(
    """
    ### Exploring the features
    * UI elements
    * Caching and updating
    """
)

# Explore UI elements
st.header("The standard API")
st.subheader("Exploring basic UI elements")
with st.echo():
    # show some code in the app
    def hello_function(my_name):
        return "Hello " + my_name + "!"

st.code("""pip list | grep pandas""", language="bash")
st.json({
    'amid': 'PCT9991',
    'number_comparables': 10,
    'parameters': [
        'color', 'padding', 'shape'
    ]
})

# a button
if st.button('Say hello'):
    st.write("Hello there")
else:
    st.write("Goodbye")


# radioboxes
genre = st.radio(
    "What's your favorite movie genre?",
    ('Comedy', 'Drama', 'Documentary'), 
    index=1
)

if genre == "Comedy":
    st.write("You should watch Dumb and the Dumber")
else:
    st.write("You should watch Twelve Angry Men")


option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home Phone", "Mobile Phone")
)

st.write("You selected: ", option)


options = st.multiselect(
    "What are your favorite colors",
    ('Green', "Yellow", "Red", "Blue"),
    ('Yellow', 'Red')
)
st.write("You selected:", options)


d = st.date_input(
    'When is your birthday',
    datetime.date(2019, 7, 6))
st.write('Your birthday is:', d)

# t = st.time_input('Set an alarm for', datetime.time(8, 45))
# st.write('Alarm is set for', t)


# widgets are treated as variables
st.subheader("A slider example")
x = st.slider('Select a value', min_value=1, max_value=100, value=12)
st.write(x, 'squared is', x ** 2)  # can pass anything into it


# listing a pandas.DataFrame
st.subheader("A dummy table updated by the slider")
df_dummy =  pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [elem * x for elem in [10, 10, 30, 40]]
})

# st.write(df_dummy)
# st.dataframe(df_dummy)
st.table(df_dummy)
option = st.sidebar.selectbox(
    "Which value of the first column do you want to select?",
    df_dummy['first column']
)

st.sidebar.markdown('You selected the option nr. ' + str(option))


# load some data into memory
st.subheader("Loading data with caching")
read_and_cache_csv = st.cache(pd.read_csv)

BUCKET = "https://streamlit-self-driving.s3-us-west-2.amazonaws.com/"
data = read_and_cache_csv(BUCKET + "labels.csv.gz", nrows=1000)
desired_label = st.selectbox('Filter to:', ['car', 'truck'])
st.write(data[data.label == desired_label])


# drawing basic charts
st.header("Data Visualization")
st.subheader("Some basic charts/plots")

chart_data = pd.DataFrame(
    np.random.randn(100, 3), 
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)  # uses Vega by default

if st.checkbox('Show bar and area plots', False):
    # area and bar charts
    chart_data_low = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c']
    )
    st.area_chart(chart_data_low)
    st.bar_chart(chart_data_low)

    # matplotlib chart
    _ = plt.hist(chart_data['a'], bins=30)
    _ = plt.title("Distribution of X")
    st.pyplot()

# drawing a scatterplot
df_normal = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c']
)

# altair charts
c = alt.Chart(df_normal).mark_circle().encode(
    x='a', y='b', size='c', color='c'
)
st.write(c)

# vega charts
vega_check = st.checkbox("Same, but with VegaLite", False)
if vega_check:
    st.vega_lite_chart(df_normal, {
        'mark': 'circle',
        'encoding': {
            'x': {'field': 'a', 'type': 'quantitative'},
            'y': {'field': 'b', 'type': 'quantitative'},
            'size': {'field': 'c', 'type': 'quantitative'},
            'color': {'field': 'c', 'type': 'quantitative'}
        }
    })

# drawing a map
map_check = st.checkbox("Show map", False)
if map_check:
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])
    # st.map(map_data)

    # a better map with perspective
    st.deck_gl_chart(
        viewport={
            'latitude': 37.76,
            'longitude': -122.4,
            'zoom': 11,
            'pitch': 50,
        },
        layers=[{
            'data': map_data,
            'type': 'ScatterplotLayer'
        }]
    )

# st.subheader("Simulate a long running process")

# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#     latest_iteration.text(f'Iteration {i + 1}')
#     bar.progress(i + 1)
#     time.sleep(0.1)
# st.write('we are done')

x1 = np.random.randn(200) - 3
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

hist_data = [x1, x2, x3]
group_labels = ["Group 1", "Group 2", "Group 3"]

fig = ff.create_distplot(
    hist_data, group_labels, bin_size=[.1, .25, .5]
)
st.plotly_chart(fig)


# plotting graphs
st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
''')


# image = Image.open("my_image.png")
# st.image(image, caption='Sunrise by the mountains', use_column_width=True)