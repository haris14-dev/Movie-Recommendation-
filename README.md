# Movie Recommender Application

A Django-based machine learning web application that recommends movies based on similarity analysis using the MovieLens dataset.

## Features

- 🎬 Search for movies by title
- 🤖 AI-powered movie recommendations
- 📊 Based on MovieLens dataset (ml-latest-small)
- 💨 Fast and responsive UI with modern styling
- 🎯 Uses scikit-learn clustering for recommendations

## Tech Stack

- **Backend:** Django 6.0
- **ML:** scikit-learn, pandas
- **Frontend:** HTML5, CSS3, JavaScript
- **Server:** Gunicorn
- **Database:** SQLite3

## Installation

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd movie_app
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Open http://localhost:8000 in your browser

## Deployment

### Heroku Deployment

1. **Install Heroku CLI:**
   ```bash
   npm install -g heroku
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

6. **Open the app:**
   ```bash
   heroku open
   ```

### Manual Server Deployment

1. **Install dependencies on server:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env file:**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Run with Gunicorn:**
   ```bash
   gunicorn backend.wsgi --bind 0.0.0.0:8000
   ```

## Project Structure

```
movie_app/
├── backend/              # Django project settings
│   ├── settings.py      # Main configuration
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI application
│   └── asgi.py          # ASGI application
├── recommender/         # Django app
│   ├── utils/
│   │   └── recommender.py  # ML recommendation logic
│   ├── templates/
│   │   └── index.html      # Frontend template
│   ├── views.py         # API views
│   └── urls.py          # App URLs
├── static/              # Static files (CSS, JS)
├── ml-latest-small/     # MovieLens dataset (auto-downloaded)
├── manage.py            # Django CLI
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku deployment config
└── README.md           # This file
```

## API Endpoints

### GET `/` 
Home page with search interface.

### GET `/api/suggestions/?query=<search_term>`
Get movie suggestions based on search query.

**Response:**
```json
{
  "suggestions": ["Movie 1", "Movie 2", ...]
}
```

### GET `/api/recommendations/?movie=<movie_name>`
Get recommended movies based on selected movie.

**Response:**
```json
{
  "recommendations": [
    {
      "title": "Movie Title",
      "mean": 3.75,
      "count": 100
    },
    ...
  ]
}
```

## Dataset

The application uses the **MovieLens Small Dataset** which includes:
- 100,836 ratings from 610 users on 9,742 movies
- Automatically downloaded on first run
- Located in `ml-latest-small/` directory

## Performance Notes

- First request may take longer as the ML model is trained on startup
- Data is loaded into memory for fast recommendations
- Suitable for small to medium-scale deployments

## Troubleshooting

### Template not found
Ensure `recommender` is in INSTALLED_APPS in settings.py

### Static files not loading
Run: `python manage.py collectstatic`

### ML model takes too long
The dataset download and model training happens on first run. Subsequent requests are fast.

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions, please create an issue in the repository.
