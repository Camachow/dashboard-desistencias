from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st


def histograma(yInscritos, yCompareceram, yAprovados, yEvasao, categoryarray):
    fig_hist = make_subplots(rows=2, cols=2, horizontal_spacing=0.2)
    #Inscrições
    fig_hist.append_trace(go.Histogram( 
        y = yInscritos,
        histnorm='percent',
        name='Inscritos', 
        xbins=dict(size=0.3),
        marker_color='#E800E7',
        opacity=0.75
    ), 1,1)
    #Compareceram
    fig_hist.append_trace(go.Histogram(
        y = yCompareceram,
        histnorm='percent',
        name='Compareceram',
        xbins=dict(size=0.3),
        marker_color='#0094FF',
        opacity=0.75
    ), 1, 2 )
    #Aprovados
    fig_hist.append_trace(go.Histogram(
        y = yAprovados,
        histnorm='percent',
        name='Aprovados', 
        xbins=dict(size=0.3),
        marker_color='#8C44FF',
        opacity=0.75
    ), 2, 1)
    #Evasão
    fig_hist.append_trace(go.Histogram(
        y = yEvasao,
        histnorm='percent',
        name='Evasão', 
        xbins=dict(size=0.3),
        marker_color='#FE8C00',
        opacity=0.75
    ), 2, 2)
    #Atualização aplicada a todos os subplots
    fig_hist.update_yaxes(categoryorder='array', categoryarray = categoryarray)
    fig_hist.update_xaxes(showgrid=True, ticks="outside", range=[0, None])
    st.plotly_chart(fig_hist)