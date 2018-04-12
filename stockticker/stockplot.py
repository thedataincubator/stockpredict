"""plot for stockticker app"""
from bokeh.plotting import figure
from bokeh.embed import components

def plotting(prediction, df): # pylint: disable=C0103
    """plots two lines given by prediction and df"""
    fig = figure(x_axis_type="datetime")
    fig.line(prediction['ds'].values,
             prediction['yhat'].values,
             line_color='red')
    fig.line(df['ds'].values, df['y'].values)
    script, div = components(fig)
    return script, div
