import csv
""" EXPLICACIÓN CÓGIDO CUARTA PARTE
Honestamente, esta parte fue por un error. En la parte anterior guardé mal los datos en el
csv, pues separé las columnsa por comas, pero no caí en cuenta que los textos también tienen
comas y por ende no se puede cargar bien los datos. Este texto precisamente arregla eso. 

"""


# Archivo de entrada y salida
input_csv = "../noticias_completas.csv"
output_csv = "../noticias_completas_final.csv"

# Leer el archivo original y escribirlo con el nuevo delimitador
with open(input_csv, mode="r", encoding="utf-8") as infile, open(output_csv, mode="w", encoding="utf-8", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, delimiter="~", quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        try:
            # Unir la fila original en una cadena para procesarla
            line = ",".join(row)

            # Extraer URL
            sep1 = line.find(",")
            url = line[:sep1].strip()
            line = line[sep1 + 1:]

            # Extraer fecha
            sep2 = line.find(",")
            fecha = line[:sep2].strip()
            line = line[sep2 + 1:]

            # Extraer título y texto
            if line.startswith('"'):
                sep3 = line.find('"', 1)  # Buscar el cierre del título
                titulo = line[1:sep3].strip()
                line = line[sep3 + 2:]  # Saltar la coma después del título
            else:
                sep3 = line.find(",")
                titulo = line[:sep3].strip()
                line = line[sep3 + 1:]

            texto = line.strip('"')  # Eliminar comillas externas del texto

            # Escribir la línea reformateada
            writer.writerow([url, fecha, titulo, texto])

        except Exception as e:
            print(f"Error procesando la fila: {row}. Error: {e}")

print(f"Archivo reformateado guardado en: {output_csv}")