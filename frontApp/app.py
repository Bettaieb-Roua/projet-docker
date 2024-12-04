from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def upload_files():
    return render_template("form.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)