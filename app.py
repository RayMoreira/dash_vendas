import pandas as pd 
import plotly_express as px
import streamlit as st


# Lendo as bases de dados
df_vendas = pd.read_excel("Vendas.xlsx")
df_produtos = pd.read_excel("Produtos.xlsx")

# Fazendo um merge
df = pd.merge(df_vendas, df_produtos, how='left', on='ID Produto')

# Criando colunas
df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
df["Lucro"] = df["Valor Venda"] - df["Custo"]
df["mes_ano"] = df["Data Venda"].dt.to_period("M").astype(str)

# Agrupando dados (isso pode ser feito dentro da função se preferir)
produtos_por_marca = df.groupby('Marca')['Quantidade'].sum().reset_index()  # Total de produtos vendidos por marca
lucro_por_categoria = df.groupby('Categoria')['Lucro'].sum().reset_index()  # Total de lucro por categoria
lucro_mes_categoria = df.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()

def main(dataframe):
    st.title("Análise de Vendas")
    st.image("vendas.png")

    total_custo = dataframe["Custo"].sum()
    total_lucro = dataframe["Lucro"].sum()
    total_clientes = dataframe["ID Cliente"].nunique()

    total_custo_formatted = f"${total_custo:,.2f}"
    total_lucro_formatted = f"${total_lucro:,.2f}"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Custo", total_custo_formatted)

    with col2:
        st.metric("Total Lucro", total_lucro_formatted)
        
    with col3:
        st.metric("Total Clientes", total_clientes)

    # Criação das colunas para os gráficos
    col1, col2 = st.columns(2)

    # Gráfico de produtos vendidos por marca (horizontal)
    produtos_por_marca = dataframe.groupby('Marca').agg({'Quantidade': 'sum'}).reset_index()
    produtos_por_marca = produtos_por_marca.sort_values(by='Quantidade', ascending=True)

    with col1:
        fig_produtos = px.bar(produtos_por_marca, 
                               x='Quantidade', 
                               y='Marca', 
                               title='Total de Produtos Vendidos por Marca',
                               labels={'Quantidade': 'Quantidade Vendida', 'Marca': 'Marca'},
                               orientation='h')
        fig_produtos.update_traces(texttemplate='%{x}', textposition='auto', textfont_size=10)
        fig_produtos.update_layout(height=400, width=600, yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig_produtos)

    # Gráfico de lucro por categoria (pizza)
    with col2:
        lucro_por_categoria = dataframe.groupby('Categoria').agg({'Lucro': 'sum'}).reset_index()
        fig_lucro = px.pie(lucro_por_categoria, 
                           values='Lucro', 
                           names='Categoria', 
                           title='Lucro por Categoria',
                           labels={'Lucro': 'Valor do Lucro', 'Categoria': 'Categoria'})
        fig_lucro.update_layout(height=300, width=400)
        st.plotly_chart(fig_lucro)

    # Gráfico de lucro por mês e categoria
    st.subheader("Lucro por Mês e Categoria")  # Opcional: Adiciona um título para o gráfico
    fig2 = px.line(lucro_mes_categoria, 
                   x="mes_ano", 
                   y="Lucro",
                   title="Lucro por Mês e Categoria", 
                   color="Categoria", 
                   height=400, 
                   width=800)
    st.plotly_chart(fig2)
if __name__ == "__main__":
    main(df)
