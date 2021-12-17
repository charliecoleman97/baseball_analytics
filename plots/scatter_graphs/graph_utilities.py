import pybaseball as pb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
import plotly.io as pio
import numpy as np
from PIL import Image
import math



def scatter_with_regression(dataframe, x_val:str, y_val:str, colour_val:str, hover_name= "Name", hover_data_1="Team", hover_data_2="PA"):
    # plot scatter points
    fig = px.scatter(
        dataframe, x=f"{x_val}", y=f"{y_val}",
        color=colour_val,
        hover_name=hover_name,
        hover_data=[hover_data_1, hover_data_2],
        color_continuous_scale=px.colors.diverging.Tropic,
        width=1350, height=700,
        title=f'{x_val} vs {y_val}'
    )
    # change marker style
    fig.update_traces(marker_line_width=2, marker_size=10)
    fig.update_yaxes(nticks=20)
    fig.update_xaxes(nticks=40)
    
    # add regression and standard deviation lines
    #obtain m (slope) and b(intercept) of linear regression line
    x=dataframe[f"{x_val}"]
    y=dataframe[f"{y_val}"]
    m, b = np.polyfit(x, y, 1)

    #add linear regression lines to scatterplot and
    x_linspace = np.linspace(x.min(), x.max(), 100)
    y_sigma = y.std()



    COLORS = px.colors.qualitative.D3
    hex_color =COLORS[0]

    fig.add_traces(go.Scatter(
        x=x_linspace, 
        y=m*x_linspace+b, 
        showlegend=False,
        name='regression',
        line=dict(
            color='rgba' + str(hex_to_rgba(h=hex_color, alpha=0.4)
        ),
        width=2,
        dash='dash')
    ))

    fig.add_traces(go.Scatter(
        x=x_linspace, 
        y=m*x_linspace+(b+y_sigma), 
        showlegend=False,
        name='+1 st_dev',
        line=dict(
            color='rgba' + str(hex_to_rgba(h=hex_color, alpha=0.4)
        ),
        width=2,
        dash='dash')
    ))

    fig.add_traces(go.Scatter(
        x=x_linspace, 
        y=m*x_linspace+(b-y_sigma), 
        showlegend=False,
        name='-1 st_dev',
        line=dict(
            color='rgba' + str(hex_to_rgba(h=hex_color, alpha=0.4)
        ),
        width=2,
        dash='dash')
    ))

    return fig


def hex_to_rgba(h, alpha):
    '''
    converts color value in hex format to rgba format with alpha transparency
    '''
    return tuple([int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)] + [alpha])


def scatter(dataframe, x_val:str, y_val:str, colour_val:str, hover_name= "Name", hover_data_1="Team", hover_data_2="PA"):

    fig1 = px.scatter(
        dataframe, x=f"{x_val}", y=f"{y_val}",
        color=colour_val,
        hover_name=hover_name,
        hover_data=[hover_data_1, hover_data_2],
        color_continuous_scale=px.colors.diverging.Tropic,
        width=1350, height=700,
        title=f'{x_val} vs {y_val}'

    )

    fig1.update_traces(marker_line_width=2, marker_size=10)
    fig1.update_yaxes(nticks=20)
    fig1.update_xaxes(nticks=40)

    # Means
    fig1.add_hline(y=np.mean(dataframe[y_val]), line_dash="dot", row="all", col="all",
                annotation_text=f"Mean {y_val}", 
                annotation_position="bottom right")

    fig1.add_vline(x=np.mean(dataframe[x_val]), line_dash="dot", row="all", col="all",
                annotation_text=f"Mean {x_val}", 
                annotation_position="bottom right")
    return fig1


def add_percentiles(dataframe:str, x_val:str, y_val:str, fig:str, upper_percentile:int, lower_percentile:int):
    # Upper Percentile
    fig.add_shape(
        x0=dataframe[x_val].quantile(q=upper_percentile), 
        y0=dataframe[y_val].quantile(q=upper_percentile),
        x1=dataframe[x_val].quantile(q=1),
        y1=dataframe[y_val].quantile(q=1),
        line=dict(color="LightSeaGreen", width=2, dash="dot"),
        )
    fig.add_annotation(
        x=dataframe[x_val].quantile(q=upper_percentile),
        y=dataframe[y_val].quantile(q=1),
        text = f"{math.trunc(upper_percentile*100)}th percentile",
        font=dict(
            family="arial",
            size=15,
            color="LightSeaGreen"
        )
    )

    # Lower Percentile
    fig.add_shape(
        x0=dataframe[x_val].quantile(q=0), 
        y0=dataframe[y_val].quantile(q=0),
        x1=dataframe[x_val].quantile(q=lower_percentile),
        y1=dataframe[y_val].quantile(q=lower_percentile),
        line=dict(
            color="#EF553B", 
            width=2, 
            dash="dot")
        )

    fig.add_annotation(
    x=dataframe[x_val].quantile(q=0),
    y=dataframe[y_val].quantile(q=lower_percentile),
    text = f"{math.trunc(lower_percentile*100)}th percentile",
    font=dict(
        family="arial",
        size=15,
        color="#EF553B"
    )
    )
    return fig


def add_annotation(fig, message, x_pos, y_pos, color='black',arrow=False):
    fig.add_annotation(
    x=x_pos, 
    y=y_pos,
    text=message,
    showarrow=arrow,
    font=dict(
        family="arial",
        size=18,
        color=color
    )
    )
    return fig


def add_shape(fig:str, x0, x1, y0, y1, shape_type="circle", outline_color="purple"):
    fig.add_shape(
        type=shape_type,
        xref="x", yref="y",
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(color=outline_color, width=2, dash="dash")
    )
    return fig