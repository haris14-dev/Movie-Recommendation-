from django.shortcuts import render
from django.http import JsonResponse
from .utils.recommender import load_data, suggest_movies, recommend_movies
from .utils.tmdb import get_tmdb_poster, get_tmdb_poster_quick  # your TMDB poster functions
import threading
import os

# Simple in-memory caches for posters and suggestions
poster_cache = {}
suggestions_cache = {}

# Load movie stats once at startup
movie_stats = load_data()

def home(request):
    return render(request, "index.html")

def get_suggestions(request):
    query = request.GET.get("query", "").strip().lower()
    # check cache first
    if query in suggestions_cache:
        return JsonResponse({"suggestions": suggestions_cache[query]})
    suggestions = suggest_movies(movie_stats, query)
    # cache for future requests
    suggestions_cache[query] = suggestions
    return JsonResponse({"suggestions": suggestions})

def get_recommendations(request):
    movie_name = request.GET.get("movie", "")
    recs = recommend_movies(movie_stats, movie_name)
    
    # Convert to list of dicts
    recs = recs.reset_index().to_dict(orient="records")
    
    # For faster responses: return a placeholder immediately for uncached posters
    # and fetch/save the real poster in a background thread so future requests are fast.
    def _fetch_and_cache(title):
        try:
            url = get_tmdb_poster(title)
            poster_cache[title] = url
        except Exception:
            poster_cache[title] = "https://via.placeholder.com/185x278?text=No+Image"

    for movie in recs:
        title = movie.get('title')
        if title in poster_cache:
            movie['poster_url'] = poster_cache[title]
            continue

        # not cached: return immediate TMDB CDN URL (fast) and start background local save
        quick_url = get_tmdb_poster_quick(title)
        movie['poster_url'] = quick_url
        # start background fetch thread to download and cache a local thumbnail
        t = threading.Thread(target=_fetch_and_cache, args=(title,), daemon=True)
        t.start()
    
    return JsonResponse({"recommendations": recs})


def get_poster_status(request):
    """Return poster URL from cache or filesystem if available for a given title."""
    title = request.GET.get('title', '')
    if not title:
        return JsonResponse({'poster_url': ''})

    # check in-memory cache first
    if title in poster_cache:
        return JsonResponse({'poster_url': poster_cache[title]})

    # check filesystem
    try:
        # rebuild safe file name used by tmdb.download logic
        safe_name = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')[:60]
        posters_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'images', 'posters'))
        local_path = os.path.join(posters_dir, f"{safe_name}.jpg")
        if os.path.exists(local_path):
            web_path = f"/static/images/posters/{os.path.basename(local_path)}"
            # store in cache for quicker future responses
            poster_cache[title] = web_path
            return JsonResponse({'poster_url': web_path})
    except Exception:
        pass

    return JsonResponse({'poster_url': ''})
