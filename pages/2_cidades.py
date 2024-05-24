import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.functions import *

st.set_page_config(
    page_title='Cidades',
    page_icon=':city:',
    layout='wide'
)

cidades = ['Bom Despacho', 'Itabira', 'Pequi']
cidade = st.selectbox('Selecione a cidade', cidades)

if cidade == 'Bom Despacho':
    alunos = st.session_state['alunosBomDespacho']
    inscricoes = st.session_state['inscricoesBomDespacho']

elif cidade == 'Itabira':
    alunos = st.session_state['alunosItabira']
    inscricoes = st.session_state['inscricoesItabira']

else:
    alunos = st.session_state['alunosPequi']
    inscricoes = st.session_state['inscricoesPequi']

### Tratamento dos Dados
inscricoesAprovados = [inscricao for inscricao in inscricoes if inscricao.get('enrolled') == True]
alunosEvasao = [aluno for aluno in alunos if aluno.get('status') == 'Inativo']

# Certifique-se de que os dados estão em formato de DataFrame
if isinstance(inscricoes, list):
    inscricoes = pd.DataFrame(inscricoes)
if isinstance(inscricoesAprovados, list):
    inscricoesAprovados = pd.DataFrame(inscricoesAprovados)

# Verifique se a coluna 'dataNasc' está presente
if 'dataNasc' not in inscricoes.columns:
    st.error("Coluna 'dataNasc' não encontrada em 'inscricoes'")
    st.stop()

if 'dataNasc' not in inscricoesAprovados.columns:
    st.error("Coluna 'dataNasc' não encontrada em 'inscricoesAprovados'")
    st.stop()

# Adiciona colunas de idade e faixa etária
inscricoes['dataNasc'] = pd.to_datetime(inscricoes['dataNasc'], errors='coerce')
inscricoes['idade'] = inscricoes['dataNasc'].apply(calcular_idade)
inscricoes['faixa_etaria'] = inscricoes['idade'].apply(categorizar_idade)

inscricoesAprovados['dataNasc'] = pd.to_datetime(inscricoesAprovados['dataNasc'], errors='coerce')
inscricoesAprovados['idade'] = inscricoesAprovados['dataNasc'].apply(calcular_idade)
inscricoesAprovados['faixa_etaria'] = inscricoesAprovados['idade'].apply(categorizar_idade)

st.write(f"### {cidade}")
st.write(f"Total de inscritos: {len(alunos)}")
st.write(f"Total de ativos: {contar_usuarios_com_atributo(alunos, 'status', 'Ativo')}")
st.write(f"Total de Suspensos: {contar_usuarios_com_atributo(alunos, 'status', 'Suspenso')}")
st.write(f"Total de inativos: {contar_usuarios_com_atributo(alunos, 'status', 'Inativo')}")
st.write('---')

st.write('## Status dos Alunos Atualmente')
col1, col2 = st.columns(2)
with col1:
    fig = px.pie(alunos, names='status')
    st.plotly_chart(fig)

st.write('---')

st.write('## Processo Seletivo x Aprovados')

st.write('### Gênero')

# Remover valores None da coluna "genero"
filtered_genero = [g for g in inscricoes["genero"].unique() if g is not None]

fig_hist = make_subplots(rows=2, cols=2, horizontal_spacing=0.2)
#Inscrições
fig_hist.append_trace(go.Histogram( 
    y=inscricoes['genero'],
    histnorm='percent',
    name='Inscritos', 
    xbins=dict(size=0.3),
    marker_color='#E800E7',
    opacity=0.75
), 1,1)
#Compareceram
fig_hist.append_trace(go.Histogram(
    y=inscricoes[inscricoes['absent'] == False]['genero'],
    histnorm='percent',
    name='Compareceram',
    xbins=dict(size=0.3),
    marker_color='#0094FF',
    opacity=0.75
), 1, 2 )
#Aprovados
fig_hist.append_trace(go.Histogram(
    y=inscricoesAprovados['genero'],
    histnorm='percent',
    name='Aprovados', 
    xbins=dict(size=0.3),
    marker_color='#FE8C00',
    opacity=0.75
), 2, 1)
#Atualização aplicada a todos os subplots
fig_hist.update_xaxes(showgrid=True, ticks="outside", range=[0, None])
st.plotly_chart(fig_hist)

