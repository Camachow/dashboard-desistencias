import streamlit as st
import pandas as pd
import plotly.express as px
from utils.functions import *
from utils.charts import histograma as hist
from utils.globals import *


st.set_page_config(
    page_title='Cidades',
    page_icon='🌇',
    layout='wide'
)

cidades = ['Bom Despacho', 'Itabira', 'Pequi']
cidade = st.selectbox('Selecione a cidade', cidades)

# Inicializar as chaves no st.session_state, se não estiverem definidas
if 'alunosBomDespacho' not in st.session_state:
    st.session_state['alunosBomDespacho'] = []

if 'inscricoesBomDespacho' not in st.session_state:
    st.session_state['inscricoesBomDespacho'] = []

if 'alunosItabira' not in st.session_state:
    st.session_state['alunosItabira'] = []

if 'inscricoesItabira' not in st.session_state:
    st.session_state['inscricoesItabira'] = []

if 'alunosPequi' not in st.session_state:
    st.session_state['alunosPequi'] = []

if 'inscricoesPequi' not in st.session_state:
    st.session_state['inscricoesPequi'] = []

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

if not inscricoesAprovados:
    inscricoesAprovados = MODELOJSON

#alunosEvasao = [aluno for aluno in alunos if aluno.get('status') == 'Inativo']

# Certifique-se de que os dados estão em formato de DataFrame
if isinstance(inscricoes, list):
    inscricoes = pd.DataFrame(inscricoes)
if isinstance(inscricoesAprovados, list):
    inscricoesAprovados = pd.DataFrame(inscricoesAprovados)
if isinstance(alunos, list):
    alunos_df = pd.DataFrame(alunos)
    alunosEvasao = alunos_df[alunos_df['status'] == 'Inativo']

alunosEvasao = alunosEvasao.drop(columns=['createdAt', 'cel', 'cityId', 'id', 'numero', 'bairro', 'complemento', 'rua', 'cep', 'dataNasc', 'hasPreferredName', 'preferredName', 'nomeCompleto', 'emailPd'])
alunosEvasaoComleta = pd.merge(inscricoesAprovados, alunosEvasao, on='cpf', how='inner')

verificaDataNasc(inscricoes)
verificaDataNasc(inscricoesAprovados)
verificaDataNasc(alunosEvasaoComleta)

st.write(f"### {cidade}")

st.write('## Status dos Alunos Atualmente')
st.write(f"Total de inscritos: {len(alunos)}")
st.write(f"Total de ativos: {contar_usuarios_com_atributo(alunos, 'status', 'Ativo')}")
st.write(f"Total de Suspensos: {contar_usuarios_com_atributo(alunos, 'status', 'Suspenso')}")
st.write(f"Total de inativos: {contar_usuarios_com_atributo(alunos, 'status', 'Inativo')}")
st.write('---')

fig = px.pie(alunos, names='status')
st.plotly_chart(fig)

st.write('---')

st.write('## Processo Seletivo x Aprovados')

#if inscricoes['genero'] is not None:
st.write('### Gênero')

# Remover valores None da coluna "genero"
filtered_genero = [g for g in inscricoes["genero"].unique() if g is not None]

hist(
    inscricoes['genero'],
    inscricoes[inscricoes['absent'] == False]['genero'],
    inscricoesAprovados['genero'],
    alunosEvasaoComleta['genero'],
    ['Feminino','Masculino','NaoBinario','Outros','PrefiroNaoDeclarar']
)

st.write('### Idade')

hist(
    inscricoes['faixa_etaria'],
    inscricoes[inscricoes['absent'] == False]['faixa_etaria'],
    inscricoesAprovados['faixa_etaria'],
    alunosEvasaoComleta['faixa_etaria'],
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
alunosEvasaoComleta['rendaFamiliar'] = alunosEvasaoComleta['rendaFamiliar'].map(mapa_renda)

hist(
    inscricoes['rendaFamiliar'],
    inscricoes[inscricoes['absent'] == False]['rendaFamiliar'],
    inscricoesAprovados['rendaFamiliar'],
    alunosEvasaoComleta['rendaFamiliar'],
    ["Menor que 1","Entre 1 e 3","Entre 3 e 10","Entre 10 e 40", "Maior que 40"]
)

st.write('### Raça')

hist(
    inscricoes['raca'],
    inscricoes[inscricoes['absent'] == False]['raca'],
    inscricoesAprovados['raca'],
    alunosEvasaoComleta['raca'],
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
alunosEvasaoComleta['escolaPublica'] = alunosEvasaoComleta['escolaPublica'].map(mapa_renda)

hist(
    inscricoes['escolaPublica'],
    inscricoes[inscricoes['absent'] == False]['escolaPublica'],
    inscricoesAprovados['escolaPublica'],
    alunosEvasaoComleta['escolaPublica'],
    ["Publica","Particular"]
)

st.write('---')

st.write('## Tabelas')
st.write('### Inscritos')
st.write(inscricoes)
st.write('### Alunos')
st.write(alunos_df)
st.write('### Aprovados')
st.write(inscricoesAprovados)
st.write('### Alunos com Evasão')
st.write(alunosEvasaoComleta)

