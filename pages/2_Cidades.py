import streamlit as st
import pandas as pd
import plotly.express as px
from utils.functions import *
from utils.charts import histograma as hist

st.set_page_config(
    page_title='Cidades',
    page_icon='🌇',
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

hist(
    inscricoes['genero'],
    inscricoes[inscricoes['absent'] == False]['genero'],
    inscricoesAprovados['genero'],
    ['Feminino','Masculino','NaoBinario','Outros','PrefiroNaoDeclarar']
)

st.write('### Idade')

hist(
    inscricoes['faixa_etaria'],
    inscricoes[inscricoes['absent'] == False]['faixa_etaria'],
    inscricoesAprovados['faixa_etaria'],
    ['15-18', '19-25', '26-35', '36+']
)


st.write('### Renda Familiar')

# Mapeamento de valores originais para novos nomes
mapa_renda = {
    'InferiorAUmSalarioMinimo': 'Menor que 1',
    'De1a3SalariosMinimos': 'Entre 1 e 3',
    'De3a10SalariosMinimos': 'Entre 3 e 10',
    'De10a40SalariosMinimos': 'Entre 10 e 40',
    'MaisDe40SalariosMinimos': 'Maior que 40',
}

# Aplicar o mapeamento aos dados
inscricoes['rendaFamiliar'] = inscricoes['rendaFamiliar'].map(mapa_renda)
inscricoesAprovados['rendaFamiliar'] = inscricoesAprovados['rendaFamiliar'].map(mapa_renda)

hist(
    inscricoes['rendaFamiliar'],
    inscricoes[inscricoes['absent'] == False]['rendaFamiliar'],
    inscricoesAprovados['rendaFamiliar'],
    ["Menor que 1","Entre 1 e 3","Entre 3 e 10","Entre 10 e 40", "Maior que 40"]
)

st.write('### Raça')

hist(
    inscricoes['raca'],
    inscricoes[inscricoes['absent'] == False]['raca'],
    inscricoesAprovados['raca'],
    ["Branca","Preta","Parda","Amarela"]
)

st.write('### Escola Pública')
# Mapeamento de valores originais para novos nomes
mapa_renda = {
    True: 'Publica',
    False: 'Particular'
}

# Aplicar o mapeamento aos dados
inscricoes['escolaPublica'] = inscricoes['escolaPublica'].map(mapa_renda)
inscricoesAprovados['escolaPublica'] = inscricoesAprovados['escolaPublica'].map(mapa_renda)

hist(
    inscricoes['escolaPublica'],
    inscricoes[inscricoes['absent'] == False]['escolaPublica'],
    inscricoesAprovados['escolaPublica'],
    ["Publica","Particular"]
)

st.write('---')

st.write('## Tabelas')
st.write('### Inscritos')
st.write(inscricoes)
st.write('### Aprovados')
st.write(inscricoesAprovados)

