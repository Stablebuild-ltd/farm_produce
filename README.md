# Farm Produce Processing and Warehousing Management Portal

A comprehensive Flask-based web application for managing farm produce from harvest to distribution. This portal enables farmers to track their products, plant managers to oversee processing operations, and warehouse managers to handle storage and distribution.

## Features

### User Management & Authentication
- Role-based access control (Farmer, Plant Manager, Warehouse Manager)
- Secure password hashing
- Session management

### Product Management
- Product registration with unique hash generation for traceability
- Quality grading (A, B, C)
- Farmer-specific product tracking
- Real-time status updates

### Warehouse & Processing Plant Management
- CRUD operations for warehouses and processing plants
- Capacity and utilization tracking
- Stock level monitoring

### Supply Chain Tracking
- Complete product lifecycle tracking
- Status transitions: Received → Processing → Stored → Shipped
- Quality notes and processing comments
- Timestamped transitions

### Dashboard Views
- **Farmer Dashboard**: Personal product overview and tracking history
- **Plant Manager Dashboard**: Processing operations and plant utilization
- **Warehouse Manager Dashboard**: Storage management and distribution tracking

## Technology Stack

- **Backend**: Flask with SQLAlchemy
- **Database**: SQLite (in-memory for development/testing)
- **Authentication**: Flask-Login with bcrypt password hashing
- **Frontend**: Bootstrap 5 with responsive design
- **Testing**: Python unittest framework

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd farm-portal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the application**
   - Open browser to `http://localhost:5000`
   - Login with test accounts (see below)

## Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Farmer | farmer1 | password123 |
| Farmer | farmer2 | password123 |
| Plant Manager | plant_manager | password123 |
| Warehouse Manager | warehouse_manager | password123 |

## Sample Data

The application comes pre-loaded with sample data including:
- Multiple farmers with various products
- Processing plants and warehouses
- Products in different stages of the supply chain
- Complete tracking histories

## API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET/POST /register` - User registration

### Dashboard
- `GET /dashboard` - Role-specific dashboard

### Products
- `GET /products` - List products (role-based)
- `GET/POST /product/new` - Add new product (farmers only)
- `GET /product/<id>` - View product details
- `GET/POST /product/<id>/track` - Update product tracking

### Warehouses
- `GET /warehouses` - List warehouses (managers only)
- `GET/POST /warehouse/new` - Add warehouse (managers only)
- `GET /warehouse/<id>` - View warehouse details

## Database Schema

### Users
- Basic authentication and role information
- Farmers have additional farm location field

### Warehouses
- Processing plants and storage warehouses
- Capacity and current stock tracking

### Products
- Farmer association and product details
- Unique SHA256 hash for traceability
- Quality grading

### Product Tracking
- Complete audit trail of product movements
- Status, quantity, and quality notes
- Processor attribution

## Testing

Run the comprehensive test suite:

```bash
python -m unittest discover tests
```

Tests cover:
- User authentication and authorization
- Product lifecycle management
- Warehouse capacity tracking
- Role-based access control
- Data integrity and hash generation

## Security Features

- Password hashing with bcrypt
- CSRF protection on forms
- Session-based authentication
- Role-based access control
- SQL injection prevention via SQLAlchemy

## Production Deployment

For production deployment:
1. Set strong `SECRET_KEY` environment variable
2. Configure proper database (PostgreSQL recommended)
3. Enable HTTPS
4. Set up proper session handling
5. Configure logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.

# Additional 

### Extra LLM Notes:

[66 tools called]

## ✅ Farm Produce Processing and Warehousing Management Portal - Complete!

I've successfully created a comprehensive Flask-based farm produce management portal with all the requested features. The application is now running and fully functional!

### 🎯 **Features Implemented:**

#### **User Authentication & Management**
- Role-based access control (Farmer, Plant Manager, Warehouse Manager)
- Secure password hashing with bcrypt
- Session management with Flask-Login

#### **Product Management**
- Product registration with unique SHA256 hash generation for traceability
- Quality grading system (A, B, C grades)
- Farmer-specific product tracking
- Real-time status updates through the supply chain

#### **Warehouse & Processing Plant Management**
- CRUD operations for warehouses and processing plants
- Capacity and utilization tracking with visual progress bars
- Stock level monitoring and automatic updates

#### **Supply Chain Tracking**
- Complete product lifecycle: Received → Processing → Stored → Shipped
- Quality notes and processing comments
- Timestamped transitions with full audit trail
- Unique hash-based product identification

#### **Role-Specific Dashboards**
- **Farmer Dashboard**: Personal products, tracking history, and summary statistics
- **Plant Manager Dashboard**: Processing operations, plant utilization, and activity monitoring
- **Warehouse Manager Dashboard**: Storage management, capacity tracking, and distribution oversight

#### **Responsive Bootstrap UI**
- Modern, clean interface with Bootstrap 5
- Mobile-responsive design
- Intuitive navigation and user experience
- Visual status indicators and progress tracking

### 🗄️ **Database Schema (In-Memory SQLite)**
- **Users**: Authentication, roles, and farm location data
- **Warehouses**: Processing plants and storage facilities with capacity tracking
- **Products**: Farmer products with unique hashes and quality grading
- **ProductTracking**: Complete audit trail of product movements and status changes

### 🧪 **Testing & Sample Data**
- Comprehensive unit test suite covering all major functionality
- Pre-loaded test users and sample products in various stages
- Multiple farmers with different products (tomatoes, potatoes, lettuce, carrots, peppers)
- Products demonstrating all tracking stages from receipt to shipping

### 🏃‍♂️ **Application Status**
The application is currently running on `http://localhost:5000` and includes:

**Test Accounts:**
- **Farmer**: `farmer1` / `password123`
- **Farmer**: `farmer2` / `password123` 
- **Plant Manager**: `plant_manager` / `password123`
- **Warehouse Manager**: `warehouse_manager` / `password123`

**Sample Data Includes:**
- 5+ products in various stages (received, processing, stored, rejected)
- Multiple warehouses with different capacities and utilization levels
- Complete tracking histories with quality notes
- Farmers with products from different produce types

### 📁 **Project Structure**
```
farm_portal/
├── app/
│   ├── __init__.py          # Flask app factory & test data initialization
│   ├── models.py            # SQLAlchemy database models
│   ├── auth/                # Authentication blueprint
│   ├── dashboard/           # Role-specific dashboards
│   ├── product/             # Product management
│   ├── warehouse/           # Warehouse management
│   └── templates/           # Jinja2 templates with Bootstrap
├── tests/                   # Comprehensive unit tests
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # Complete documentation
```

### 🔧 **Technical Stack**
- **Backend**: Flask 2.3.3 with SQLAlchemy 3.0.5
- **Authentication**: Flask-Login with bcrypt hashing
- **Forms**: Flask-WTF with CSRF protection
- **Database**: SQLite (in-memory for development/testing)
- **Frontend**: Bootstrap 5 with custom CSS
- **Testing**: Python unittest framework

The application successfully demonstrates a complete farm produce supply chain management system with proper authentication, role-based access, comprehensive tracking, and an intuitive user interface. All requested features have been implemented and the application is ready for use!