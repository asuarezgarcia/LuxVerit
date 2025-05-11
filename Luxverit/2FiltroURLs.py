
import csv
import sys

""" EXPLICACIÓN CÓDIGO SEGUNDA PARTE

Aún con los filtros puestos en la API hay algunas noticias que no se ajustan a lo que se busca, por lo cual se hace un filtrado adicional
en el dataframe final. Este filtro es más personalizado, tomando la URL y eliminando palabras clave que irrelevantes para nuestra
investigación. 

*NOTA: este código se separa del archivo "Gdelt" para poder limpiar los datos sin necesidad de cargarlos todos otra vez. 

"""

# Configurar la salida estándar para usar UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Archivo de entrada y salida
input_csv = 'gdelt_colombia_politica.csv'
output_csv = 'gdelt_colombia_politica_filtrado.csv'

# Palabras clave para filtrar
keywords = ["deportes", "entretenimiento", "tendencias", "bocas", "estilo de vida", "vivir-bien/", "gente/", "/ocio"]

contador = 0

# Abrir el archivo de entrada y salida
with open(input_csv, mode='r', encoding='utf-8') as infile, open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Leer y escribir el encabezado (sin la columna 1)
    header = next(reader)
    writer.writerow([col for i, col in enumerate(header) if i != 1])

    # Procesar cada fila
    for row in reader:
        url = row[0]  # Columna 0: URL
        title = row[3]  # Columna 3: Descripción

        # Verificar si la fila contiene alguna palabra clave
        url_matches = [keyword for keyword in keywords if keyword.lower() in url.lower()]
        title_matches = [keyword for keyword in keywords if keyword.lower() in title.lower()]

        if url_matches or title_matches:
            print(f"Eliminando fila: {repr(row)}")  # Usar repr para evitar problemas de Unicode
            print(f"Coincidencias en URL: {url_matches}")
            print(f"Coincidencias en Descripción: {title_matches}")
            contador += 1
        else:
            # Escribir la fila filtrada (sin la columna 1)
            writer.writerow([col for i, col in enumerate(row) if i != 1])

print(f"Archivo filtrado guardado en: {output_csv}")
print(f"Total de filas eliminadas: {contador}")