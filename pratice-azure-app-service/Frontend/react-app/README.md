## 🏗️ Architecture

```
Assignment-2/
├── Backend/              # Flask API
│   ├── api/
│   │   └── routes.py    # API endpoints
│   ├── app.py           # Flask app with CORS
│   ├── models.py        # Database models
│   └── requirements.txt # Python dependencies
│
└── Frontend/            # React App
    └── react-app/
        ├── src/
        │   ├── App.jsx      # Main component
        │   ├── App.css      # Component styles
        │   └── index.css    # Global design system
        └── .env.example     # Environment config
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose (for containerized deployment)
- OR Node.js 20+ and Python 3.12+ (for local development)

### Option 1: Docker Deployment (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd Backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Update database credentials

5. **Run the backend:**
   ```bash
   python app.py
   ```
   Backend will be available at http://localhost:5000

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd Frontend/react-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure API URL:**
   - Copy `.env.example` to `.env`
   - Update `VITE_API_URL` if needed (default: http://localhost:5000)

4. **Run the development server:**
   ```bash
   npm run dev
   ```
   Frontend will be available at http://localhost:5173

## 📡 API Endpoints

### GET /items
Fetch all items from the database.

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Sample Item",
      "source": "manual",
      "created_at": "2024-12-24T12:00:00"
    }
  ]
}
```

### POST /add-item
Add a new item to the database.

**Request Body:**
```json
{
  "name": "New Item",
  "source": "api"
}
```

**Response:**
```json
{
  "status": "added",
  "item": {
    "id": 2,
    "name": "New Item",
    "source": "api",
    "created_at": "2024-12-24T12:00:00"
  }
}
```

## 🎨 UI Features

### Design System
- **Color Palette**: Modern gradients with purple, blue, and pink accents
- **Typography**: Inter font family for clean, modern text
- **Effects**: Glassmorphism, smooth animations, hover effects
- **Responsive**: Mobile-first design with breakpoints

### Components

1. **Add Item Form**
   - Sticky sidebar on desktop
   - Input validation
   - Success/error messages
   - Loading states

2. **Items Grid**
   - Responsive card layout
   - Animated on scroll
   - Hover effects
   - Item count badge
   - Refresh button

3. **States**
   - Loading spinner
   - Empty state with icon
   - Error messages
   - Success notifications

## 🔧 Configuration

### Environment Variables

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:5000
```

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## 🐛 Troubleshooting

### CORS Issues
- Ensure `flask-cors` is installed in backend
- Check that CORS is enabled in `app.py`

### API Connection Failed
- Verify backend is running on port 5000
- Check `VITE_API_URL` in frontend `.env`
- Ensure no firewall blocking the connection

### Items Not Displaying
- Check browser console for errors
- Verify database connection in backend
- Test API endpoints directly: http://localhost:5000/items

## 📝 Development Notes

### Backend Changes Made
1. ✅ Updated `/add-item` endpoint to accept JSON data
2. ✅ Added request validation for name and source fields
3. ✅ Added CORS support for cross-origin requests
4. ✅ Added flask-cors to requirements.txt

### Frontend Implementation
1. ✅ Created modern design system with CSS variables
2. ✅ Built responsive React component with hooks
3. ✅ Implemented API integration with fetch
4. ✅ Added form validation and error handling
5. ✅ Created loading, error, and empty states
6. ✅ Added smooth animations and transitions

## 🎯 Next Steps

- [ ] Add delete item functionality
- [ ] Add edit item functionality
- [ ] Add search/filter capabilities
- [ ] Add pagination for large datasets
- [ ] Add user authentication
- [ ] Add item categories/tags

## 📄 License

This project is part of Docker Assignment-2.

---

**Enjoy managing your items! 🚀**
