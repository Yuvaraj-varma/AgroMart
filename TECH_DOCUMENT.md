# 🌾 AgroMart - Complete Technology Document
## For Interview Preparation & Learning

---

# 1. PROGRAMMING LANGUAGES

## Python (Backend)
- **Version:** Python 3.13
- **Used for:** All backend logic, API, database operations
- **Why Python?**
  - Easy to read and write
  - Huge library ecosystem
  - Best for data-heavy applications
  - Industry standard for backend APIs

## JavaScript (Frontend)
- **Version:** ES2024 (Modern JS)
- **Used for:** All frontend UI, user interactions
- **Why JavaScript?**
  - Only language that runs in browsers
  - React/Next.js are built on JS
  - Huge community and ecosystem

---

# 2. FRAMEWORKS

## FastAPI (Backend Framework)
- **What it is:** Modern Python web framework for building APIs
- **Version:** Latest
- **Why FastAPI?**
  - Very fast (one of the fastest Python frameworks)
  - Auto-generates API documentation (Swagger UI)
  - Built-in data validation using Pydantic
  - Async support
- **How used in AgroMart:**
  - All REST API endpoints
  - Request/Response handling
  - Middleware (CORS)
  - Static file serving (uploads)
- **Key concepts:**
  - `APIRouter` - groups related endpoints
  - `Depends()` - dependency injection
  - `Form()` - form data handling
  - `File()` - file upload handling

## Next.js 15 (Frontend Framework)
- **What it is:** React framework for production
- **Version:** 15.5.4
- **Why Next.js?**
  - Built on top of React
  - File-based routing (each file = one page)
  - Server-side rendering support
  - Built-in optimization
- **How used in AgroMart:**
  - All frontend pages
  - Client-side routing
  - Environment variables (NEXT_PUBLIC_API_URL)
- **Key concepts:**
  - `"use client"` - marks component as client-side
  - `useRouter()` - programmatic navigation
  - `useSearchParams()` - read URL parameters
  - App Router (src/app/ folder structure)

## React 19 (UI Library)
- **What it is:** JavaScript library for building user interfaces
- **Version:** 19.1.0
- **Why React?**
  - Component-based architecture
  - Virtual DOM for fast updates
  - Huge ecosystem
  - Industry standard
- **How used in AgroMart:**
  - All UI components
  - State management with hooks
  - Context API for cart
- **Key concepts used:**
  - `useState` - local component state
  - `useEffect` - side effects (API calls)
  - `useContext` - global state (cart)
  - `createContext` - create global state

---

# 3. DATABASES

## PostgreSQL (Relational Database)
- **What it is:** Open-source relational database
- **Why PostgreSQL?**
  - ACID compliant (data is always safe)
  - Handles structured data perfectly
  - Supports complex queries
  - Industry standard
- **How used in AgroMart:**
  - Stores users (buyers, vendors)
  - Stores products (crops, seeds, fertilizers)
  - Stores orders
- **Tables in AgroMart:**
  ```
  buyers       - buyer accounts
  vendors      - vendor accounts
  crops        - crop listings
  seeds        - seed listings
  fertilizers  - fertilizer listings
  products     - generic products
  orders       - order records
  order_items  - items in each order
  ```
- **Connection:** `postgresql+psycopg2://user:pass@localhost:5432/db`

## MongoDB (NoSQL Database)
- **What it is:** Document-based NoSQL database
- **Why MongoDB?**
  - Flexible schema (no fixed columns)
  - Perfect for storing API response data
  - Fast reads for large datasets
  - JSON-like documents
- **How used in AgroMart:**
  - Stores live market rates from Agmarknet API
  - Stores order history (from Kafka)
  - Stores price history
- **Collections in AgroMart:**
  ```
  rates         - daily market rates (crops + seeds)
  orders        - Kafka-consumed orders
  price_history - historical commodity prices
  ```
- **Connection:** `mongodb://localhost:27017/`
- **Database name:** `liveRatesDB`

