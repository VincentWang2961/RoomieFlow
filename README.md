# RoomieFlow - Accommodation Scheduling Management System

A lightweight, web-based accommodation scheduling management system designed for simplicity and ease of use. The system handles accommodation time slot applications and approvals with minimal complexity while maintaining essential functionality for user management, property administration, and flexible time allocation parameters.

## 🏗️ Architecture

- **Backend**: Flask with SQLAlchemy, JWT authentication
- **Frontend**: Vue.js 3 with Composition API, Pinia state management
- **Database**: PostgreSQL (production) / SQLite (development)
- **Deployment**: Docker containers with Traefik reverse proxy

## 🚀 Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RoomieFlow
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Initialize the database** (first time only)
   ```bash
   docker-compose exec backend python migrations_init.py
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Default admin login: `admin` / `admin123`

## 🛠️ Development Setup

### Backend Development

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python migrations_init.py
   ```

6. **Run development server**
   ```bash
   flask run
   ```

### Frontend Development

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh JWT token

### User Management

- `GET /api/users/` - Get all users (admin only)
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user information
- `PUT /api/users/{id}/password` - Change user password

### Property Management

- `GET /api/properties/` - Get user's properties
- `POST /api/properties/` - Create new property
- `GET /api/properties/{id}` - Get property details
- `PUT /api/properties/{id}` - Update property

### Room Management

- `GET /api/rooms/?property_id={id}` - Get rooms for property
- `POST /api/rooms/` - Create new room
- `GET /api/rooms/{id}` - Get room details
- `PUT /api/rooms/{id}` - Update room

### Booking Management

- `GET /api/bookings/` - Get user's bookings
- `POST /api/bookings/` - Create booking application
- `GET /api/bookings/{id}` - Get booking details
- `PUT /api/bookings/{id}/approve` - Approve booking
- `PUT /api/bookings/{id}/reject` - Reject booking
- `GET /api/bookings/weekly` - Get weekly booking chart data (New!)

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
FLASK_ENV=development
DATABASE_URL=postgresql://user:pass@localhost:5432/roomieflow
JWT_SECRET_KEY=your-secret-key-here
```

### Time Allocation System

The system supports three session types:
- **Morning**: 0.5 days (configurable)
- **Midday**: 1.0 days (includes lunch)
- **Evening**: 1.0 days (includes overnight stay)

Weekly limits are configurable per property with shared time pools between users.

## 📊 Visual Booking Chart

The application now features an intuitive weekly booking chart that provides a clear overview of accommodation schedules:

### Key Features
- **Weekly Calendar View**: Monday-to-Sunday layout showing the entire week at a glance
- **Time Slot Organization**: Three daily sessions (Morning, Midday, Evening) displayed in a grid format
- **Status Color Coding**:
  - 🟡 **Yellow**: Pending bookings awaiting approval
  - 🟢 **Green**: Approved bookings confirmed for use
  - 🔴 **Red**: Rejected booking applications
- **Interactive Navigation**: 
  - Previous/Next week arrows for browsing different time periods
  - "Today" button to quickly return to current week
  - Current day highlighting for easy reference
- **Booking Details**: Each booking shows user name, room, and status at a glance
- **Click-to-Book**: Empty time slots can be clicked to initiate booking creation
- **Responsive Design**: Optimized for both desktop and mobile devices

### Usage
1. Navigate to the Dashboard after logging in
2. Scroll down to view the "Weekly Booking Schedule"
3. Use navigation controls to browse different weeks
4. Click on any booking to view details or on empty slots to create new bookings

## 🏠 Features

### Current Implementation (MVP)

- ✅ User registration and authentication
- ✅ Property and room management
- ✅ Booking application system
- ✅ Admin approval workflow
- ✅ Time allocation tracking
- ✅ JWT-based API authentication
- ✅ Responsive web interface
- ✅ **Visual Weekly Booking Chart** (New!)
  - Monday-to-Sunday calendar view
  - Interactive time slots (Morning, Midday, Evening)
  - Color-coded booking status (Pending/Approved/Rejected)
  - Week navigation with today highlighting
  - Click-to-book functionality

### Planned Features

- ⏳ Email notifications
- ⏳ Calendar integration
- ⏳ Usage analytics
- ⏳ Mobile app

## 🐳 Docker Deployment

The application includes complete Docker configuration for easy deployment:

```yaml
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔒 Security

- Secure password hashing with bcrypt
- JWT token-based authentication
- Input validation and sanitization
- SQL injection prevention
- CORS protection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` folder

## 🚦 Project Status

**Current Phase**: MVP Development ✅  
**Version**: 0.2.0  
**Status**: Enhanced with Visual Booking Chart - Ready for Testing