# Spiritual Gifts Survey Application

A full-stack web application for digitizing and administering a spiritual gifts assessment survey. Built with Django REST Framework backend and Vue.js frontend.

## Features

- **120 Question Survey**: Complete spiritual gifts assessment with 8 questions per gift
- **15 Spiritual Gifts**: Prophecy, Serving, Teaching, Exhortation, Giving, Leadership, Mercy, Wisdom, Knowledge, Faith, Healing, Miracles, Discernment, Tongues, and Interpretation
- **Real-time Progress**: Visual progress bar showing completion status
- **Instant Results**: Automatic calculation and visualization of spiritual gift scores
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Data Persistence**: All responses stored in backend database
- **Results Analysis**: Percentage-based scoring with top 3 gifts highlighted

## Tech Stack

### Backend
- Django 4.2+
- Django REST Framework
- SQLite database
- CORS headers for API access

### Frontend
- Vue 3
- Vue Router
- Axios for API calls
- Vite build tool
- Modern CSS with responsive design

## Project Structure

```
spiritual-gifts/
├── backend/                    # Django backend
│   ├── spiritual_gifts/       # Django project settings
│   ├── survey/                # Survey app
│   │   ├── models.py         # Database models
│   │   ├── serializers.py    # API serializers
│   │   ├── views.py          # API views
│   │   ├── urls.py           # API routes
│   │   └── management/       # Management commands
│   ├── manage.py
│   └── requirements.txt
├── frontend/                   # Vue frontend
│   ├── src/
│   │   ├── views/            # Vue components
│   │   ├── App.vue           # Main app component
│   │   ├── main.js           # App entry point
│   │   ├── api.js            # API service
│   │   └── style.css         # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Populate the database** with questions:
   ```bash
   python manage.py populate_data
   ```

6. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

   The backend API will be available at `http://localhost:8000`
   Admin panel: `http://localhost:8000/admin`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## API Endpoints

### Spiritual Gifts
- `GET /api/spiritual-gifts/` - List all spiritual gifts
- `GET /api/spiritual-gifts/{id}/` - Get specific gift details

### Questions
- `GET /api/questions/` - List all survey questions
- `GET /api/questions/{id}/` - Get specific question

### Survey Responses
- `POST /api/survey-responses/` - Submit a new survey response
- `GET /api/survey-responses/{id}/` - Get survey response details
- `GET /api/survey-responses/{id}/results/` - Get calculated results
- `POST /api/survey-responses/{id}/complete/` - Mark survey as completed

## Usage

1. **Start both servers** (backend on port 8000, frontend on port 5173)
2. **Open the application** in your browser at `http://localhost:5173`
3. **Enter optional information** (name and email)
4. **Complete all 120 questions** using the rating scale:
   - **Much** (3 points) - This describes me very well
   - **Some** (2 points) - This describes me somewhat
   - **Little** (1 point) - This describes me a little
   - **Not At All** (0 points) - This does not describe me
5. **Submit the survey** to see your results
6. **View your top spiritual gifts** with scores and percentages
7. **Print or save your results** for future reference

## Scoring System

- Each spiritual gift has 8 questions
- Questions are rated 0-3 points
- Maximum possible score per gift: 24 points (8 questions × 3 points)
- Results show both raw scores and percentages
- Gifts are ranked from highest to lowest score

## Database Models

### SpiritualGift
- Stores the 15 spiritual gift categories
- Includes name and description

### Question
- 120 survey questions
- Each linked to a specific spiritual gift
- Numbered 1-120

### SurveyResponse
- Stores user information (optional)
- Tracks creation and completion timestamps
- Calculates results based on answers

### Answer
- Individual responses to questions
- Links question to survey response
- Stores rating (0-3)

## Development

### Backend Development
- Models: `backend/survey/models.py`
- API Views: `backend/survey/views.py`
- Serializers: `backend/survey/serializers.py`
- Admin Panel: `backend/survey/admin.py`

### Frontend Development
- Survey Form: `frontend/src/views/SurveyView.vue`
- Results Display: `frontend/src/views/ResultsView.vue`
- API Service: `frontend/src/api.js`
- Styles: `frontend/src/style.css`

## Production Deployment

### Backend
1. Update `settings.py`:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for secrets
   - Switch to PostgreSQL for production database
2. Collect static files: `python manage.py collectstatic`
3. Use a production WSGI server (gunicorn, uWSGI)
4. Set up HTTPS with SSL certificate

### Frontend
1. Build for production: `npm run build`
2. Serve the `dist` folder with a web server (Nginx, Apache)
3. Update API endpoints in production configuration

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin` to:
- View all survey responses
- Manage questions and spiritual gifts
- Export data
- Monitor user submissions

## Customization

### Adding More Questions
1. Edit `backend/survey/management/commands/populate_data.py`
2. Add questions to the `questions_data` list
3. Run: `python manage.py populate_data`

### Changing Spiritual Gifts
1. Modify the `gifts_data` list in `populate_data.py`
2. Update frontend descriptions in `ResultsView.vue`

### Styling
- Global styles: `frontend/src/style.css`
- Component-specific styles: Inside each `.vue` file

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

This project is created for ministry use. Feel free to adapt and use for your church or organization.

## Support

For issues or questions:
1. Check the Django logs in terminal
2. Check browser console for frontend errors
3. Verify both servers are running
4. Ensure database is populated with questions

## Future Enhancements

- Email results to users
- PDF export of results
- Historical tracking for repeat surveys
- Group analysis and statistics
- Multi-language support
- Gift descriptions and ministry recommendations
- Integration with church management systems

---

Built with ❤️ for ministry purposes
# spiritual-gifts