---

# 4. ORM (Object Relational Mapper)

## SQLAlchemy
- **What it is:** Python ORM for databases
- **Why ORM?**
  - Write Python code instead of SQL
  - Prevents SQL injection attacks
  - Easy to switch databases
  - Auto-creates tables from Python classes
- **How used in AgroMart:**
  - All PostgreSQL operations
  - Model definitions
  - Session management
- **Key concepts:**
  ```python
  # Model = Table
  class Crop(Base):
      __tablename__ = "crops"
      id = Column(Integer, primary_key=True)
      name = Column(String(100))

  # Query = SELECT
  db.query(Crop).all()              # SELECT * FROM crops
  db.query(Crop).filter(id==1)      # SELECT * WHERE id=1
  db.add(crop)                      # INSERT
  db.commit()                       # SAVE
  db.delete(crop)                   # DELETE
  ```

## PyMongo
- **What it is:** Python driver for MongoDB
- **How used in AgroMart:**
  - All MongoDB operations
  - Creating indexes
  - Storing/fetching live rates
- **Key concepts:**
  ```python
  collection.find_one()             # Get one document
  collection.find()                 # Get all documents
  collection.update_one(upsert=True)# Insert or Update
  collection.create_index()         # Create index
  ```

---

# 5. AUTHENTICATION & SECURITY

## JWT (JSON Web Tokens)
- **What it is:** Token-based authentication system
- **Library:** `python-jose`
- **Algorithm:** HS256
- **Expiry:** 60 minutes
- **How it works:**
  ```
  1. User logs in with email + password
  2. Backend verifies password
  3. Backend creates JWT token with user_id + role
  4. Frontend stores token in localStorage
  5. Every request sends token in header:
     Authorization: Bearer <token>
  6. Backend verifies token on protected routes
  ```
- **Token contains:**
  ```json
  {
    "sub": "123",        ← user ID
    "role": "vendor",    ← user role
    "exp": 1234567890    ← expiry time
  }
  ```

