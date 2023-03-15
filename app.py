from flask import Flask, render_template, request
from drug_prediction_pipeline import predict
from cytoscape import predict_cy


app = Flask(__name__)

@app.route('/step1')
def step1(Drug_a = None, Drug_b = None):
    return render_template('p1.html', Drug_a = Drug_a, Drug_b = Drug_b)

@app.route('/step2', methods = ['POST'])
def step2():
    if request.method == 'POST':
        A = request.form['Drug_a']
        B = request.form['Drug_b']
        result = predict(A, B)
        return render_template("p2.html", error=result[0], drug_a=result[1], drug_b=result[2], type = result[3], Description = result[4], Confidence = result[5])

@app.route('/step3', methods = ['POST'])
def step3():
    if request.method == 'POST':
        A = request.form['Drug_a']
        B = request.form['Drug_b']
        result = predict_cy(A,B)
        return render_template("p3.html", drug_a = result[0], drug_b = result[1], intersection_uniprots = result[2], inter_result = result[3], hy_result = result[4])

@app.route('/')
def hello_pybo():
    return render_template('intro.html')




