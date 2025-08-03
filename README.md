# checklist-app-api

This is the backend API for a checklist management application. It is built using **FastAPI**, **SQLAlchemy**, and **MySQL**. 
The API provides endpoints for creating, retrieving, updating, and deleting checklists and their associated items.

> ⚠️ This project is currently under active development. Planned features include the addition of users and a controller-service-data layer architecture for better modularity and maintainability.

---

## Features
- Create and manage checklists
- Add, update, retrieve, and delete checklist items
- FastAPI with Pydantic models for request/response validation
- Relational data modeling using SQLAlchemy ORM
- CORS configured to support frontend development on localhost:3000

---

## Tech Stack

- **Language**: Python
- **API Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: MySQL

---

## Getting Started
### Prerequisites

Before running the application, please make sure these are installed:

- **pip** (Python package manager)
- **Python 3.10+**
- **MySQL** 
- An IDE such as **IntelliJ IDEA Ultimate** or **VS Code**

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/spechotta/checklist-app-api.git

2. **Create and configure a virtual environment:**

   - If you're using IntelliJ IDEA Ultimate, you can create a virtual environment when setting up the project.
   - Alternatively, you may create a virtual environment manually using the following instructions: https://docs.python.org/3/library/venv.html.


3. **Install required dependencies manually:**

   ```bash
   pip install fastapi pymysql sqlalchemy uvicorn python-dotenv

4. **Create a `.env` file in the project root directory with the following content:**

   ```env
   DATABASE_URL = "mysql+pymysql://<username>:<password>@localhost:3306/<your database name>"
   ```
   
   Replace `<username>`, `<password>`, and `<your database name>` with your own MySQL username, password, and the name of the database you've created for this application.


5. **Run the application:**

    - From the terminal:
    ```bash
    uvicorn app.main:app --reload
    ```
    - Alternatively, you may create a run/debug configuration within IntelliJ to run the application.


6. **Access the API documentation in your browser:**

    - **Swagger UI**: http://localhost:8000/docs#
   