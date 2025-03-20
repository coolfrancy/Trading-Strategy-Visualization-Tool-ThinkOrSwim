from flask import Flask, render_template, request, url_for, redirect
import sys
import os

#path to TosChart for importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

from TosChart.cleaner.cleaner import wash
from TosChart.cleaner.erase import clean_folder
from TosChart.visual import data

app=Flask(__name__)

#where the cleaned and uncleaned data is being stored
uncleaned_data_path='/workspaces/TosChartWeb/TosChart/uncleaned_data'
cleaned_data_path='/workspaces/TosChartWeb/TosChart/cleaned_data'

#home page allows you to add files
@app.route('/')
def home():
    return render_template('home.html')

#shows chart
@app.route('/clean_files', methods=['GET', 'POST'])
def clean_files():
    #deletes data from folder so prev data dont effect new chart
    clean_folder(uncleaned_data_path)
    clean_folder(cleaned_data_path)

    #to make sure the user imported a file
    if 'cfile' not in request.files:
        return 'No file was given'

    
    #shows all the files currently in folder
    multi_file=request.files.getlist('cfile')

    for file in multi_file:
        if file.filename=='' or 'desktop.ini' in file.filename:
            continue

        #adds file to uncleaned_data folder
        os.makedirs(uncleaned_data_path, exist_ok=True)
        file_name=os.path.basename(file.filename)
        file_path=os.path.join(uncleaned_data_path, file_name)
        file.save(file_path)
    
    #clean files
    wash(uncleaned_data_path, cleaned_data_path)

    return redirect(url_for('chart'))

@app.route('/chart')
def chart():
    info=data(cleaned_data_path)
    return render_template('chart.html', info=info)

    

if __name__=='__main__':
    app.run(debug=True, port=5002)