st.write('### Idade')
fig_hist = make_subplots(rows=2, cols=2, horizontal_spacing=0.2)

# Remover valores None da coluna "faixa_etaria"
#filtered_faixa_etaria = [g for g in inscricoes["faixa_etaria"].unique() if g is not None]
# Definindo a ordem das categorias no eixo y
#categoria_ordem = sorted(inscricoes["faixa_etaria"].unique())

#Inscrições
fig_hist.append_trace(go.Histogram( 
    y=inscricoes['faixa_etaria'],
    histnorm='percent',
    name='Inscritos', 
    xbins=dict(size=0.3),
    marker_color='#E800E7',
    opacity=0.75
), 1,1)
#Compareceram
fig_hist.append_trace(go.Histogram(
    y=inscricoes[inscricoes['absent'] == False]['faixa_etaria'],
    histnorm='percent',
    name='Compareceram',
    xbins=dict(size=0.3),
    marker_color='#0094FF',
    opacity=0.75
), 1, 2 )
#Aprovados
fig_hist.append_trace(go.Histogram(
    y=inscricoesAprovados['faixa_etaria'],
    histnorm='percent',
    name='Aprovados', 
    xbins=dict(size=0.3),
    marker_color='#FE8C00',
    opacity=0.75
), 2, 1)
#Atualização aplicada a todos os subplots
fig_hist.update_yaxes(categoryorder='array', categoryarray=["15-18","19-25","26-35","36+"])
fig_hist.update_xaxes(showgrid=True, ticks="outside", range=[0, None])
st.plotly_chart(fig_hist)


st.write('### Renda Familiar')
fig_hist = make_subplots(rows=2, cols=2, horizontal_spacing=0.2)

#Inscrições
fig_hist.append_trace(go.Histogram( 
    y=inscricoes['rendaFamiliar'],
    histnorm='percent',
    name='Inscritos', 
    xbins=dict(size=0.3),
    marker_color='#E800E7',
    opacity=0.75
), 1,1)
#Compareceram
fig_hist.append_trace(go.Histogram(
    y=inscricoes[inscricoes['absent'] == False]['rendaFamiliar'],
    histnorm='percent',
    name='Compareceram',
    xbins=dict(size=0.3),
    marker_color='#0094FF',
    opacity=0.75
), 1, 2 )
#Aprovados
fig_hist.append_trace(go.Histogram(
    y=inscricoesAprovados['rendaFamiliar'],
    histnorm='percent',
    name='Aprovados', 
    xbins=dict(size=0.3),
    marker_color='#FE8C00',
    opacity=0.75
), 2, 1)
#Atualização aplicada a todos os subplots
fig_hist.update_yaxes(categoryorder='array', categoryarray=["15-18","19-25","26-35","36+"])
fig_hist.update_xaxes(showgrid=True, ticks="outside", range=[0, None], categoryorder='array', categoryarray=["15-18","19-25","26-35","36+"])
st.plotly_chart(fig_hist)


st.write('### Raça')
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(inscricoes, x='raca')
    fig.update_layout(title='Inscrições por Raça')
    st.plotly_chart(fig)
with col2:
    fig = px.histogram(inscricoesAprovados, x='raca')
    fig.update_layout(title='Inscrições Aprovadas por Raça')
    st.plotly_chart(fig)

st.write('### Escola Pública')
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(inscricoes, x='escolaPublica')
    fig.update_layout(title='Inscrições por Escola Pública')
    st.plotly_chart(fig)
with col2:
    fig = px.histogram(inscricoesAprovados, x='escolaPublica')
    fig.update_layout(title='Inscrições Aprovadas por Escola Pública')
    st.plotly_chart(fig)

st.write('## Tabelas')
st.write('### Inscritos')
st.write(inscricoes)
st.write('### Aprovados')
st.write(inscricoesAprovados)

