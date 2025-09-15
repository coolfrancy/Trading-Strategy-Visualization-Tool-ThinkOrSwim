from flask import Flask, render_template, request, url_for, redirect, session, send_from_directory
from dotenv import load_dotenv
import sys
import os
from datetime import datetime, timedelta

load_dotenv()

# Path to TosChart for importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TosChart.cleaner.cleaner import wash
from TosChart.cleaner.erase import clean_folder
from TosChart.visual import data

# Configuration
SESSION_TIMEOUT_MINUTES = 30
INVALID_FILES = ['desktop.ini', '']

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('app_secret_key')
app.permanent_session_lifetime = timedelta(minutes=SESSION_TIMEOUT_MINUTES)

# File paths
UNCLEANED_DATA_PATH = os.path.join(os.getcwd(), 'TosChart', 'uncleaned_data')
CLEANED_DATA_PATH = os.path.join(os.getcwd(), 'TosChart', 'cleaned_data')
UNCLEANED_PHASES_PATH = os.path.join(os.getcwd(), 'TosChart', 'phases', 'uncleaned_phases_data')
CLEANED_PHASES_PATH = os.path.join(os.getcwd(), 'TosChart', 'phases', 'cleaned_phases_data')


def clear_all_folders():
    """Clear all data folders to prevent previous data from affecting new charts."""
    folders_to_clear = [
        UNCLEANED_DATA_PATH,
        CLEANED_DATA_PATH,
        UNCLEANED_PHASES_PATH,
        CLEANED_PHASES_PATH
    ]
    
    for folder in folders_to_clear:
        clean_folder(folder)


def is_valid_file(file):
    """Check if uploaded file is valid (not empty and not a system file)."""
    return file.filename != '' and 'desktop.ini' not in file.filename


def save_uploaded_files(files, destination_path):
    """Save uploaded files to specified destination path."""
    os.makedirs(destination_path, exist_ok=True)
    
    for file in files:
        if not is_valid_file(file):
            continue
            
        file_name = os.path.basename(file.filename)
        file_path = os.path.join(destination_path, file_name)
        file.save(file_path)


def has_valid_files(files):
    """Check if file list contains any valid files."""
    return files and any(is_valid_file(file) for file in files)


def process_phase_files(phase_files):
    """Process phase files and return appropriate phases path."""
    if not has_valid_files(phase_files):
        return ''
    
    save_uploaded_files(phase_files, UNCLEANED_PHASES_PATH)
    os.makedirs(CLEANED_PHASES_PATH, exist_ok=True)
    wash(UNCLEANED_PHASES_PATH, CLEANED_PHASES_PATH)
    
    return CLEANED_PHASES_PATH


def process_main_files(main_files):
    """Process main trading files."""
    if not has_valid_files(main_files):
        return False
    
    save_uploaded_files(main_files, UNCLEANED_DATA_PATH)
    os.makedirs(CLEANED_DATA_PATH, exist_ok=True)
    wash(UNCLEANED_DATA_PATH, CLEANED_DATA_PATH)
    
    return True


@app.route('/')
def home():
    """Home page - allows users to upload files."""
    clear_all_folders()
    session.clear()
    return render_template('home.html')


@app.route('/clean_files', methods=['GET', 'POST'])
def clean_files():
    """Process uploaded files and generate chart analysis."""
    clear_all_folders()
    
    # Get uploaded files
    main_files = request.files.getlist('cfile')
    phase_files = request.files.getlist('pfile')
    
    # Validate main files
    if 'cfile' not in request.files:
        return 'No file was given', 404
    
    if not has_valid_files(main_files):
        return 'No valid files uploaded', 400
    
    # Process main files
    if not process_main_files(main_files):
        return 'Failed to process main files', 500
    
    # Process phase files (optional)
    phases_path = process_phase_files(phase_files)
    
    # Generate analysis summary
    try:
        summary = data(CLEANED_DATA_PATH, phases_path)
        session['summary'] = summary
    except ValueError as e:
        return f'No ThinkOrSwim csv file found: {e}'
    
    return redirect(url_for('chart'))


@app.route('/chart')
def chart():
    """Display the generated chart with analysis summary."""
    summary = session.get('summary')
    
    if summary:
        return render_template('chart.html', summary=summary)
    else:
        return 'No ThinkOrSwim csv file found: No summary available'

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory(app.root_path, 'ads.txt')

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    return "Something went wrong, Please try again.", 500


@app.errorhandler(404)
def not_found_error(error):
    """Handle page not found errors."""
    return "Page not found.", 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)