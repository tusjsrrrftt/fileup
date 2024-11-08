# FileUp - Simple File Upload and Sharing Application

FileUp is a Flask-based web application that allows users to upload files and share them via a public URL. It uses SSH tunneling to make the application accessible from the internet.

## Features

- File upload and storage
- File download via public URL
- Automatic SSH tunnel setup for public access
- Periodic SSH tunnel restart to maintain connection

## Project Structure
fileup/
│
├── app.py
├── launch.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   └── error.html
│
└── uploads/
    └── (uploaded files will be stored here)