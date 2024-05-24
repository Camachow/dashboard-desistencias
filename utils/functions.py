import streamlit as st

# Função para contar usuários com um atributo específico
def contar_usuarios_com_atributo(usuarios, atributo, valor):
    return sum(1 for usuario in usuarios if usuario.get(atributo) == valor)

def mostrar_dados_cidade(cidade, alunos):
    st.write(f"### {cidade}")
    st.write(f"Total de inscritos: {len(alunos)}")
    st.write(f"Total de ativos: {contar_usuarios_com_atributo(alunos, 'status', 'Ativo')}")
    st.write(f"Total de Suspensos: {contar_usuarios_com_atributo(alunos, 'status', 'Suspenso')}")
    st.write(f"Total de inativos: {contar_usuarios_com_atributo(alunos, 'status', 'Inativo')}")
