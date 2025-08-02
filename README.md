# WasteWise - Smart Waste Management Platform

A comprehensive waste management and sanitation platform built with Django, featuring IoT integration, gamification, and mobile-responsive design.

## 🌟 Features

### Core Functionality
- **Smart Waste Pickup Scheduling**: Users can schedule segregated waste collection with preferred time slots
- **IoT Sensor Integration**: Real-time monitoring of bin fill levels, alerts, and maintenance tracking
- **Gamification System**: Points, badges, leaderboards, and rewards to encourage recycling behavior
- **User Management**: Custom user profiles with different user types (residents, collectors, admins)

### Technical Features
- **RESTful API**: Complete API endpoints for mobile app integration
- **Real-time Dashboard**: IoT sensor monitoring and alerts
- **Responsive Design**: Mobile-first responsive UI using Bootstrap 5
- **Admin Interface**: Comprehensive Django admin for system management

## 🏗️ Architecture

### Database Models
- **Users App**: Custom user model with profile management and gamification fields
- **Waste App**: Pickup scheduling, waste categories, locations, and collection tracking
- **Sensors App**: IoT bin monitoring, sensor readings, alerts, and maintenance logs
- **Gamification App**: Badges, rewards, leaderboards, and user achievements

### Technology Stack
- **Backend**: Django 5.2, Django REST Framework
- **Database**: SQLite (development), PostgreSQL-ready
- **Frontend**: Bootstrap 5, JavaScript, Chart.js
- **Authentication**: Django's built-in auth with custom user model
- **Styling**: Custom CSS with responsive design

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual environment

### Installation Steps

1. **Clone and Setup Environment**
```bash
cd project-102
python3 -m venv waste_management_env
source waste_management_env/bin/activate  # On Windows: waste_management_env\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

4. **Run Development Server**
```bash
python manage.py runserver
```

5. **Access the Application**
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📱 Application Structure

### Apps Overview

#### 1. Users App (`/users/`)
- Custom user registration and authentication
- User dashboard with pickup statistics
- Profile management with gamification data
- User types: Resident, Collector, Admin

#### 2. Waste App (`/waste/`)
- Waste pickup scheduling system
- Waste category management
- Location-based pickup services
- Collection history and tracking

#### 3. Sensors App (`/sensors/`)
- IoT bin monitoring dashboard
- Real-time sensor data collection
- Alert management system
- Maintenance logging

#### 4. Gamification App (`/gamification/`)
- Points and leveling system
- Badge achievement system
- Community leaderboards
- Reward redemption marketplace

### Key Features Implemented

#### 🗓️ Pickup Scheduling System
- Schedule waste collection by category
- Priority-based scheduling (low, medium, high, urgent)
- Automatic points calculation based on weight and segregation quality
- Status tracking: pending → confirmed → in progress → completed

#### 🤖 IoT Integration
- Smart bin monitoring with fill level sensors
- Real-time alerts for bin status (full, overflow, maintenance needed)
- Sensor battery monitoring and maintenance scheduling
- Anomaly detection for unusual sensor readings

#### 🎮 Gamification Engine
- Points system: 10 points per kg + bonuses for proper segregation
- Level system: automatic leveling based on points earned
- Badge system: recyclable achievements for different milestones
- Leaderboards: weekly, monthly, and all-time rankings
- Reward marketplace: redeem points for discounts and vouchers

#### 📊 Analytics & Monitoring
- User dashboard with recycling statistics
- Sensor data visualization
- Collection efficiency metrics
- Environmental impact tracking

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Settings Configuration
- Custom user model: `users.User`
- Media and static files handling
- CORS configuration for API access
- REST framework pagination and authentication

## 🔒 Security Features
- Custom user authentication
- CSRF protection
- Secure password validation
- Session-based authentication
- API token authentication ready

## 📱 Mobile Responsiveness
- Bootstrap 5 responsive grid system
- Mobile-first design approach
- Touch-friendly interface elements
- Progressive web app ready

## 🚀 Production Deployment
The application is configured for easy deployment with:
- WhiteNoise for static file serving
- PostgreSQL database support
- Gunicorn WSGI server configuration
- Environment-based configuration management

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License
This project is licensed under the MIT License.

## 🆘 Support
For support and questions, please create an issue in the repository.

---

Built with ❤️ for a cleaner, smarter tomorrow!