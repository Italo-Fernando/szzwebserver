from flask import Flask
import uuid

app = Flask(__name__)

@app.get('/szz/variants')
def szz_variants():
    return [{'variant_name' : 'B_SZZ'}]

@app.get('/szz/find_bug_commits/<result_id>')
def check_result(result_id):
    return {'szz_variant': 'B_SZZ', 'status' : 'WAITING', 'result' : []}

@app.post('/szz/find_bug_commits/')
def find_bug_commits():
    return {'result_id' : uuid.uuid4()}

@app.post('/repo')
def download_repo():
    return {'repository_id' : uuid.uuid4()}

@app.delete('/repo/<repository_id>')
def delete_repo(repository_id):
    return f'deleted repository with id: {repository_id}'

@app.get('/repo/<repository_id>/status')
def repository_status(repository_id):
    return {'status' : 'WAITING'}

if __name__ == '__main__':
    app.run()