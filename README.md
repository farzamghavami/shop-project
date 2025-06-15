# 🛍 Shop Project (Django + Docker + PostgreSQL)

This project is a **back-end online store (E-commerce)** implemented with **Django**. It exclusively handles **back-end components** (without a Front-end) and utilizes **Docker Compose** for convenient setup and execution.

## 🔹 Tech Stack

- **Python (Django)** for back-end
- **Postgres** for the database
- **Docker Compose** for easy orchestration
- Separate **serializer**, **model**, **view**, and **url** files for each app
- **Docker** used within the Interpreter environment

## 🔹 Architectural Design

The project includes 4 separate apps, each with its own models, serializers, views, and URLs:

- **accounts** — User, Seller, and Admin management
- **catalog** — Product management
- **interactions** — Comments, likes, or customer interaction with sellers
- **orders** — Customer orders and payments

All automated tests are placed in a separate directory called `tests`.

The main project’s directory is **ecommerce**, which contains `settings.py`.

## 🔹 Roles and Permissions

The platform includes **3 roles with different permissions**:

- **Regular User**: Browsing and placing orders
- **Seller**: Adding and managing products
- **Admin**: Managing users, sellers, and products

Permissions are implemented and enforced within the `core` application.

## 🔹 Installation and Run

```bash
git clone https://github.com/farzamghavami/shop-project.git
cd shop-project
docker-compose up --build
Once up and running, you can access the API at http://localhost:8000.

🔹 Usage
Ability to add new models

API for integrating with a Front-end application

Pre-existing tests to validate functionality

🔹 Contributing
Contributions are welcome! Please submit a Pull Request with your improvements.

🔹 Project Tree
bash
Copy
Edit
.
├── __pycache__
├── accounts
│   └ (models, views, serializers, urls)
├── catalog
│   └ (models, views, serializers, urls)
├── core
│   └ (permissions, authentication, base settings)
├── ecommerce
│   └ settings.py
├── interactions
│   └ (models, views, serializers, urls)
├── orders
│   └ (models, views, serializers, urls)
└── tests
    └ (test files for apps)
✅ To add this README.md to your project:

Create a new README.md in your project’s root directory:

bash
Copy
Edit
touch README.md
Open it in your text editor:

bash
Copy
Edit
code README.md
Paste the content above into README.md.

Save the file — your project’s repository now includes a clear, helpful, and professional README.md.

✨ If you'd like, I can generate a downloadable ZIP file with this README.md for you. Just let me know! 🌟








