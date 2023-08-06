"""Defines all functions within plot part of exergi package."""

from pandas import DataFrame
from plotly import express


def lineplot(df_: DataFrame, x_name: str, y_names: list, width=1200, 
             height=500, title='No title'):
    """Create a figure of columns in specified dataframe using plotly.
    
    Arguments:
        df_         - Dataframe with data to plot. All data must be in the 
                      same dataframe    
        x           - String with name of column for x-axis, can't be index
        y           - List of string with name of columns for y-axis.
        width       - Width por plot in pixels.
        height      - Height por plot in pixels.        
        title       - Title for plot.
        
    Returns:
        - Plotly figure with legend.

    """
    # Define position of legend
    legend_dict = dict(orientation='h', yanchor='bottom', y=1.0, 
                       xanchor='left', x=0)
    
    # Create figure
    fig = express.line(df_, x=x_name, y=y_names, title=title, width=width, 
                       height=height)
    fig.update_layout(legend=legend_dict)
    fig.show()
