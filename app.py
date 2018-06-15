from flask import Flask, render_template, request, redirect
import quandl as q
import pandas as pd
from bokeh.models.widgets import TextInput #Select
from bokeh.plotting import figure, show #, output_file
from bokeh.models import Band, ColumnDataSource, Range1d, Title
from bokeh.embed import components
#setting api key to access data from quandl
q.ApiConfig.api_key = "WTAu2SBBZyADGzrpPL-c"

#def get_stock_data(ti):
    #data = q.get_table('WIKI/PRICES', paginate=True,
    #               ticker = ti, date = { 'gte': '2018-01-01', 'lte': '2018-04-01' },
    #               qopts={"columns":["ticker", "date", "close", "low", "high"]})
    #return data

def create_stock_plot(ti):
    data = q.get_table('WIKI/PRICES', paginate=True,
                   ticker = ti, date = { 'gte': '2018-01-01', 'lte': '2018-04-01' },
                   qopts={"columns":["ticker", "date", "close", "low", "high"]})
    #creating dictionary database to plot
    df = pd.DataFrame(data=dict(x=data.date, y=data.close, low=data.low, high=data.high)).sort_values(by="x")
    source = ColumnDataSource(df.reset_index())

    t1 = "Closing Cost with High/Low Reach Band for Stock: '%s'" %(ti)
    t2 = "From %s to %s" %('Jan 2018', 'Apr 2018')
    #figure configuration
    p = figure(title = t1, plot_width=500, plot_height=500, x_axis_type="datetime")
    p.y_range = Range1d(data.low[data.low.idxmin()]-2, data.high[data.high.idxmax()]+2)
    p.xaxis.axis_label = 'Days'
    p.yaxis.axis_label = 'Value in USD'

    p.line('x', 'y', color = 'firebrick', source = source, line_width=2)

    band = Band(base = 'x', lower='low', upper='high', level='underlay', source = source,
                fill_alpha=0.5, line_width=1, line_color='black', fill_color = 'grey')

    p.add_layout(band)
    p.add_layout(Title(text=t2, align="center"), "below")
    return p

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    ti = request.form['stock-ticker']
    #ti = text.upper()
    # Create the plot
    plot = create_stock_plot(ti)
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("graph2.html", script=script, div=div)

@app.route('/graph')
def graph():
    script, div = components(plot)
    return render_template('graph2.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
