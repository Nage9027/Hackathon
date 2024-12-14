This directory contains all the HTML templates used by the Flask application. The templates are built using Flask's Jinja2 templating engine, allowing dynamic content rendering and seamless integration with backend logic.

List of Templates and Descriptions
1. index.html
Purpose: Serves as the landing page of the application.
Features:
Links to login, signup, and other sections.
Provides a welcoming interface for users.
2. dashboard.html
Purpose: Displays the user dashboard after login.
Features:
Dynamically renders user-specific content, such as uploaded files or project details.
Includes support for customizable backgrounds (e.g., videos or images).
3. category.html
Purpose: Organizes content into different categories for better navigation.
Features:
Acts as a hub for exploring various features of the application.
4. project.html
Purpose: Lists student projects and requires a password for access.
Features:
Securely displays project details.
Renders a form for password input and validation.
5. project_upload.html
Purpose: Handles PDF file uploads for student projects or resources.
Features:
Allows users to upload PDF files.
Displays a list of previously uploaded files.
6. view_uploadedtxt.html
Purpose: Displays a list of uploaded .txt files and their summaries.
Features:
Summarizes text files using backend logic.
Provides an intuitive interface for viewing text analysis results.
7. view_uploadedpdf.html
Purpose: Lists uploaded PDF files for easy access and download.
Features:
Renders links to download the files.
Organizes uploaded files in a user-friendly format.
8. join.html
Purpose: Provides an interface for users to join discussions or collaborative projects.
Features:
Acts as a placeholder for future enhancements in collaboration tools.
9. password_prompt.html (Inline in project.html)
Purpose: A simple form to collect a password before granting access to secure sections.
Features:
Validates user input and restricts unauthorized access.
Key Features of Templates
Dynamic Content:

Integrates with Flask backend to display real-time data.
Uses Jinja2 syntax ({{ }} and {% %}) for loops, conditions, and data rendering.
Reusability:

Common UI components like headers, footers, and navigation bars are consistent across templates.
Responsive Design:

Ensures templates are mobile-friendly using CSS flexbox and media queries.
Interactive Forms:

Implements forms for login, signup, file uploads, and text analysis.
Provides feedback messages for user actions.
Usage Instructions
Place all the .html files in the templates folder of your Flask project.
Use Flask's render_template method to serve these templates:
python
Copy code
from flask import render_template

@app.route('/')
def home():
    return render_template('index.html')
Ensure dynamic elements like URLs and file paths are passed correctly from the backend:
python
Copy code
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', background_image_url=url_for('static', filename='images/bg.jpg'))
