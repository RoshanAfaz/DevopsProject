# Project Documentation: Multi-Service Dockerized App

This project demonstrates a production-like microservices architecture using Docker Compose.

## Project Structure
```text
/college/devopsproject
├── backend/
│   ├── app.py             # Flask API with DB connection
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Python environment
├── frontend/
│   ├── server.js          # Node.js server
│   ├── public/
│   │   └── index.html     # Premium UI dashboard
│   ├── package.json       # Node dependencies
│   └── Dockerfile         # Node environment
├── mysql/
│   └── init.sql           # Database schema & seed data
└── docker-compose.yml     # Orchestration file
```

## Key Features
- **Frontend**: A modern, responsive dashboard built with semantic HTML and CSS. It communicates with the backend via the browser.
- **Backend**: A Flask REST API that provides system status and database connectivity details.
- **Database**: A MySQL instance that automatically initializes with a `users` table and sample data.
- **Orchestration**: Uses `docker-compose` with health checks and `depends_on` to ensure the database is ready before the backend starts.

## How to Build and Run

### 1. Prerequisites
- Docker and Docker Compose installed.

### 2. Configure Environment Secrets
Create a `.env` file in the root directory (or use the existing one) with these values:
```text
DB_ROOT_PASSWORD=your_root_password
DB_NAME=test_db
DB_USER=dev_user
DB_PASSWORD=secure_password123
DB_HOST=db
```
> [!WARNING]
> Never commit your `.env` file to public source control like GitHub. Add it to your `.gitignore` file immediately.

### 3. Build and Start the Services
Run the following command in the root directory:
```bash
docker-compose up --build
```

### 3. Access the Application
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:5000](http://localhost:5000)
- **Backend DB Status**: [http://localhost:5000/db](http://localhost:5000/db)

### 4. Useful Commands
- **Stop services**: `docker-compose down`
- **View logs**: `docker-compose logs -f`
- **Rebuild specific service**: `docker-compose build <service_name>`
