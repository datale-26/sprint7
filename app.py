# Traigo las cosas que necesito para mi app
import streamlit as st  # Esto es para hacer la página web
import pandas as pd  # Esto lee mi archivo csv
import plotly.express as px  # Esto hace los gráficos

# Leo mi archivo de datos
car_data = pd.read_csv('vehicles_us.csv')


# Voy a sacar el fabricante de la columna model (la primera palabra)
car_data['manufacturer'] = car_data['model'].str.split().str[0]
# Hago todo en minúsculas para que se vea mejor
car_data['manufacturer'] = car_data['manufacturer'].str.lower()

# Pongo un título grande en mi app
st.title("Mi Tablero de Carros")

# Sección 1: Mostrar los datos en una tabla
st.header("Ver Datos")  # Esto es un encabezado
# Hago un checkbox para elegir si mostrar fabricantes pequeños
mostrar_pequeños = st.checkbox("Incluir fabricantes con menos de 1000 anuncios", value=True)
# Si el checkbox está marcado, muestro todos los datos
if mostrar_pequeños:
    datos_filtrados = car_data
else:
    # Cuento cuántos anuncios tiene cada fabricante
    conteo_fabricantes = car_data['manufacturer'].value_counts()
    # Solo muestro fabricantes con 1000 o más anuncios
    datos_filtrados = car_data[car_data['manufacturer'].isin(conteo_fabricantes[conteo_fabricantes >= 1000].index)]
# Muestro la tabla con algunas columnas
st.dataframe(datos_filtrados[['price', 'model_year', 'model', 'manufacturer', 'condition', 'cylinders', 'fuel']])

# Sección 2: Comparar precios entre fabricantes
st.header("Comparar Precios de Fabricantes")
# Hago una lista de fabricantes para elegir
lista_fabricantes = sorted(car_data['manufacturer'].dropna().unique())
# Pongo dos cajitas para elegir fabricantes
fabricante1 = st.selectbox("Elige el fabricante 1", lista_fabricantes)
fabricante2 = st.selectbox("Elige el fabricante 2", lista_fabricantes)
# Checkbox para normalizar el gráfico
normalizar = st.checkbox("Hacer el gráfico normalizado", value=True)

# Si hay dos fabricantes elegidos, hago el gráfico
if fabricante1 and fabricante2:
    # Filtro los datos para solo esos dos fabricantes
    datos_filtro = car_data[car_data['manufacturer'].isin([fabricante1, fabricante2])]
    # Hago un histograma de precios
    grafico_precios = px.histogram(
        datos_filtro, x="price", color="manufacturer",
        histnorm='percent' if normalizar else None,  # Si está normalizado, uso porcentaje
        barmode='overlay',  # Para que los colores se superpongan
        nbins=50  # Pongo 50 barras para que se vea bien
    )
    # Muestro el gráfico
    st.plotly_chart(grafico_precios)

# Sección 3: Histograma de condición vs año del modelo
st.header("Condición vs Año del Modelo")
# Hago un histograma de model_year con colores por condición
grafico_condicion = px.histogram(car_data, x="model_year", color="condition")
# Muestro el gráfico
st.plotly_chart(grafico_condicion)

# Sección 4: Tipos de vehículos por fabricante
st.header("Tipos de Vehículos por Fabricante")
# Hago un histograma de fabricantes con colores por tipo de vehículo
grafico_tipos = px.histogram(car_data, x="manufacturer", color="type")
# Lo hago más grande para que se vea mejor
grafico_tipos.update_layout(height=400)
# Muestro el gráfico
st.plotly_chart(grafico_tipos)