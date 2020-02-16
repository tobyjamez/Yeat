from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def search():
    return render_template('dynamic_input.html', title='Enter your ingredients!')


@app.route('/results', methods = ['GET', 'POST'])
def results():
    if request.method == 'GET':
        return redirect(url_for('/'))
    else:
        food_list = request.form.getlist('input_text[]')  # list of foods input by user
        return render_template('dynamic_input_results.html', values=food_list, title='Recipe name')


if __name__ == '__main__':
    app.run(debug = True)