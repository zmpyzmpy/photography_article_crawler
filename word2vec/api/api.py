from flask import Flask, render_template, request, Response,redirect, url_for
import gensim
from flask import jsonify
import json
app = Flask(__name__)


model = gensim.models.Word2Vec.load("./model/photography.model")
def getResult(pos, neg):
    try:
        return model.most_similar(positive=pos, negative=neg)
    except:
        return []

@app.route('/')
def home():
    
    tags = json.load(open('tags.txt'))
    
    pos = []
    neg = []
    res = []
    result = []
    query = request.args.get('query')
    if query:
        pos.append(query)
        res = getResult(pos, neg)
    
        if query in tags.keys():
            result.append([query,tags[query]])
    
    for r in res:
        tag = r[0]
        if tag in tags.keys():
            result.append([tag,tags[tag]])
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000, debug=True, threaded=True)
