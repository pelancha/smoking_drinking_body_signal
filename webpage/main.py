from flask import Flask
from flask import url_for, render_template, request


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    user = "Ученик Яндекс.Лицея"
    return render_template('index.html', title='Домашняя страница',
                           username=user)



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
