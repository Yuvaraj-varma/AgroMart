# 🌾 AgroMart - Agricultural Marketplace Platform

![AgroMart Banner](https://img.shields.io/badge/AgroMart-Agricultural%20Marketplace-green?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-15.5.4-black?style=flat&logo=next.js)
![React](https://img.shields.io/badge/React-19.1.0-blue?style=flat&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?style=flat&logo=apache-kafka)

**AgroMart** is a full-stack agricultural marketplace platform that connects farmers (vendors) with buyers. It features real-time market price updates from the Government of India's Agmarknet API, role-based authentication, and event-driven order processing.

---

## 🚀 Features

### ✅ Core Features
- 🔐 **User Authentication** - JWT-based auth with Buyer/Vendor roles
- 🌾 **Product Management** - CRUD operations for Crops, Seeds, and Fertilizers
- 🛒 **Shopping Cart** - Add to cart with quantity selection
- 💳 **Payment Options** - Bank Transfer, UPI, Cash on Delivery
- 📈 **Live Market Rates** - Real-time prices from Agmarknet API
- 📦 **Order Processing** - Kafka-based event-driven architecture
- 🖼️ **Image Upload** - Product images with file handling
- 🎨 **Responsive UI** - Modern design with Tailwind CSS

### 🔥 Advanced Features
- ⏰ **Scheduled Updates** - Daily price updates at 6 AM IST
- 🔄 **Price Normalization** - Smart commodity name matching
- 📊 **Historical Data** - MongoDB storage for price history
- 🛡️ **Role-Based Access** - Vendor-only product posting
- 🌐 **CORS Enabled** - Ready for production deployment

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (Users, Products), MongoDB (Live Rates)
- **Message Queue:** Apache Kafka
- **Authentication:** JWT + Bcrypt
- **Scheduler:** APScheduler
- **ORM:** SQLAlchemy

### Frontend
- **Framework:** Next.js 15 (React 19)
- **Styling:** Tailwind CSS 4
- **State Management:** React Context API
- **HTTP Client:** Fetch API

### External APIs
- **Agmarknet API** - Government of India's agricultural market data

---

## 📁 Project Structure

```
AgroMart/
├── backend/
│   ├── app/
│   │   ├── core/           # Security & authentication
│   │   ├── crud/           # Database operations
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # API endpoints
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── database.py     # DB connection
│   │   ├── kafka_producer.py
│   │   └── main.py         # FastAPI app
│   ├── uploads/            # Product images
│   ├── .env                # Environment variables
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── app/            # Next.js pages
    │   └── context/        # React context
    ├── public/             # Static assets
    └── package.json
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL
- MongoDB
- Apache Kafka (optional for order processing)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/AgroMart.git
cd AgroMart
```

### 2️⃣ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run the backend
uvicorn app.main:app --reload
```

**Backend runs on:** `http://127.0.0.1:8000`

### 3️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

**Frontend runs on:** `http://localhost:3000`

---

## 🔧 Environment Variables

Create a `backend/.env` file:

```env
# PostgreSQL
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/agromart

# MongoDB
MONGODB_URL=mongodb://localhost:27017/

# JWT Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Agmarknet API
AGMARKNET_API_KEY=your-api-key-here

# Kafka (Optional)
KAFKA_BOOTSTRAP=localhost:9092
KAFKA_ORDER_TOPIC=order-topic
```

---

## 📡 API Endpoints

### Authentication
```
POST   /api/auth/signup      # Register user
POST   /api/auth/login       # Login
GET    /api/auth/me          # Get current user
```

### Products
```
GET    /api/crops/           # Get all crops
POST   /api/crops/           # Create crop
GET    /api/seeds/           # Get all seeds
GET    /api/fertilizers/     # Get all fertilizers
```

### Live Rates
```
GET    /api/live-rates/latest    # Get latest market rates
GET    /api/live-rates/history   # Get historical data
```

### Orders
```
POST   /api/orders/create    # Create order (sends to Kafka)
```

**Full API Documentation:** `http://127.0.0.1:8000/docs`

---

## 🗄️ Database Schema

### PostgreSQL Tables
- **buyers** - Buyer accounts
- **vendors** - Vendor accounts
- **crops** - Crop listings
- **seeds** - Seed listings
- **fertilizers** - Fertilizer listings
- **products** - Generic products

### MongoDB Collections
- **liveRatesDB.rates** - Daily market rates from Agmarknet

---

## 🎯 Usage

### For Buyers
1. Sign up as a **Buyer**
2. Browse crops, seeds, and fertilizers
3. Check live market rates
4. Add items to cart
5. Select payment method and place order

### For Vendors
1. Sign up as a **Vendor**
2. Post products (crops, seeds, fertilizers)
3. Manage product listings
4. View orders (via Kafka consumer - not included)

---

## 🔐 Security Features

- ✅ Password hashing with Bcrypt
- ✅ JWT token authentication
- ✅ Role-based access control
- ✅ CORS protection
- ✅ Environment variable protection
- ✅ SQL injection prevention (SQLAlchemy ORM)

---

## 🚧 Future Enhancements

- [ ] Payment gateway integration (Razorpay/Stripe)
- [ ] Real-time chat between buyers and vendors
- [ ] Order tracking system
- [ ] Vendor dashboard with analytics
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Admin panel

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Yuvaraj**

- GitHub: [@YourGitHubUsername](https://github.com/YourGitHubUsername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- [Agmarknet API](https://agmarknet.gov.in/) - Government of India
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## 📸 Screenshots

### Homepage
![Homepage](screenshots/homepage.png)

### Live Market Rates
![Live Rates](screenshots/live-rates.png)

### Shopping Cart
![Cart](screenshots/cart.png)

---

## 📞 Support

For support, email yuvaraj@example.com or open an issue in this repository.

---

<div align="center">
  <strong>⭐ Star this repository if you find it helpful!</strong>
</div>
