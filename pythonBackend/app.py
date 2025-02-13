import os
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# ===== INDEX route =======
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
