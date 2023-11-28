from fastapi import FastAPI
import pandas as pd
from fastapi.responses import HTMLResponse
from collections import defaultdict
import numpy as np
import pickle

df_user_data=pd.read_csv('datasetAPI/df_user_data.csv')
df_count_reviews=pd.read_csv('datasetAPI/df_count_reviews.csv')
df_user_genre=pd.read_csv('datasetAPI/users_playtime_genre.csv')
df_developer=pd.read_csv('datasetAPI/df_developer.csv')
sentiment=pd.read_csv('datasetAPI/df_sentiment_analysis.csv')
gustos_predichos_df=pd.read_csv('datasetAPI/Matriz_recomendaciones.csv')
itemsforuser=pd.read_csv('datasetAPI/itemsforuser.csv')
most_played=pd.read_csv('datasetAPI/most_played_games.csv')

with open('dataset/id_to_game_dict', 'rb') as archivo:
    id_to_game = pickle.load(archivo)

with open('dataset/id_to_genre_dict', 'rb') as archivo:
    id_to_genre = pickle.load(archivo)


app=FastAPI()

@app.get('/')
def message():
    return 'Hello World'

@app.get('/userdata/{user_id}')
def userdata(user_id: str):
    df = df_user_data.loc[df_user_data['user_id'] == f'{user_id}']
    if df.empty:
        return "No se encontro ningun usuario con ese id, por favor introduce un id válido."
    
    df=df.rename(columns={'recommend': 'porcentaje de recomendacion',
                 'items_count': 'total items', 'total_spent':'total gastado'})
    
    table_html = df.to_html(classes='table table-striped', index=False, escape=False)

    response_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tabla datos del usuario</title>
    </head>
    <body>
        <h1>Tabla datos del usuario: {user_id}</h1>
        {table_html}
    </body>
    </html>
    """

    return HTMLResponse(content=response_html, status_code=200)

@app.get('/countreviews/{fechas}')
def countreviews(fechas: str):
    fecha_inicio=fechas.split('y')[0]
    fecha_fin=fechas.split('y')[1]
    df_count_reviews['date'] = pd.to_datetime(df_count_reviews['date'])
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Filtrar el DataFrame para el rango de fechas deseado
    df_rango = df_count_reviews[(df_count_reviews['date'] >= fecha_inicio) & (df_count_reviews['date'] <= fecha_fin)]
    
    return [len(df_rango['user_id'].unique()) ,round(df_rango['recommend'].mean()*100, 2)]

@app.get('/genre/{genero}')
def genre(genero:str):
    df=df_user_genre.groupby('game_genre')['playtime'].sum().reset_index()
    df=df.sort_values('playtime', ascending=False).reset_index().drop(columns='index')
    position = df[df['game_genre'] == genero].index[0] + 1 if genero in df['game_genre'].values else None
    
    return f'El genero {genero} se encuentra en la posición {position} de los generos mas jugados'

@app.get('/userforgenre/{genero}')
def userforgenre( genero : str ):
    df = df_user_genre.loc[df_user_genre['game_genre'] == f'{genero}'].sort_values('playtime', ascending=False).reset_index().drop(columns='index')
    df=df[['user_id','user_url', 'playtime']].head(5)
    
    table_html = df.to_html(classes='table table-striped', index=False, escape=False)

    # Crear una respuesta HTML que contiene la tabla
    response_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tabla de usuarios por género</title>
    </head>
    <body>
        <h1>Tabla de usuarios por género: {genero}</h1>
        {table_html}
    </body>
    </html>
    """
    
    return HTMLResponse(content=response_html, status_code=200)

