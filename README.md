# 🚀 DB Admin Portal

A **Role-Based Database Administration Portal** built using **Python, Streamlit, SQLAlchemy, MySQL, and PostgreSQL**.

The application provides a centralized interface for connecting to databases, dynamically exploring schemas, managing tables and records, controlling user permissions, maintaining audit logs, and interacting with databases using an **AI-powered natural language SQL assistant**.

---

## 📌 Features

### 🔐 Authentication & Authorization

* Secure Login System
* Password Hashing using `bcrypt`
* Session Management
* Role-Based Access Control (RBAC)
* User-specific permissions

### 👥 User Roles

#### Admin

* Full system access
* Manage users
* Manage permissions
* Insert, Update, Delete records
* View audit logs
* Connect to external databases

#### Editor

* View database records
* Insert records
* Update records
* Access based on assigned permissions

#### Viewer

* Read-only database access
* View tables and records
* Use permitted data analysis features

---

# 🗄️ Database Management

## 🔌 Multi-Database Connectivity

The portal supports connecting to different database systems dynamically.

### Currently Supported

* **MySQL**
* **PostgreSQL**
* **SQLite**
* **Snowflake**

The database connection interface allows users to provide database-specific connection details such as:

* Host
* Port
* Username
* Password
* Database Name
* Schema
* Warehouse
* Role
* Snowflake Account

The application creates the appropriate SQLAlchemy engine dynamically based on the selected database type.

---

## ☁️ PostgreSQL / Neon Support

The portal has been integrated with **PostgreSQL**, including cloud-hosted PostgreSQL databases such as **Neon**.

### PostgreSQL Configuration

```env
POSTGRES_HOST=your-neon-host
POSTGRES_PORT=5432
POSTGRES_DATABASE=your-database
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
POSTGRES_SSLMODE=require
```

Database credentials are stored using environment variables rather than being hardcoded in the application.

---

# 🔍 Dynamic Database Reflection

The application uses **SQLAlchemy reflection** to dynamically inspect connected databases.

It can detect:

* Tables
* Columns
* Data types
* Primary keys
* Database schema information

This eliminates the need to hardcode table structures.

### Workflow

```text
Connect Database
       ↓
Create SQLAlchemy Engine
       ↓
Test Connection
       ↓
Reflect Database Metadata
       ↓
Detect Tables
       ↓
Display Tables Dynamically
```

The same application interface can therefore work with different database schemas.

---

# 📝 CRUD Operations

The portal provides database administration functionality through a user-friendly Streamlit interface.

### Create

* Insert new records
* Dynamic forms based on table columns
* Supports multiple data types

### Read

* View database tables
* Browse records
* Search and filter data
* Pandas-based data display

### Update

* Select existing records
* Modify column values
* Update records through the interface

### Delete

* Select records
* Delete records securely
* Permission-based access

---

# 📊 Data Viewer

The Data Viewer provides dynamic database exploration.

### Features

* Dynamic table selection
* Automatic table detection
* Record browsing
* Search and filtering
* Pandas DataFrame integration
* Support for different database schemas

---

# 🔑 Permission Management

Administrators can manage table-level permissions.

Supported permissions:

```text
SELECT
INSERT
UPDATE
DELETE
```

Permissions are stored and enforced throughout the application based on the logged-in user's role.

---

# 📝 Audit Logging

The portal maintains an audit trail of important database activities.

Tracked activities include:

* User Login
* Record Insert
* Record Update
* Record Delete

Audit information can be used to track database administration activities and user actions.

---

# 🤖 AI Data Analyst

The portal includes an **AI-powered natural language to SQL assistant**.

Users can ask questions about their connected database using natural language instead of manually writing SQL queries.

### Example Queries

```text
Show top 5 highest salary employees

Average salary by department

Show the highest paid employee

How many active users exist?

Show employees earning more than 50000
```

---

## 🧠 AI SQL Workflow

```text
User Question
      ↓
Connected Database
      ↓
Database Schema Reflection
      ↓
Schema Information
      ↓
OpenRouter LLM
      ↓
Generated SQL
      ↓
SQL Validation
      ↓
User Confirmation
      ↓
Query Execution
      ↓
Result Display
      ↓
AI Explanation
```

The AI assistant uses the schema of the currently connected database to generate context-aware SQL queries.

---

# 🛡️ AI Security Layer

The AI SQL assistant includes SQL validation before query execution.

For read-only AI operations, modification commands are blocked.

### Blocked Commands

```sql
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
```

Only validated read queries such as `SELECT` are permitted through the AI analysis workflow.

This prevents the AI assistant from directly modifying or destroying database data.

---

# 🔗 Database Connection Architecture

The application uses a centralized database connection manager.

```text
                 DB Admin Portal
                       │
                       ↓
              Database Connection
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
      MySQL        PostgreSQL       SQLite
        │              │
        │              ↓
        │            Neon
        │
        └──────────────┐
                       ↓
                SQLAlchemy Engine
                       ↓
             Database Reflection
                       ↓
              Application Modules
```

---

# 🛠️ Tech Stack

