from flask import Flask, render_template, request
import os


app=Flask(__name__)

#home page allows you to add files
@app.route('/')
def home():
    return render_template('home.html')

#shows chart
@app.route('/chart', methods=['GET', 'POST'])
def chart_view():
    if 'cfile' not in request.files:
        return 'No file was given'
    
    file=request.files['cfile']

    if file.filename=='':
        return ' No selected file'
    os.makedir('/workspaces/TosChartWeb/web', exit_ok=True)
    file_path=os.path.join('/workspaces/TosChartWeb/web', file.filename)
    file.save(file_path)
    return 'file saved'
    

if __name__=='__main__':
    app.run(debug=True, port=5001)