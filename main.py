import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="Análisis Financiero", layout="wide")

# Cargar datos
url = "https://raw.githubusercontent.com/oscarjuarez17/Analisis_Solvencia_financiera/refs/heads/main/Datos_proyecto_Clean.csv"
data = pd.read_csv(url)

st.title("Proyecto Final Oscar Juarez")

# Mostrar los datos
st.title("Análisis de Solvencia Financiera")
st.write("Datos cargados desde GitHub:")
st.dataframe(data)

# Calcular los ratios
data['Liquidity_Ratio'] = data['Current_Assets'] / data['Current_Liabilities']
data['Debt_to_Equity_Ratio'] = (data['Short_Term_Debt'] + data['Long_Term_Debt']) / data['Equity']
data['Financial_Expenses_Coverage'] = data['Total_Revenue'] / data['Financial_Expenses']

# Filtros interactivos
st.sidebar.header("Filtros")
company_id = st.sidebar.multiselect("Seleccionar Company_ID", options=data['Company_ID'].unique())
country = st.sidebar.multiselect("Seleccionar País", options=data['Country'].unique())
industry = st.sidebar.multiselect("Seleccionar Industria", options=data['Industry'].unique())
company_size = st.sidebar.multiselect("Seleccionar Tamaño de Empresa", options=data['Company_Size'].unique())

# Filtrar los datos según la selección
filtered_data = data.copy()
if company_id:
    filtered_data = filtered_data[filtered_data['Company_ID'].isin(company_id)]
if country:
    filtered_data = filtered_data[filtered_data['Country'].isin(country)]
if industry:
    filtered_data = filtered_data[filtered_data['Industry'].isin(industry)]
if company_size:
    filtered_data = filtered_data[filtered_data['Company_Size'].isin(company_size)]

# Resumir el ratio de liquidez por industria
liquidity_summary = filtered_data.groupby('Industry')['Liquidity_Ratio'].mean().reset_index()

# Mostrar resultados filtrados
st.write("Resultados Filtrados:")
st.dataframe(filtered_data)

# Gráficos
st.header("Gráficos de Ratios Financieros")

# Gráfico de Ratios de Liquidez por Industria
plt.figure(figsize=(10, 5))
sns.barplot(data=liquidity_summary, x='Industry', y='Liquidity_Ratio')
plt.title('Ratio de Liquidez Promedio por Industria')
plt.xticks(rotation=45)
st.pyplot(plt)

# Gráfico de Deuda a Patrimonio (Gráfico de pastel por Company_Size)
debt_summary = filtered_data.groupby('Company_Size')['Debt_to_Equity_Ratio'].mean().reset_index()
plt.figure(figsize=(8, 8))
plt.pie(debt_summary['Debt_to_Equity_Ratio'], labels=debt_summary['Company_Size'], autopct='%1.1f%%', startangle=140)
plt.title('Ratio de Deuda a Patrimonio Promedio por Tamaño de Empresa')
st.pyplot(plt)

# Gráfico de Cobertura de Gastos Financieros (Gráfico de líneas por País)
coverage_summary = filtered_data.groupby(['Country', 'Company_ID'])['Financial_Expenses_Coverage'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=coverage_summary, x='Company_ID', y='Financial_Expenses_Coverage', hue='Country', marker='o')
plt.title('Cobertura de Gastos Financieros por País')
plt.xticks(rotation=45)
st.pyplot(plt)

# Finalización
st.write("Análisis completo. ¡Gracias por usar esta herramienta!")
