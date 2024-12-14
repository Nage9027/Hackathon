from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
import mysql.connector
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL database configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saimani@7",  # Ensure to URL encode special characters if needed
    database="login_system"
)

mycursor = mydb.cursor()

UPLOAD_FOLDER = 'uploads/resources'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allow only specific file extensions (PDF in this case)
ALLOWED_EXTENSIONS = {'pdf'}

# Function to check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def home():
    return render_template('index.html')


# Email configuration
sender_email = "risenmusic2@gmail.com"  # Your Gmail address
password = "lrmrqfuwwwudzlpb"  # Newly generated app-specific password
smtp_server = "smtp.gmail.com"
smtp_port = 587  # TLS port

@app.route('/send_email', methods=['POST'])
def send_email():
    recipient_email = request.form['email']  # Get the recipient email from the form
    message = request.form['message']  # Get the message from the form

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Message from Your Flask App"
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Establish a connection to the Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()  # Send the EHLO command to the server
        server.starttls()  # Start TLS encryption
        server.ehlo()  # Re-send EHLO after starting TLS

        # Log in with your email and app-specific password
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())  # Send the email
        server.quit()  # Close the connection
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email. Error: {str(e)}"

@app.route('/category')
def category():
    return render_template('category.html')
@app.route('/projects')
@app.route('/projects', methods=['GET', 'POST'])
def projects():
    correct_password = 123456  # Define the correct password
    
    if request.method == 'POST':
        try:
            entered_password = int(request.form.get('password'))  # Get the entered password
            if entered_password == correct_password:
                return render_template('project.html')  # Render the protected page
            else:
                return "Error: Incorrect password!"  # Show an error message
        except ValueError:
            return "Error: Invalid password format!"  # Handle case where input is not an integer
    
    # Render the password input form on GET request
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Prompt</title>
        </head>
        <body>
            <h1>Enter Password to Access Projects</h1>
            <form method="POST">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
    '''

@app.route('/upload_project', methods=['GET', 'POST'])
def upload_project():
    if request.method == 'POST':
        project_file = request.files['project_file']

        if project_file and allowed_file(project_file.filename):
            filename = project_file.filename
            project_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Ensure the upload folder exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            project_file.save(project_path)
            flash(f'Project file {filename} uploaded successfully!', 'success')

        else:
            flash('Invalid file format. Only PDF files are allowed.', 'danger')

    # List all project files (PDFs in the upload folder)
    project_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    return render_template('project_upload.html', project_files=project_files)

@app.route('/analyze_textfile', methods=['POST'])
def analyze_textfile():
    textfile_name = request.form['textfile_name']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], textfile_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        flash('Text file not found.', 'danger')
        return redirect(url_for('view_textfiles'))

    # Extract text from the text file using the function
    text = extract_text_from_txt(file_path)

    # Summarize the extracted text
    summary = summarize_text(text)

    # Render the page with the summary
    return render_template('view_uploadedtxt.html', text_files=os.listdir(app.config['UPLOAD_FOLDER']), summary=summary, textfile_name=textfile_name)



@app.route('/view_textfiles')
def view_textfiles():
    text_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('view_uploadedtxt.html', text_files=text_files)
def extract_text_from_txt(file_path):
    """Extract text from a .txt file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def summarize_text(text):
    """Summarize text (can use spaCy or another summarization method)."""
    # For demonstration, just return the first few lines of the text
    return '\n'.join(text.split('\n')[:3])  # Limit to the first 3 lines


@app.route('/view_pdfs')
def view_pdfs():
    # List all PDF files in the upload folder
    pdf_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    return render_template('view_uploadedpdf.html', pdf_files=pdf_files)

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        mycursor.execute("SELECT * FROM login WHERE email = %s", (email,))
        existing_user = mycursor.fetchone()

        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('home'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        mycursor.execute("INSERT INTO login (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mydb.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('home'))

@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        mycursor.execute("SELECT * FROM login WHERE email = %s", (email,))
        user = mycursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid email or password. Please try again.', 'danger')
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('home'))
    
    # Pass the image URL to the template
    background_image_url = url_for('static', filename='videos/pretty-sky.gif')
    return render_template('dashboard.html', background_image_url=background_image_url)

@app.route('/join_project')
def join_project():
    return render_template('join.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('dashboard'))

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('dashboard'))

    if pdf_file and allowed_file(pdf_file.filename):
        # Save the file to the specified upload folder
        filename = pdf_file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        pdf_file.save(file_path)
        flash(f'File {filename} uploaded successfully!', 'success')
        return redirect(url_for('view_pdfs'))  # Redirect to the view_pdfs route after upload

    flash('Invalid file format. Only PDF files are allowed.', 'danger')
    return redirect(url_for('dashboard'))

# Route to serve a specific PDF file
@app.route('/uploads/resources/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Initialize database (checking if table exists)
@app.before_request
def create_tables():
    mycursor.execute("SHOW TABLES LIKE 'login'")
    result = mycursor.fetchone()
    if not result:
        mycursor.execute('''CREATE TABLE login (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(80) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL
        )''')
        mydb.commit()

if __name__ == '__main__':
    app.run(debug=True)
