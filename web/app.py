from flask import Flask, render_template, request, url_for, redirect, session
from dotenv import load_dotenv
import sys
import os

load_dotenv()
#path to TosChart for importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

from TosChart.cleaner.cleaner import wash
from TosChart.cleaner.erase import clean_folder
from TosChart.visual import data
from datetime import datetime, timedelta

app=Flask(__name__)
app.secret_key = os.getenv('app_secret_key')

# Session configuration
SESSION_TIMEOUT_MINUTES = 30  # 30 minutes timeout
app.permanent_session_lifetime = timedelta(minutes=SESSION_TIMEOUT_MINUTES)

#where the cleaned and uncleaned data is being stored

uncleaned_data_path = os.path.join(os.getcwd(), 'TosChart', 'uncleaned_data')
cleaned_data_path = os.path.join(os.getcwd(), 'TosChart', 'cleaned_data')


#home page allows you to add files
@app.route('/')
def home():
    #deletes data from folder so prev data dont effect new chart
    clean_folder(uncleaned_data_path)
    clean_folder(cleaned_data_path)
    session.clear()

    return render_template('home.html')

#shows chart
@app.route('/clean_files', methods=['GET', 'POST'])
def clean_files():
    #deletes data from folder so prev data dont effect new chart
    clean_folder(uncleaned_data_path)
    clean_folder(cleaned_data_path)


    #to make sure the user imported a file
    if 'cfile' not in request.files:
        return 'No file was given', 404

    
    #shows all the files currently in folder
    multi_file=request.files.getlist('cfile')
    if not multi_file or all(file.filename == '' for file in multi_file):
        return 'No valid files uploaded', 400

    for file in multi_file:
        if file.filename=='' or 'desktop.ini' in file.filename:
            continue #skips invalid files

        #adds file to uncleaned_data folder
        os.makedirs(uncleaned_data_path, exist_ok=True)
        # Create the cleaned data directory if it doesn't exist
        os.makedirs(cleaned_data_path, exist_ok=True)

        file_name=os.path.basename(file.filename)
        file_path=os.path.join(uncleaned_data_path, file_name)
        file.save(file_path)

    #clean files
    wash(uncleaned_data_path, cleaned_data_path)

    #summary of files
    try:
        summary=data(cleaned_data_path)
        session['summary'] = summary
    except ValueError as e:
        return f'No ThinkOrSwim csv file found : {e}'

    return redirect(url_for('chart'))

@app.route('/chart')
def chart():
    summary=session.get('summary')
    if summary:
        return render_template('chart.html', summary=summary)
    else:
        return f'No ThinkOrSwim csv file found : {e}'
        

    
@app.errorhandler(500)
def internal_error(error):
    return "Something went wrong, Please try again.", 500

@app.errorhandler(404)
def not_found_error(error):
    return "Page not found.", 404

if __name__=='__main__':
    app.run(debug=True, port=5002)