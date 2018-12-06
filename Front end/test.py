from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/_get_data/', methods=['POST'])
def _get_data():
    my_list = ["one", "two", "three"]
    return jsonify({'_data_: render_template('response.html', my_list=my_list)})


if __name__ == "__main__":
    app.run(debug=True)
