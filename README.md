Blocky — Simple, Modern Database Development
Blocky is a lightweight, developer‑friendly toolkit designed to simplify database development. It provides a clean, intuitive interface for building, testing, and visualizing database structures without unnecessary complexity.

Project Goal
The goal of Blocky is to create an easy, accessible solution for database development. The project focuses on reducing friction, improving clarity, and offering a modern workflow for anyone working with databases, whether they are beginners or experienced developers.

Features
Visual database builder for designing tables and relationships

Simple schema editing and testing tools

Clean and responsive user interface

Session‑based authentication for secure access

Admin panel for privileged operations

API endpoints for automation and external integration

Lightweight Flask backend designed for extensibility

Technology Stack
Python (Flask)

SQLite / MySQL / PostgreSQL

HTML, CSS, JavaScript

Jinja2 templating

Session-based authentication

Security
Blocky follows secure development practices, including:

Environment-based configuration

Secret keys stored outside version control

Protected admin routes

Session cookies for authentication

Clear project structure for safe collaboration

Project Structure

Blocky/
│
├── app/
│   ├── routes.py
│   ├── auth.py
│   ├── models.py
│   ├── templates/
│   └── static/
│
├── instance/
│   └── database.db
│
├── .gitignore
├── README.md
└── requirements.txt

Future Plans
Advanced admin dashboard

Drag‑and‑drop schema designer

Live database preview

Import and export tools

Dark mode

Cloud synchronization options

Contributing
Contributions are welcome. If you have suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License.
