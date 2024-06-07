import streamlit as st
import matplotlib.pyplot as plt
import utils.functions as f
import pandas as pd

st.set_page_config(
    page_title='Zabbix',
    page_icon='💻',
    layout='wide'
)

auth_token = f.get_zabbix_token()

st.title('Zabbix')
st.write('## Hosts')
st.write('Total de hosts: ', f.get_hosts_count(auth_token))
st.write('---')
st.write('## Alunos Sem usar notebook há 3 ou 7 dias')

col1, col2 = st.columns(2)
with col1:
    trigger_name = "Windows: o agente Zabbix não está disponível ha 3 dias"
    df_3dias = f.studentsByTrigger(auth_token, trigger_name)

with col2:
    trigger_name = "Windows: o agente Zabbix não está disponível ha 7 dias"
    df_7dias = f.studentsByTrigger(auth_token, trigger_name)

df_resultado = pd.merge(df_7dias, df_3dias, on='Host Name', how='outer')
df_resultado.fillna(False, inplace=True)
df_resultado['Host Name'] = df_resultado['Host Name'].str.replace('[a-zA-Z]', '', regex=True)
#Change column name
df_resultado.rename(columns={'Host Name': 'Patrimonio'}, inplace=True)
#df_debug = df_resultado[(df_resultado['+7DiasInativo'] == True) & (df_resultado['+3DiasInativo'] == True)]
st.write(df_resultado)

count_3a7diasInativo = df_resultado[(df_resultado['+7DiasInativo'] == False) & (df_resultado['+3DiasInativo'] == True)].shape[0]
count_mais7diasInativo = df_resultado[(df_resultado['+7DiasInativo'] == True) & (df_resultado['+3DiasInativo'] == True)].shape[0]
hosts_count = f.get_hosts_count(auth_token)
count_ativos = (int(hosts_count) - count_3a7diasInativo - count_mais7diasInativo)
# Criar um dataframe para os resultados
result_data = {
    'Combination': ['Ativos','3-7 Dias Inativo', '+7 Dias Inativo'],
    'Count': [count_ativos, count_3a7diasInativo, count_mais7diasInativo]
}
result_df = pd.DataFrame(result_data)

# Plotar os gráficos
plt.figure(figsize=(10, 5))

# Gráfico de barras
plt.subplot(1, 2, 1)
plt.bar(result_df['Combination'], result_df['Count'], color=['green', 'yellow','red'])
plt.title('Inatividade de Notebooks')
plt.xlabel('Atividade')
plt.ylabel('Contagem')

# Gráfico de pizza
plt.subplot(1, 2, 2)
plt.pie(result_df['Count'], labels=result_df['Combination'], autopct='%1.1f%%', colors=['green', 'yellow','red'])
plt.title('Inatividade de Notebooks')

plt.tight_layout()
plt.show()

st.pyplot(plt)