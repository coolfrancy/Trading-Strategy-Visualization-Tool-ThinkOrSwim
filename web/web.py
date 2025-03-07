from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chart', methods=['GET', 'POST'])
def chart_view():
    if request.method=="POST":
        chart_files=request.files['cfile']
        return f'got file {chart_files.filename}'
    else:
        return 'wtf is going on'
if __name__=='__main__':
    app.run(debug=True, port=5001)