## Bcrypt (Password Hashing)
- **What it is:** Password hashing algorithm
- **Library:** `passlib[bcrypt]`
- **Why hash passwords?**
  - Never store plain text passwords
  - Even if database is hacked, passwords are safe
  - One-way hash (can't reverse it)
- **How it works:**
  ```
  Plain password: "mypassword123"
  Hashed:         "$2b$12$abc...xyz" (stored in DB)
  
  Login: verify("mypassword123", "$2b$12$abc...xyz") → True/False
  ```

## HTTPBearer
- **What it is:** FastAPI security scheme
- **Used for:** Extracting JWT token from request headers
- **Swagger UI:** Shows "Authorize" button in API docs

---

# 6. MESSAGE QUEUE

## Apache Kafka
- **What it is:** Distributed event streaming platform
- **Library:** `kafka-python`
- **Why Kafka?**
  - Handles high volume of messages
  - Decouples services (producer doesn't wait for consumer)
  - Messages are stored and can be replayed
  - Industry standard for event-driven architecture
- **How used in AgroMart:**
  - When buyer places order → sent to Kafka topic
  - Kafka stores the order message
  - Consumer (separate service) can process orders
- **Key concepts:**
  ```
  Producer  → sends messages to Kafka
  Consumer  → reads messages from Kafka
  Topic     → category of messages ("order-topic")
  Broker    → Kafka server (localhost:9092)
  ```
- **Flow in AgroMart:**
  ```
  Cart → Place Order → FastAPI → KafkaProducer → order-topic
  ```

---

# 7. DATA VALIDATION

## Pydantic
- **What it is:** Python data validation library
- **Version:** v2
- **Why Pydantic?**
  - Validates data automatically
  - Converts types automatically
  - Clear error messages
  - FastAPI uses it natively
- **How used in AgroMart:**
  - All request/response schemas
  - Input validation rules
  - Settings management
- **Key concepts:**
  ```python
  class CropCreate(BaseModel):
      name: str                    # required string
      price: Optional[float]       # optional float
      
      @field_validator("price")
      def validate_price(cls, v):
          if v <= 0:
              raise ValueError("Price must be > 0")
          return v
  ```

## Pydantic Settings
- **What it is:** Pydantic extension for app configuration
- **Library:** `pydantic-settings`
- **How used in AgroMart:**
  - Loads all environment variables from `.env`
  - Type-safe configuration
  - Single source of truth for all settings

---

# 8. TASK SCHEDULING

## APScheduler
- **What it is:** Python job scheduling library
- **How used in AgroMart:**
  - Runs `fetch_and_store_agmarknet_data()` every day at 6 AM IST
  - Automatically updates live market rates
- **Key concepts:**
  ```python
  scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
  scheduler.add_job(my_function, "cron", hour=6, minute=0)
  scheduler.start()
  ```

---

# 9. EXTERNAL API

## Agmarknet API (Government of India)
- **What it is:** India's agricultural market data API
- **Provider:** data.gov.in
- **URL:** `https://api.data.gov.in/resource/9ef84268...`
- **What data it provides:**
  - Daily commodity prices from mandis across India
  - Min price, Max price, Modal price
  - Market name, State, Commodity name
- **How used in AgroMart:**
  - Fetched daily at 6 AM IST
  - Stored in MongoDB
  - Displayed on Live Rates page
  - Used to update product prices dynamically

---

# 10. STYLING

## Tailwind CSS 4
- **What it is:** Utility-first CSS framework
- **Version:** 4
- **Why Tailwind?**
  - No need to write custom CSS
  - Responsive design built-in
  - Fast development
  - Consistent design
- **How used in AgroMart:**
  - All UI styling
  - Responsive grid layouts
  - Colors, spacing, typography
- **Key classes used:**
  ```
  bg-green-600    → green background
  text-white      → white text
  rounded-lg      → rounded corners
  shadow-md       → drop shadow
  flex            → flexbox layout
  grid            → grid layout
  hover:bg-green-700 → hover effect
  ```

---

# 11. STATE MANAGEMENT

## React Context API
- **What it is:** Built-in React state management
- **Why Context?**
  - Share state across all components
  - No need for external library (Redux)
  - Simple and lightweight
- **How used in AgroMart:**
  - Cart state shared across all pages
  - `CartProvider` wraps entire app
  - Any page can access cart with `useCart()`
- **Key concepts:**
  ```javascript
  // Create context
  const CartContext = createContext()
  
  // Provide to all children
  <CartContext.Provider value={{cartItems, addToCart}}>
    {children}
  </CartContext.Provider>
  
  // Use anywhere
  const { cartItems, addToCart } = useCart()
  ```

## localStorage
- **What it is:** Browser storage that persists on refresh
- **How used in AgroMart:**
  - Stores JWT token
  - Stores user role
  - Stores user name
  - Stores cart items (persists on refresh)

---

# 12. TESTING

## Pytest
- **What it is:** Python testing framework
- **How used in AgroMart:**
  - 25 automated tests
  - Tests auth, products, validation
- **Test files:**
  ```
  tests/
  ├── conftest.py         ← test setup (TestClient)
  ├── test_auth.py        ← 6 auth tests
  ├── test_products.py    ← 6 product tests
  └── test_validation.py  ← 13 validation tests
  ```
- **Run tests:**
  ```bash
  .venv\Scripts\pytest tests/ -v
  ```

## FastAPI TestClient
- **What it is:** Test HTTP requests without running server
- **Library:** `httpx`
- **How used:**
  ```python
  client = TestClient(app)
  res = client.post("/api/auth/signup", json={...})
  assert res.status_code == 200
  ```

---

# 13. CONTAINERIZATION

## Docker
- **What it is:** Container platform
- **Files created:**
  - `backend/Dockerfile` - builds backend image
  - `frontend/Dockerfile` - builds frontend image
  - `docker-compose.yml` - runs all services together
- **Services in docker-compose:**
  ```
  postgres    → PostgreSQL database
  mongodb     → MongoDB database
  zookeeper   → Required for Kafka
  kafka       → Message queue
  backend     → FastAPI app
  frontend    → Next.js app
  ```
- **Run everything:**
  ```bash
  docker-compose up --build
  ```

---

# 14. PROJECT ARCHITECTURE

## Backend Architecture Pattern
```
Request → Router → Service → CRUD → Database
                ↓
           Pydantic Schema (validation)
```

- **Router** → handles HTTP (GET, POST, PUT, DELETE)
- **Service** → business logic (save image, build data)
- **CRUD** → database queries only
- **Schema** → data validation and shapes

## Frontend Architecture Pattern
```
Page → API call → Backend
  ↓
Context (Cart state)
  ↓
localStorage (persistence)
```

## Database Architecture
```
PostgreSQL → structured data (users, products)
MongoDB    → flexible data (live rates, orders)
```

---

# 15. API DESIGN

## REST API
- **What it is:** Architectural style for APIs
- **HTTP Methods used:**
  ```
  GET    → fetch data
  POST   → create data
  PUT    → update data
  DELETE → delete data
  ```
- **Status codes used:**
  ```
  200 → Success
  400 → Bad Request (validation error)
  401 → Unauthorized (no/invalid token)
  403 → Forbidden (wrong role)
  404 → Not Found
  422 → Unprocessable Entity (Pydantic error)
  500 → Server Error
  ```

## All API Endpoints
```
Auth:
POST   /api/auth/signup
POST   /api/auth/login
GET    /api/auth/me

Crops:
GET    /api/crops/
POST   /api/crops/
GET    /api/crops/{id}
PUT    /api/crops/{id}
DELETE /api/crops/{id}

Seeds:
GET    /api/seeds/
POST   /api/seeds/
GET    /api/seeds/{id}
PUT    /api/seeds/{id}
DELETE /api/seeds/{id}

Fertilizers:
GET    /api/fertilizers/
POST   /api/fertilizers/
GET    /api/fertilizers/{id}
PUT    /api/fertilizers/{id}
DELETE /api/fertilizers/{id}

Live Rates:
GET    /api/live-rates/
GET    /api/live-rates/latest
GET    /api/live-rates/history

Orders:
POST   /api/orders/create

Vendor:
GET    /api/vendor/my-products
DELETE /api/vendor/my-products/{category}/{id}
```

---

# 16. ENVIRONMENT VARIABLES

## .env file (Backend)
```env
DATABASE_URL=postgresql+psycopg2://...
MONGODB_URL=mongodb://localhost:27017/
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
AGMARKNET_API_KEY=your-api-key
KAFKA_BOOTSTRAP=localhost:9092
KAFKA_ORDER_TOPIC=order-topic
```

## .env.local (Frontend)
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

---

# 17. TOOLS & UTILITIES

| Tool | Purpose |
|------|---------|
| **uvicorn** | ASGI server to run FastAPI |
| **psycopg2** | PostgreSQL adapter for Python |
| **python-dotenv** | Load .env files |
| **pytz** | Timezone handling (IST) |
| **requests** | HTTP requests to Agmarknet API |
| **ESLint** | JavaScript code linting |
| **Turbopack** | Fast Next.js bundler |

---

# 18. COMPLETE TECH STACK SUMMARY

## Backend
| Category | Technology |
|----------|-----------|
| Language | Python 3.13 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Relational DB | PostgreSQL |
| NoSQL DB | MongoDB |
| DB Driver (PG) | psycopg2 |
| DB Driver (Mongo) | PyMongo |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) |
| Password | Bcrypt (passlib) |
| Message Queue | Apache Kafka |
| Scheduler | APScheduler |
| Testing | Pytest + httpx |
| Config | pydantic-settings |
| Server | Uvicorn |

## Frontend
| Category | Technology |
|----------|-----------|
| Language | JavaScript (ES2024) |
| Framework | Next.js 15 |
| UI Library | React 19 |
| Styling | Tailwind CSS 4 |
| State | React Context API |
| Storage | localStorage |
| HTTP | Fetch API |
| Routing | Next.js App Router |

## Infrastructure
| Category | Technology |
|----------|-----------|
| Containerization | Docker |
| Orchestration | Docker Compose |
| Version Control | Git + GitHub |
| External API | Agmarknet (data.gov.in) |

---

# 19. KEY CONCEPTS TO LEARN FOR INTERVIEW

## Backend Concepts
1. **REST API** - what it is, HTTP methods, status codes
2. **JWT Authentication** - how tokens work, why stateless
3. **ORM** - what it is, why use it, SQLAlchemy basics
4. **Dependency Injection** - FastAPI's `Depends()`
5. **Middleware** - CORS, what it does
6. **Pydantic Validation** - schemas, validators
7. **Event-Driven Architecture** - Kafka, producer/consumer

## Database Concepts
1. **SQL vs NoSQL** - when to use which
2. **PostgreSQL** - relational, ACID, tables, foreign keys
3. **MongoDB** - documents, collections, flexible schema
4. **Indexes** - why they make queries faster
5. **ORM vs Raw SQL** - pros and cons

## Frontend Concepts
1. **React Hooks** - useState, useEffect, useContext
2. **Context API** - global state management
3. **localStorage** - browser storage, persistence
4. **Fetch API** - HTTP requests from browser
5. **Next.js Routing** - file-based routing, App Router

## Security Concepts
1. **Password Hashing** - why never store plain text
2. **JWT** - structure, signing, verification
3. **CORS** - what it is, why needed
4. **Role-Based Access** - buyer vs vendor permissions
5. **Environment Variables** - why not hardcode secrets

## DevOps Concepts
1. **Docker** - containers, images, Dockerfile
2. **Docker Compose** - multi-service setup
3. **Git** - version control, commits, push/pull
4. **Environment Variables** - .env files

---

# 20. INTERVIEW QUESTIONS & ANSWERS

**Q: Why did you use FastAPI instead of Django?**
A: FastAPI is faster, has automatic API documentation, built-in validation with Pydantic, and is better suited for building REST APIs. Django is better for full-stack web apps with templates.

**Q: Why two databases (PostgreSQL + MongoDB)?**
A: PostgreSQL for structured data that needs relationships (users, products). MongoDB for flexible, schema-less data like live market rates from external APIs where the structure can change.

**Q: How does JWT authentication work?**
A: User logs in → backend verifies password → creates JWT token with user_id and role → frontend stores token → every request sends token in header → backend verifies token on protected routes.

**Q: What is Kafka used for?**
A: Order processing. When a buyer places an order, it's sent to a Kafka topic. This decouples the order creation from order processing — the API responds immediately without waiting for order processing to complete.

**Q: What is an ORM?**
A: Object Relational Mapper. It lets you write Python classes instead of SQL queries. SQLAlchemy maps Python classes to database tables automatically.

**Q: What is CORS?**
A: Cross-Origin Resource Sharing. A security feature that controls which domains can make requests to your API. We configured it to allow requests from localhost:3000 (frontend).

**Q: Why use Docker?**
A: Docker packages the entire application with all its dependencies into containers. Anyone can run the project with one command (docker-compose up) without manually installing PostgreSQL, MongoDB, Kafka etc.

**Q: What is the difference between SQL and NoSQL?**
A: SQL (PostgreSQL) has fixed schema, tables, rows, supports complex joins and transactions. NoSQL (MongoDB) has flexible schema, stores JSON documents, better for unstructured or frequently changing data.

---

*Document created for AgroMart project by Yuvaraj*
*GitHub: https://github.com/Yuvaraj-varma/AgroMart*
