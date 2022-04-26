from flask import Flask, render_template
from views import simple_views

app = Flask(__name__)
app.register_blueprint(simple_views.bp)

@app.route('/')
def index():
    return render_template('myworks.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80", debug="true")
