# Standard Library
import json
import logging
import re
import time

# Third-party Libraries
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
from requests.exceptions import RequestException
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials


# Lidiar con NaNs
def fill_values(df, name, song, columns):

    for col_artist, col_song in columns:

        rows = (df[col_artist].apply(lambda x: any(a in name for a in x.split(','))) &
                (df[col_song].isna()))

        df.loc[rows, col_song] = song

    return df


class RateLimitReached(Exception):  # Ecxepción personalziada
    pass


class RatelimitHandler(logging.Handler):  # Handler personalizado

    # Método para procesar y manejar cada mensaje de log
    def emit(self, record):

        # Obtener mensaje del log
        msg = record.getMessage()

        # Verificar si es el mensaje que buscamos
        if "yyour application has reached a rate/request limit" in msg.lower():

            # Establecer mensaje a mostrar y detener ejecución del código
            match = re.search(r"after: (\d+)", msg)
            if match:
                retry_seconds = int(match.group(1))
                hours = retry_seconds // 3600
                minutes = (retry_seconds % 3600) // 60
                raise RateLimitReached(
                    f"Se alcanzó el límite de peticiones. Volver a ejecutar después de {hours}h. {minutes}min.")


def setup_rate_limit_logging():

    logger = logging.getLogger()  # Obtener el logger raíz
    logger.propagate = False  # Evitar que los mensajes se propaguen a otros handlers
    logger.addHandler(RatelimitHandler())  # Agregar handler personalizado
    logger.setLevel(logging.WARNING)  # Establecer nivel de log


def get_album_date(sp, artist, album, retries=3, delay=1):

    for attempt in range(retries):
        try:

            query = f"album:{album} artist:{artist}"
            results = sp.search(query, type='album', limit=1)

            items = results['albums']['items']
            if items:
                return items[0]['release_date']
            return None

        except (RequestException, SpotifyException) as e:

            if isinstance(e, SpotifyException) and e.http_status == 429:

                retry_after = int(e.headers.get('Retry-After', 0))
                hours = retry_after // 3600
                minutes = (retry_after % 3600) // 60
                clear_output(wait=True)
                raise RateLimitReached(
                    f"Se alcanzó el límite de peticiones. Volver a ejecutar después de {hours}h. {minutes}min.") from e

            else:
                clear_output(wait=True)
                print(
                    f"Error in the request ({e}). Retrying ({attempt + 1}/{retries})...")
                time.sleep(delay)

    return None


def get_album_release_dates(client_id, client_secret, release_dates_data, empty_dates, cache_file):

    auth_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    count = 0
    for i, row in empty_dates.iterrows():
        key = f"{row['artists']}||{row['album']}"

        if key not in release_dates_data:
            count += 1
            release_dates_data[key] = get_album_date(
                sp, row['artists'], row['album'])

            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(release_dates_data, f, ensure_ascii=False, indent=2)

            time.sleep(0.1)

        if count % 1000 == 0 and count != 0:
            clear_output(wait=True)
            print(f"Procesados {count} albumes...")

    return release_dates_data


# Visualización de datos
def get_top(df, column, filter, new_column, qualities, limit, filters):
    top = df[df[column] == filter].copy()
    top[new_column] = top[qualities].mean(axis=1)
    return top[filters].sort_values(by=new_column, ascending=False).head(limit)


# Gráficos
def tops(songs, labels, ticks=False):
    fig = plt.figure(figsize=(10, 5))

    cols = songs.columns

    plt.bar(songs[cols[0]],
            songs[cols[1]],
            edgecolor='black')

    plt.title(labels['title'])
    plt.ylabel(labels['y'])
    plt.ylim(labels['ylim'])

    if ticks:
        plt.xticks(rotation=-45,
                   ha='left')

    plt.show()


def song_genres_by_year(year_genre, genre_groups):
    fig, axes = plt.subplots(3, 2, figsize=(18, 18))
    axes = axes.flatten()

    for ax, (group, genres) in zip(axes, genre_groups.items()):
        valid_genres = [g for g in genres if g in year_genre.columns]

        if not valid_genres:
            ax.set_visible(False)
            continue

        subset = year_genre[valid_genres]
        bottom = np.zeros(len(subset))

        for genre in subset.columns:
            ax.bar(subset.index,
                   subset[genre],
                   bottom=bottom)
            bottom += subset[genre]

        ax.set_title(group)
        ax.set_xlabel('Año')
        ax.set_ylabel('Cantidad de canciones')
        ax.legend(valid_genres, title='Géneros')

    max_y = year_genre.sum(axis=1).max()
    for ax in axes:
        ax.set_ylim(0, max_y)

    fig.suptitle(
        'Cantidad de canciones por género a lo largo del tiempo', fontsize=18)
    plt.tight_layout()
    plt.show()


def main():
    pass


if __name__ == "__main__":
    main()
