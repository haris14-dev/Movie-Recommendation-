import requests
import re

API_KEY = "af539f0c4b00f30116be90a114677f86"

def clean_title_for_search(title):
    """Extract clean title and year from movie title like 'Movie Name (1999)'"""
    match = re.match(r'^(.+?)\s*\((\d{4})\)\s*$', title)
    if match:
        return match.group(1).strip(), match.group(2)
    return title.strip(), None

def get_tmdb_poster(movie_title):
    try:
        clean_title, year = clean_title_for_search(movie_title)
        
        # Search with year if available for better matching
        if year:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={clean_title}&year={year}"
        else:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={clean_title}"
        
        res = requests.get(url, timeout=3).json()
        results = res.get("results") or []

        # If no results with year, try without year
        if not results and year:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={clean_title}"
            res = requests.get(url, timeout=3).json()
            results = res.get("results") or []

        # pick best result with a poster
        best = None
        for r in results:
            if r and r.get("poster_path"):
                if not best or r.get("popularity", 0) > best.get("popularity", 0):
                    best = r

        if best:
            poster_path = best.get("poster_path")
            return f"https://image.tmdb.org/t/p/w342{poster_path}"

        return "https://via.placeholder.com/200x300?text=No+Poster"
    except Exception:
        return "https://via.placeholder.com/200x300?text=No+Poster"


def get_tmdb_poster_quick(movie_title):
    """Quick lookup: return TMDB image URL if available, without downloading."""
    try:
        clean_title, year = clean_title_for_search(movie_title)
        
        # Search with year if available
        if year:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={clean_title}&year={year}"
        else:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={clean_title}"
        
        res = requests.get(url, timeout=1.5).json()
        results = res.get("results") or []
        
        # If no results with year, try without
        if not results and year:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={clean_title}"
            res = requests.get(url, timeout=1.5).json()
            results = res.get("results") or []
        
        # Find best match by popularity
        best = None
        for r in results:
            if not r or not r.get("poster_path"):
                continue
            if not best or r.get("popularity", 0) > best.get("popularity", 0):
                best = r
        
        if best:
            return f"https://image.tmdb.org/t/p/w342{best.get('poster_path')}"
        return "https://via.placeholder.com/200x300?text=No+Poster"
    except Exception:
        return "https://via.placeholder.com/200x300?text=No+Poster"

