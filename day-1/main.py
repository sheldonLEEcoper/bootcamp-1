from flask import Flask , render_template
app = Flask(__name__)

@app.route('/', methods=['GET']) # / = http://127.0.0.1:5000/
def home():
    return render_template('home.html')

@app.route('/page1' ,  methods=['GET'])
def page1():
    return render_template ('page1.html')

@app.route('/page2' ,  methods=['GET'])
def page2():
    return render_template ('page2.html')

@app.route('/page3' ,  methods=['GET'])
def page3():
    return render_template ('page3.html')


if __name__ == '__main__':
    app.debug= True
    app.run()


