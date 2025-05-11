import requests
import pandas as pd
import time
import io
from urllib.parse import quote
from datetime import datetime, timedelta


""" EXPLICACIÓN CÓDIGO PRIMERA PARTE
Gdelts es una base de datos pública de noticias y eventos globales. Los datos obtenidos fueron a partir de queries a la API 
de Gdelt, que permite filtrar por temas, dominios y fechas.
Los parámetros fijos se configuraron para obtener noticias en español, originarias de colombia, que fueran artículos de noticias.
Los parámetros configurables son el tema, el dominio y el rango de fechas; se editaron para obtener una buena cantidad de noticias 
de diferentes medios, manteniendo el propósito de la investigación. Se justifica abajo el criterio de la selección de las variables
de los parámetros; cabe mencionar que en todos hubo una consideración computacional, pues aumentar variables aumentaba considerablmente
el tiempo de ejecución, por lo cual se decidio acotar.

- Tema: son opciones dadas por la API, lo cual limitó también la selección. Seleccionamos estos dado que son bastante posibles de ser 
        polarizados, eliminando otros que no, como deportes, cultura, ocio, entre otros.
- Dominio: se seleccionaron medios colombianos que fueran influyentes en el país. Algunos no pudieron obteneres (resalta la ausencia de caracol),
        pero los presentes son igualmente relevantes.
- Fechas: se seleccionaron fechas de 2024, pues son noticias suficientemente recientes para ser relevantes, pero suficientemente antiguas 
        para poder obtener sus datos (noticias muy recientes requieren subscripciones o están muy protegidas)
        También mencionar que las iteraciones se hacen por cada mes, pues la API retorma máximo 250 registros por query, entonces rangos de 
        tiempo muy largos podían dejar muchas noticias importantes fuera por este detalle técnico.
        
Finalmente mencionar 2 cosas. Primero, se puede demorar en cargar porque se establce un delay de 3 segundos entre cada query para evitar 
el error 429 (demasiadas peticiones), y segundo, se busca no repetir noticias, por ende se compara el URL de  las noticias obtenidas con las ya vistas,
antes de guardarlas, así solo se guardan nuevas, lo que también demora la ejecución.

"""


# Parámetros configurables
theme  = ["EPU_ECONOMY", "USPEC_POLITICS_GENERAL1", "UNGP_POLITICAL_FREEDOMS", "POLITICAL_TURMOIL", "EPU_POLICY_POLITICAL", "WB_2462_POLITICAL_VIOLENCE_AND_WAR"]
domain = ['eltiempo.com','elespectador.com', 'noticiasrcn.com', 'semana.com', 'pulzo.com', 'larepublica.co', 'lasillavacia.com'] 
#elcolombiano.com, wradio.com, vanguardia.com
start = ['20220101000000', '20220201000000', '20220301000000', '20220401000000', '20220501000000', '20220601000000', '20220701000000', '20220801000000', '20220901000000', '20221001000000', '20221101000000', '20221201000000'] 
end = ['20220103000000', '20220228000000', '20220330000000', '20220430000000', '20220530000000', '20220630000000', '20220703000000', '20220830000000', '20220930000000', '20221030000000', '20221130000000', '20221230000000'] 
output_csv = 'gdelt_colombia_politica.csv'

# Variables internas
base_url = 'https://api.gdeltproject.org/api/v2/doc/doc'
seen_urls = set()  # para evitar duplicados|
all_data = []

https://api.gdeltproject.org/api/v2/doc/doc?query=colombia AND domain:pulzo.com AND sourcelang:spanish AND sourcecountry:colombia&startdatetime=20220101000000&enddatetime=20221230000000&mode=ArtList&format=html&maxrecords=250

def construir_url(theme, domain, start, end):
    a = f"{base_url}?query=colombia AND theme:{theme} AND domain:{domain} AND sourcelang:spanish AND sourcecountry:colombia&startdatetime={start}&enddatetime={end}&mode=ArtList&format=csv&maxrecords=250"
    print(f"URL construida: {a}")
    return a


def extraer_y_guardar(theme, domain, start, end):
    global all_data

    url = construir_url(theme, domain, start, end)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 429:
            print("Demasiadas peticiones, esperando 60 segundos...")
            time.sleep(60)
            return
        elif r.status_code != 200:
            print(f"Error {r.status_code}: {r.text}")
            return

        df = pd.read_csv(io.StringIO(r.text))
        nuevos = df[~df['URL'].isin(seen_urls)]
        print(f"{len(nuevos)} noticias nuevas")

        seen_urls.update(nuevos['URL'])
        all_data.append(nuevos)

        # Guardar al CSV de forma acumulativa
        if not nuevos.empty:
            nuevos.to_csv(output_csv, mode='a', index=False, header=not pd.io.common.file_exists(output_csv))

    except Exception as e:
        print("Error al procesar:", e)
        
# Bucle para iterar sobre los parámetros
for i in range(len(theme)):
    for j in range(len(domain)):
        for k in range(len(start)):
            print(f"\n Iteración {theme[i]}, {domain[j]}, {start[k]}, {end[k]}")
            
            # Ajustar el rango de fechas dinámicamente
            extraer_y_guardar(theme[i], domain[j], start[k], end[k])
            time.sleep(1)  # Evitar error 429


# Unir todo
if all_data:
    full_df = pd.concat(all_data, ignore_index=True)
    print(f"\n Total artículos únicos obtenidos: {len(full_df)}")
else:
    print("\n No se obtuvo ningún dato.")



