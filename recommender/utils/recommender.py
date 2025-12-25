import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import urllib.request
import zipfile


def load_data():
    """Load and preprocess the MovieLens dataset, perform clustering."""
    url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    zipname = "ml-latest-small.zip"

    # Download dataset if not present
    if not os.path.exists(zipname):
        urllib.request.urlretrieve(url, zipname)
    if not os.path.exists("ml-latest-small"):
        with zipfile.ZipFile(zipname, "r") as z:
            z.extractall(".")

    # Load CSVs
    movies = pd.read_csv("ml-latest-small/movies.csv")
    ratings = pd.read_csv("ml-latest-small/ratings.csv")

    # One-hot encode genres
    genre_dummies = movies["genres"].str.get_dummies(sep="|")
    movies = pd.concat([movies, genre_dummies], axis=1)

    # Compute movie statistics
    movie_stats = ratings.groupby("movieId")["rating"].agg(["mean", "count"]).reset_index()
    movie_stats = movie_stats[movie_stats["count"] >= 20]  # filter movies with <20 ratings
    movie_stats = pd.merge(movie_stats, movies, on="movieId", how="left")

    # Standardize features
    scaler = StandardScaler()
    X = scaler.fit_transform(movie_stats[["mean", "count"] + list(genre_dummies.columns)])

    # KMeans clustering
    kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
    movie_stats["Cluster"] = kmeans.fit_predict(X)

    # Set index for easy lookup
    movie_stats.set_index("title", inplace=True)

    return movie_stats


def suggest_movies(movie_stats, query, max_suggestions=10):
    """
    Returns a list of movie titles that match the query (case-insensitive, partial match)
    """
    if not query:
        return []
    query = query.lower()
    suggestions = [title for title in movie_stats.index if query in title.lower()]
    return suggestions[:max_suggestions]


def recommend_movies(movie_stats, movie_name, top_n=10):
    """
    Given a movie name, return top_n similar movies based on cluster and average rating.
    """
    if movie_name not in movie_stats.index:
        return []

    cluster = movie_stats.loc[movie_name, "Cluster"]
    similar_movies = (
        movie_stats[movie_stats["Cluster"] == cluster]
        .sort_values("mean", ascending=False)
        .drop(movie_name, errors="ignore")
        .head(top_n)
    )
    return similar_movies[["mean", "count"]]
