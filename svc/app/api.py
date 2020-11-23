from flask import Flask, request
from svc.tasks.tasks import task1
app = Flask(__name__)


@app.route('/task')
def task():
    task1.apply_async((), queue='<queue name>')
    return 'added new task to the Q'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
