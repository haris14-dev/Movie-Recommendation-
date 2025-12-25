from django.shortcuts import render
from django.http import JsonResponse
from .utils.recommender import load_data, suggest_movies, recommend_movies

movie_stats = load_data()

def home(request):
    return render(request, "index.html")

def get_suggestions(request):
    query = request.GET.get("query", "")
    suggestions = suggest_movies(movie_stats, query)
    return JsonResponse({"suggestions": suggestions})

def get_recommendations(request):
    movie_name = request.GET.get("movie", "")
    recs = recommend_movies(movie_stats, movie_name)
    recs = recs.reset_index().to_dict(orient="records")
    return JsonResponse({"recommendations": recs})
