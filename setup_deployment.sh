#!/bin/bash
# Quick deployment setup script for Linux/Mac
# Run: bash setup_deployment.sh

echo "🚀 Movie Recommender - Deployment Setup Script"
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check Python version
echo -e "${BLUE}[1/6]${NC} Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python $python_version found"

# 2. Install dependencies
echo -e "${BLUE}[2/6]${NC} Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Dependencies installed"

# 3. Create environment file
echo -e "${BLUE}[3/6]${NC} Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠${NC} .env file created - IMPORTANT: Edit it with your settings!"
    echo "   - Generate SECRET_KEY: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
    echo "   - Set DEBUG=False"
    echo "   - Set ALLOWED_HOSTS to your domain(s)"
else
    echo -e "${GREEN}✓${NC} .env file already exists"
fi

# 4. Run migrations
echo -e "${BLUE}[4/6]${NC} Running database migrations..."
python manage.py migrate --noinput > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Migrations complete"

# 5. Collect static files
echo -e "${BLUE}[5/6]${NC} Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Static files collected"

# 6. Test
echo -e "${BLUE}[6/6]${NC} Testing setup..."
python manage.py check > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All checks passed!"
else
    echo -e "${YELLOW}⚠${NC} Some checks failed - see above"
fi

echo ""
echo "================================================"
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your settings:"
echo "   nano .env"
echo ""
echo "2. Choose a deployment option:"
echo "   - Heroku: See DEPLOYMENT.md (Option 1)"
echo "   - Docker: See DEPLOYMENT.md (Option 2)"
echo "   - AWS/VPS: See DEPLOYMENT.md (Option 3)"
echo ""
echo "3. Test locally before deployment:"
echo "   DEBUG=False python manage.py runserver"
echo ""
echo "Full documentation: See DEPLOYMENT.md and README.md"
echo "================================================"
