# KanMind Backend

KanMind Backend is a Django REST Framework–based backend application developed to support a JavaScript frontend project.  
The backend was designed, implemented, and structured after the frontend was completed, with a clear focus on clean API design, scalability, and maintainability.

This project follows a modular, feature-based architecture and provides authentication, board management, and task management functionality via RESTful APIs.

---

## 🚀 Tech Stack

- **Backend Framework:** Django, Django REST Framework
- **Language:** Python
- **Authentication:** Token-based authentication
- **Database:** SQLite (development)
- **API Style:** REST
- **Tooling:** Django ORM, Migrations, Environment-based settings

---

## 🧩 Project Structure

KanMind_Backend/
├── core/ # Project settings, URLs, ASGI/WSGI
├── authentication/ # Custom user model & authentication logic
├── boards/ # Board domain logic
├── tasks/ # Task domain logic
├── manage.py
├── requirements.txt
├── README.md

Each domain (authentication, boards, tasks) is encapsulated in its own Django app to ensure separation of concerns and long-term scalability.

---

## 🔐 Authentication

- Custom user model
- Token-based authentication
- Secure access control for protected endpoints
- Ownership-based permissions for boards and tasks

---

## 📋 Boards

Boards represent containers for organizing tasks.

**Features:**

- Create, update, delete boards
- Board ownership validation
- Authenticated access only

---

## ✅ Tasks

Tasks belong to boards and represent actionable items.

**Features:**

- Full CRUD functionality
- Relation to boards
- Validation and permission checks
- Filtering and ordering support

---

## 🌐 API Design Principles

- RESTful endpoint structure
- Clear separation between serializers, views, and models
- Validation logic handled at serializer level
- Permission checks enforced at view level
- Modular and readable codebase

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd KanMind_Backend
```

## 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Apply migrations

```bash
python manage.py migrate
```

## 5. Run development server

```bash
python manage.py runserver
```

🔗 Frontend Integration

This backend was built to integrate with an existing JavaScript frontend application.
CORS and authentication mechanisms are configured to support secure frontend-backend communication.

🧪 Development Notes

Environment-specific settings are supported

Database can be easily switched for production usage

Codebase structured for extensibility and testing

📌 Status

✔ Backend implementation completed
✔ All core features functional
✔ Ready for further extension (testing, deployment, production hardening)

👤 Author

Developed by `Ogulcan Erdag`
Full-Stack Developer with a strong focus on backend architecture and clean API design.

---