| Technology     | Usage                          |
| -------------- | ------------------------------ |
| Python 3.11    | Application Backend            |
| Streamlit      | Web Interface                  |
| SQLAlchemy     | Database Connectivity & ORM    |
| MySQL 8.0      | Relational Database            |
| PostgreSQL     | Relational Database            |
| Neon           | Cloud PostgreSQL               |
| SQLite         | Lightweight Database Support   |
| Snowflake      | Cloud Data Warehouse Support   |
| Pandas         | Data Processing & Data Display |
| bcrypt         | Password Hashing               |
| Requests       | API Communication              |
| OpenRouter API | AI SQL Generation              |
| OpenPyXL       | Excel Processing               |
| Git & GitHub   | Version Control                |

---

# 📂 Project Structure

```text
DB_Admin_Portal/
│
├── app.py
│
├── auth/
│   ├── login.py
│   ├── permissions.py
│   └── session.py
│
├── database/
│   ├── connection.py
│   ├── connection_manager.py
│   ├── reflection.py
│   ├── models.py
│   ├── session.py
│   └── base.py
│
├── crud/
│   ├── create.py
│   ├── read.py
│   ├── update.py
│   └── delete.py
│
├── views/
│   ├── dashboard.py
│   ├── database_connection.py
│   ├── tables_page.py
│   ├── data_viewer.py
│   ├── insert_page.py
│   ├── update_page.py
│   ├── delete_page.py
│   ├── users_page.py
│   ├── permissions_page.py
│   ├── logs_page.py
│   └── ai_chat_page.py
│
├── ai/
│   ├── openrouter_client.py
│   ├── sql_generator.py
│   └── sql_validator.py
│
├── services/
│   ├── logging_service.py
│   ├── export_service.py
│   ├── bulk_service.py
│   └── table_service.py
│
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/vaishnavish1307/ai-database-admin-portal.git

cd ai-database-admin-portal
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configure Environment Variables

Create a `.env` file in the project root.

```env
# MySQL
DB_HOST=localhost
DB_PORT=3306
DB_NAME=db_admin_portal
DB_USER=root
DB_PASSWORD=your_password

# PostgreSQL / Neon
POSTGRES_HOST=your-neon-host
POSTGRES_PORT=5432
POSTGRES_DATABASE=your-database
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
POSTGRES_SSLMODE=require

# AI
OPENROUTER_API_KEY=your_api_key
```

### ⚠️ Security

**Never commit `.env` to GitHub.**

Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

Use `.env.example` to document the required environment variables without exposing actual credentials.

---

# ▶️ Run the Application

Activate the virtual environment and run:

```bash
streamlit run app.py
```

The application will be available locally at:

```text
http://localhost:8501
```

---

# 🔄 Current Progress

| Module                       | Status         |
| ---------------------------- | -------------- |
| Authentication               | ✅ Completed    |
| Session Management           | ✅ Completed    |
| Role Management              | ✅ Completed    |
| Permission Management        | ✅ Completed    |
| MySQL Connectivity           | ✅ Completed    |
| PostgreSQL Connectivity      | ✅ Completed    |
| Neon PostgreSQL Connectivity | ✅ Completed    |
| SQLite Support               | ✅ Completed    |
| Snowflake Connection Support | ✅ Implemented  |
| Dynamic Database Reflection  | ✅ Completed    |
| Dynamic Table Detection      | ✅ Completed    |
| Data Viewer                  | ✅ Completed    |
| Insert Module                | ✅ Completed    |
| Update Module                | ✅ Completed    |
| Delete Module                | ✅ Completed    |
| User Management              | ✅ Completed    |
| Audit Logging                | ✅ Completed    |
| AI SQL Generation            | ✅ Completed    |
| SQL Validation               | ✅ Completed    |
| AI Query Execution           | ✅ Completed    |
| AI Result Explanation        | 🚧 In Progress |
| Excel Export                 | 🚧 In Progress |
| Bulk Operations              | 🚧 In Progress |

---

# 🎯 Future Enhancements

* Excel Export
* CSV Export
* Bulk Insert
* Bulk Update
* Bulk Delete
* Data Visualization Dashboard
* Query History
* Saved Reports
* Database Backup & Restore
* AI Insights Dashboard
* Query Performance Monitoring
* Advanced Database Analytics
* Additional Cloud Database Integrations

---

# 🔒 Security Considerations

The application follows several security practices:

* Password hashing using bcrypt
* Role-Based Access Control
* Table-level permissions
* SQL validation
* Read-only AI query restrictions
* Environment-based credential management
* Database connection testing before use
* Audit logging of important operations

Database credentials and API keys should always be stored outside the source code using environment variables or deployment-platform secrets.

---

# 🚀 Project Highlights

### Dynamic Database Connectivity

Connect to different database systems through a single administration portal.

### AI-Powered SQL Assistant

Convert natural language questions into SQL queries using an LLM while applying SQL validation before execution.

### Role-Based Database Administration

Provide different levels of access to administrators, editors, and viewers.

### Dynamic Schema Reflection

Automatically detect tables and database structures without hardcoded schemas.

### Secure Database Operations

Combine permissions, SQL validation, and audit logging to provide controlled database administration.

---

⭐ If you found this project useful, don't forget to star the repository!
