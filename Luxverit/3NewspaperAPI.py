import pandas as pd
from newspaper import Article

""" EXPLICACIÓN CODIGO TERCERA PARTE

En esta parte ya tenemos los urls de los artículos que deseamos analizar. Ahora usamos la API newspaper
para extraer el texto de cada uno de los artículos empleando la url. De cada texto se extraen los primeros 1000
caracteres, pues es una parte representativa del texto (especialemente la introducción resumen el contenido y la 
posición del autor), y cargar más para cada uno de los artículo tiene un gran costo computacional, no solo
para extraer el texto, también para el modelo de análisis posterior.

También nos dimos cuenta que la API extrae la mayor parte correctamente, pero a veces copia publicidad o propaganda,
por lo cual se hace un filtro adicional al texto para eliminar estos casos. Se agregaran 200 caracteres a los 1000
originales considerando aquellos que se eliminarán.

*NOTA: recomiendo usar el código de prueba para verificar el funcionamiento. El completo tardó 16 horas.

"""

# Cargar el CSV exportado de GDELT
df = pd.read_csv("gdelt_colombia_politica_filtrado.csv") 

# Ponerle titulo a las columnas del df
df.columns = ['url', 'fecha', 'titulo']

df_prueba = df.head(10)

print(f"columnas del df: {df.columns}")

# Extraer contenido de cada URL
def extraer_texto(url):
    try:
        articulo = Article(url, language='es')
        print("Descargando:", url) # esta línea es para ver el progreso, puede quitarse si es incómodo
        articulo.download()
        articulo.parse()
        articulo.text[:2500]  # Los primeros 2500 caracteres
        
        # Filtrar el texto para eliminar publicidad o propaganda
        # eliminar saltos de página 
        articulo.text = articulo.text.replace("\n", " ")
        # eliminar espacios dobles
        articulo.text = articulo.text.replace("  ", " ")
        # quitar promoción ElTiempo
        articulo.text = articulo.text.replace("Ingrese o regístrese acá para guardar los artículos en su zona de usuario y leerlos cuando quiera", "")
        
        
        return articulo.text[:1200]  # Retornar los primeros 1200 caracteres del texto
    except:
        print("Error al procesar la URL:", url)
        return ""

""" Prueba (esto se usó para probar que el código funcionara antes de aplicarlo a todas las noticias)

    # Extraer contenido de cada URL en el DataFrame de prueba
    df_prueba["texto"] = df_prueba["url"].apply(extraer_texto)

    # Guardar el resultado de prueba en un archivo separado
    df_prueba.to_csv("gdelt_con_texto_prueba.csv", index=False)

    print("Prueba completada. Resultado guardado en 'gdelt_con_texto_prueba.csv'")
    
"""

# Aplicarlo a todas las URLs
df["texto"] = df["url"].apply(extraer_texto)

# Guardar resultado
df.to_csv("noticias_completas.csv", index=False)
print("Prueba completada. Resultado guardado en 'gdelt_con_texto_prueba.csv'")

