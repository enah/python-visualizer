from flask import Flask, request, render_template, flash, url_for, redirect

from pylint import epylint
from controlflow import exec_script_str

import re
import json
import tempfile
import argparse

app = Flask(__name__)

EXAMPLE = """
# Try this simple example
def memo(f):
    cache = dict()
    def wrapped(*args):
        t = tuple(args)
        if t not in cache:
            cache[t] = f(*args)
        return cache[t]
    return wrapped
@memo
def fibo(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibo(n-1) + fibo(n-2)
print fibo(10)
"""

@app.route("/", methods=['GET', 'POST'])
def home():
    example = json.dumps(EXAMPLE)

    upload_template = "python_flow_visualizer_upload.html"

    try:
        code = request.files['code_file']
        if code.size > 1024*1024:
            return render(upload_template,
                          errors=["file size limit exceeded :("],
                          example=example)
        code = code.read()
    except:
        code = None

    if code is None:
        code = request.form.get('code', None)

    if not code:
        return render_template(upload_template,
                               errors=["no code found."],
                               example=example)

    data = dict()

    result = exec_script_str(code)
    if len(result)<=1:
        result = "your code doesn't seem too short to be interesting!"
    if type(result) == str:
        return render_template(upload_template,
                               errors=[result],
                               code=json.dumps(code))
    data['branches'], data['stats'] = result

    data['code'] = [None,] + code.split('\n')

    with tempfile.NamedTemporaryFile() as f:
        f.write(code)
        f.seek(0)
        out, err = epylint.py_run(f.name, True)

    report = out.read()
    raw_reports = report.split('\n')[1:]
    reports = dict()

    for report in raw_reports:
        regex = re.compile(r'^[^:]+:(\d+): \[([-\w]+),([^\]]*)] (.*)$',re.i)
        r = regex.match(report)
        if r is None:
            continue
        line, warning, function, message = r.groups()
        if warning in ("fixme",):
            continue
        line = int(line)
        reports[line] = {
            "type":warning,
            "function":function,
            "message":message
        }

    data['warnings'] = reports

    json_data = json.dumps(data)

    return render_template("python_flow_visualizer.html",
                           data=json_data)

def main():
    parser = argparse.ArgumentParser(description='Runs the viewer')
    parser.add_argument('-p', '--production', action="store_true")
    args = parser.parse_args()
    PROD = args.production
    if PROD:
        app.run(host="0.0.0.0", port=80)
    else:
        app.run(debug=True)

if __name__ == '__main__':
    main()
