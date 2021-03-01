from flask import Flask, request
from svc.tasks.tasks import task1
app = Flask(__name__)


@app.route('/task')
def task():
    task1.apply_async((), queue='sqs-us-east-1-amazonaws-com_160043208412_try2')
    return 'added new task to the Q'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
