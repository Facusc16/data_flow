# 🎶 Data & Flow

Este proyecto se encarga de la limpieza y exploración de datos de un dataset de canciones de Spotify, para explorar las principales medidas estadísticas mediante visualizaciones y aprovechar su información para el modelado de un modelo predictivo de clasificación de los géneros de las canciones.

## 📊 Dataset
Los datos provienen de Kaggle, y fueron completados mediante la API de Spotify.
Incluyen información de canciones como:
- Metadata (Nombre, Artista, duración, género, album, fecha de lanzamiento)
- Cualidades (danceability, positiveness, speechiness)
- Afinidad a contextos (party, driving, exercise, etc)
- Atributos de audio (key, tempo, loudness, time signature)
- Similitudes con otras canciones y artistas

## 🛠️ Requisitos

Este proyecto está desarrollado en **Python 3.11** y utiliza las siguientes librerías principales:
- pandas
- numpy
- matplotlib
- scikit-learn
- spotipy
- joblib

Puedes instalarlas ejecutando:

```bash
pip install -r requirements.txt
```

## 🚀 Uso

Para ejecutar el análisis abre el notebook principal:

```bash
jupyter notebook data_and_flow.ipynb
```

En el notebook encontrarás:
- Preprocesamiento y limpieza de los datos
- Análisis exploratorio con visualizaciones  
- Entrenamiento y evaluación del modelo de clasificación (Random Forest)

## 📈 Resultados

- Ranking de canciones y artístas que transmiten más flow.
- Clasificación de canciones según distintas categorías (Ejercicio, conducción, etc.)
- Cantidad de canciones por año y género 
- Modelo de clasificación de géneros musicales (Random Forest) con:
  - Métricas: *accuracy*, *precision*, *recall*, *F1-score*  
  - Matriz de confusión y análisis de features importantes.

## 🚧 Futuro trabajo

- Probar otros algoritmos de clasificación (XGBoost, SVM, redes neuronales).  
- Mejorar selección/ingeniería de características (feature engineering).
- Integración en tiempo real con la API de Spotify para inferencia en nuevas canciones.  

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.
