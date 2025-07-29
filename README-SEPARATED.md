# Flask Auth System - Django + React

This project has been separated into a Django REST API backend and a React frontend.

## Project Structure

```
flask-auth-system/
├── backend/           # Django REST API
│   ├── manage.py
│   ├── requirements.txt
│   ├── backend/       # Django project settings
│   └── authentication/  # Django app
└── frontend/          # React application
    ├── package.json
    ├── public/
    └── src/
```

## Setup Instructions

### Backend (Django API)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Copy .env file and update with your settings
cp .env.example .env
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Start the Django development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### Frontend (React)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout
- `GET /api/profile/` - Get user profile
- `POST /api/change-password/` - Change password
- `POST /api/forgot-password/` - Forgot password
- `GET /api/health/` - Health check

## Features

### Backend (Django)
- Django REST Framework API
- Custom User model with email login
- Session-based authentication
- CORS support for React frontend
- Password validation
- Admin interface

### Frontend (React)
- React Router for navigation
- Context API for state management
- Bootstrap for styling
- Axios for API calls
- Protected routes
- Form validation
- Responsive design

## Development

### Backend Development
- API runs on `http://localhost:8000`
- Admin interface: `http://localhost:8000/admin/`
- API documentation can be added with DRF browsable API

### Frontend Development
- React app runs on `http://localhost:3000`
- Hot reloading enabled
- Proxy configured to backend API

## Production Deployment

### Backend
- Use production WSGI server (Gunicorn)
- Configure production database (PostgreSQL)
- Set up proper environment variables
- Configure static files serving

### Frontend
- Build React app: `npm run build`
- Serve static files from build directory
- Configure proper API endpoints for production

## Key Changes from Flask

1. **Authentication**: Uses Django's built-in authentication system
2. **API Structure**: RESTful API with Django REST Framework
3. **Database**: Django ORM instead of SQLAlchemy
4. **Frontend**: Separate React application instead of Flask templates
5. **State Management**: React Context API for authentication state
6. **Routing**: React Router for client-side routing

## Benefits of This Architecture

- **Separation of Concerns**: Backend and frontend are completely separate
- **Scalability**: Can scale backend and frontend independently
- **Technology Flexibility**: Can easily swap frontend or backend technologies
- **Mobile Ready**: Same API can serve mobile applications
- **Development Efficiency**: Teams can work on frontend and backend simultaneously
