# 📋 Webinar Registration App

A Streamlit web application for webinar registration with email validation and MySQL database integration.

## Features

✅ **Dropdown selection** of available webinars  
✅ **Email validation** - ensures valid email format  
✅ **User information** - captures first name, last name, and phone number  
✅ **Database storage** - saves all registrations to MySQL  
✅ **Form validation** - validates all inputs before submission  
✅ **Beautiful UI** - clean, responsive interface built with Streamlit  

## Prerequisites

- Python 3.8+
- MySQL Server installed and running
- pip (Python package manager)

## Setup Instructions

### 1. Install Required Packages

The packages have already been installed. They include:
- `streamlit` - Web framework
- `pymysql` - MySQL database connector
- `email-validator` - Email validation
- `python-dotenv` - Environment variable management

### 2. Set Up the Database

**Option A: Using MySQL Command Line**

```bash
mysql -u root -p < setup_database.sql
```

**Option B: Using MySQL Workbench or phpMyAdmin**

1. Create a new database called `webinar_db`
2. Copy and paste the contents of `setup_database.sql` and execute

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your MySQL credentials:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=webinar_db
   ```

### 4. Run the Application

```bash
streamlit run webinar_registration.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Select a Webinar** - Choose from the dropdown list
2. **Enter Email** - Must be a valid email format
3. **Enter Name** - Provide first and last name
4. **Enter Phone** - Valid 10-digit (or 11 with country code) phone number
5. **Click Register** - Submit and view confirmation

## Form Validation

- ✅ Email must be in valid format (e.g., user@example.com)
- ✅ All fields are required
- ✅ Phone must be 10 digits (or 11 starting with 1)
- ✅ Email must be unique (no duplicates)

## Database Schema

### `registrations` table:
```
id (PRIMARY KEY)
webinar (VARCHAR)
email (VARCHAR, UNIQUE)
first_name (VARCHAR)
last_name (VARCHAR)
phone (VARCHAR)
registration_date (TIMESTAMP)
```

### `webinars` table (optional):
```
id (PRIMARY KEY)
title (VARCHAR)
description (TEXT)
date (DATETIME)
max_attendees (INT)
created_at (TIMESTAMP)
```

## Troubleshooting

**"Database connection error"**
- Ensure MySQL is running
- Check your `.env` credentials
- Verify the `webinar_db` database exists

**"Email already registered"**
- This email has already registered for a webinar
- Use a different email address

**"Invalid phone number"**
- Ensure phone is 10 digits (or 11 starting with 1)
- Remove all formatting characters, just use digits

## Deployment

To deploy publicly (optional):

1. **Streamlit Cloud** (Free tier available):
   - Push your code to GitHub
   - Create account at https://streamlit.io/cloud
   - Deploy directly from your GitHub repo

2. **Railway.app** (Generous free tier):
   - Deploy from GitHub using Railway
   - Set environment variables in Railway dashboard

3. **PythonAnywhere**:
   - Upload files to PythonAnywhere
   - Configure MySQL connection
   - Deploy as WSGI app

## File Structure

```
.env                          # Environment variables (not in git)
.env.example                  # Template for environment variables
webinar_registration.py       # Main Streamlit application
setup_database.sql            # Database setup script
README.md                     # This file
```

## License

MIT License - Feel free to modify and use as needed.