@app.get('/developer/{desarrollador}')
def developer(desarrollador: str):
    try: 
        desarrollador=desarrollador
        desarrollador_lower = desarrollador.lower()
        df = df_developer.loc[df_developer['developer'] == f'{desarrollador_lower}'].sort_values('year')
        df=df.drop_duplicates()
        yearB = 0
        dict_años = defaultdict(list)  # Changed the dictionary value type to list
        items = 0
        items_free=0
        for index, row in df.iterrows():
            year = row['year']
            price = row['price']
            if  year != yearB:
                items = 0  # Restablece la cuenta de elementos si es un nuevo año
                yearB = year
                items_free=0
                
            if price == 0.00:
                items_free+=1
                dict_años[year] = [f'{items_free}', items] 
            else:
                items += 1
                dict_años[year] = [f'{items_free}', items]
        texto=' Free content %'

        df = pd.DataFrame(dict_años.values(), dict_años.keys()).rename(columns={0:f'{desarrollador}{texto}', 1: 'lanzamientos ese año'})
        df['año'] = df.index
        df = df[['año', f'{desarrollador}{texto}', 'lanzamientos ese año']]
        df[f'{desarrollador}{texto}']= round((pd.to_numeric(df[f'{desarrollador}{texto}']) / df['lanzamientos ese año']*100), 2)
        
        table_html = df.to_html(classes='table table-striped', index=False, escape=False)

        # Crear una respuesta HTML que contiene la tabla
        response_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tabla resumen del desarrollado</title>
        </head>
        <body>
            <h1>Tabla resumen del desarrollador: {desarrollador}</h1>
            {table_html}
        </body>
        </html>
        """
    
        return  HTMLResponse(content=response_html, status_code=200)
    except KeyError:
        raise HTTPException(status_code=404, detail=f'Desarrollador "{desarrollador}" no encontrado')


@app.get('/sentimentanalysis/{anio}', name="sentiment_analysis")
def sentiment_analysis(anio: int):
    # Copia el DataFrame 'sentiment' para evitar modificar el original
    df = sentiment.copy()
    
    # Filtra el DataFrame para obtener las reseñas del año especificado
    filtered_df = df[df['año_lanzamiento'] == anio]['review']
    
    if not filtered_df.empty:
        # Cuenta la cantidad de reseñas positivas (2), negativas (0) y neutras (1)
        positivo = filtered_df.iloc[0].count('2')
        negativo = filtered_df.iloc[0].count('0')
        neutro = filtered_df.iloc[0].count('1')
        
        # Devuelve un mensaje con los resultados del análisis de sentimiento
        return f'Negative = {negativo}, Neutral = {neutro}, Positive = {positivo}'
    else:
        # Devuelve un mensaje si no hay reseñas para el año especificado
        return 'No hay reseñas para este año de lanzamiento'
    
    
@app.get('/recomendacionusuario/{user_id}')
def recomendacion_usuario(user_id):
    try:
        # Obtener las predicciones para el usuario
        predicciones = gustos_predichos_df.set_index('user_id').loc[user_id]

        # Obtener los 10 géneros principales según las predicciones
        top_generos = list(np.abs(predicciones).sort_values(ascending=False).index[:10])

        # Obtener los juegos comprados por el usuario
        juegos_comprados = itemsforuser[itemsforuser['user_id'] == user_id]['item_id'].values[0]

        # Inicializar la lista de juegos recomendados
        juegos_recomendados = []
        contador = 0

        # Iterar a través de los géneros principales
        for genero in top_generos:
            for index, row in most_played.iterrows():
                item_id = row['item_id']
                genero_item = id_to_genre.get(item_id, '')

                # Verificar si el juego pertenece al género actual y aún no se ha agregado
                if genero in genero_item and item_id not in juegos_recomendados:
                    juegos_recomendados.append(item_id)
                    contador += 1

                # Salir del bucle si se han encontrado 3 juegos para este género
                if contador == 3:
                    break
            contador = 0

        # Remover juegos que el usuario ya tiene
        juegos_recomendados = [juego for juego in juegos_recomendados if juego not in juegos_comprados]

        # Obtener los 5 mejores juegos recomendados
        top_5_juegos = juegos_recomendados[:5]

        # Obtener los nombres de los juegos a partir de sus IDs
        for i, id in enumerate(top_5_juegos):
            top_5_juegos[i] = id_to_game.get(id, '')

        return top_5_juegos

    except KeyError:
        # Manejar el caso en el que no se encuentra el user_id
        return f'Usuario con ID {user_id} no encontrado'