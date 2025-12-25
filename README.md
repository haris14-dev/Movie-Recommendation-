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
   git clone https://github.com/haris14-dev/Movie-Recommendation-.git
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
   - Open https://movie-recommender-ohes.onrender.com/

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
