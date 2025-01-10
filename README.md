# Database Visualization
This project is a web application for visualizing and managing a database, 
implemented with a Python (Flask) backend and a frontend built with HTML, CSS, and JavaScript.

## Features

- **View and manipulate table data**: Add and delete records.
- **Predefined Queries**:
  - Simple queries (e.g., list models and their mentors).
  - Complex queries with subqueries and dynamic parameters.
- **Interactive and dynamic design**: JavaScript for real-time data display.

## Project Structure

- **Backend**: Flask
  - File: `backend.py`
  - Features:
    - Routes for simple and complex queries.
    - Routes for data manipulation (add, delete).
    - Connection to a MySQL database.

- **Frontend**: HTML, CSS, JavaScript
  - Files:
    - `index.html`: Web application structure.
    - `main.js`: Dynamic functionality and interaction with the backend API.
    - `style.css` (optional): Styling the interface (can be added later).

- **Database**:
  - The database structure is defined by the following tables:
    - `Model`, `Mentor`, `Competitie`, `Jurat`, etc.
  - Relationships between tables ensure data integrity.

## Author

This project was developed to facilitate understanding of table relationships and data manipulation in a relational database due to a uni project.



