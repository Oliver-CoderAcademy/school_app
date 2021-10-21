from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/students/')
def view_students():
    return 'This page will display a list of all students.'

if __name__ == '__main__':
    app.run(debug=True)  