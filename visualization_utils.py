import altair as alt
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd


red   = "rgb(180, 32, 52)"
green = "rgb(46, 209, 149)"


def create_line_chart(df, x_axis, y_axis, title):

    range_ = [red, green]
    line_chart = alt.Chart(df).mark_bar(interpolate='linear').encode(
    #x = x_axis,
    alt.X('Umsatztyp:N'),
    y = y_axis,
    #color=alt.Color('Umsatztyp').scale(domain=domain, range=range_)
    color=alt.Color('Umsatztyp', scale={"range": range_}),
    column=x_axis,
    ).properties(
    title=title
    )

    return line_chart


def aufstellung_bar_chart(df, x_axis, y_axis, title):
    plot = px.bar(df[['Betrag_absolut', 'Umsatztyp']], color='Umsatztyp',
                  color_discrete_sequence= [red, green], barmode='group',
                  y=y_axis,
                  title=title)
    plot.update_layout(yaxis_tickprefix = '€', yaxis_tickformat = '%.2f')
    plot.update_xaxes(showline=True, gridcolor="rgb(238, 232, 213)", zeroline=True)
    plot.update_yaxes(showline=True, gridcolor="rgb(238, 232, 213)", zeroline=True)
    return plot
    

def create_plotly_pie_chart(df, values='Betrag_absolut', names='Zahlungsempfänger*in', title='Zahlungsempfänger'):
    plot = px.pie(df, values=values, names=names, title=title, color_discrete_sequence=px.colors.sequential.Darkmint, hole=.3)
    plot.update_layout(yaxis_ticksuffix = '€', yaxis_tickformat = '%.2f')#, hover_tickformat= '%.2f')

    return plot


def create_histogram(df, y_axis, n_bins, histfunc='count'):
    plot = px.histogram(df[[y_axis]], nbins=n_bins, histfunc='avg')
    return plot


def bar_chart(df, y_axis, title=""):
    plot = px.bar(df[y_axis], y=y_axis, title=title)
    plot.update_layout(yaxis_ticksuffix = '€', yaxis_tickformat = '%.2f')
    plot.update_layout(hovermode="x")
    plot.update_traces(hovertemplate=f"{y_axis}: "+"%{y:.2f}€")
    plot.update_xaxes(showline=True, gridcolor="rgb(238, 232, 213)", zeroline=True)
    plot.update_yaxes(showline=True, gridcolor="rgb(238, 232, 213)", zeroline=True)
    plot.update_traces(marker_color=red)
    return plot