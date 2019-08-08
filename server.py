from flask import Flask, render_template, request, url_for
import time
import json
#from AsyncTask import AsyncGitTask


app = Flask(__name__)
output_resource = 'output.txt'
#skill_resource = 'java-skills.txt'
skill_resource = 'myncr-testing-skills.txt'

@app.route("/")
def home():
    #return render_template("reports.html")
    return render_template("resumes.html")

def run_algorithms():
        return {'file_name': 'filename', 'set_min': 'hello world 1','rep_sec':'hello world 2'}

@app.route("/direct")
def home2():
    return render_template('rect.html',string=run_algorithms())

@app.route("/resume")
def get_resumes():
    f = open(output_resource, 'r')
    string = f.read()
    f.close() 
    #params = {   'api_key': '{API_KEY}'  }
    #return json.dumps(data)
    j = json.loads(string)
    print('json.dumps(string) :', j["category"])
    return j["category"]

def getBestFit(skillMaxScore, candidates):
    skInfo = []
    for k in candidates:
        candidateFit = {}
        for s in skillMaxScore:
            if isinstance(k[s], (int, float)):
                j = k[s] * 100 / skillMaxScore[s]; 
                candidateFit[s] = j
            else:
                candidateFit[s] = 0
        
        skInfo.append(candidateFit)
    print(skInfo)
    return skInfo
    
def getScores(skillFile, candidates):
    f1 = open(skillFile, 'r')
    sk1 = f1.read()
    print(sk1)
    sk1.split("\n")
    skillList = sk1.split("\n")
    f1.close()
    skillMaxScore={}
    for s in skillList:
        skillMaxScore[s] = 1
    
    for k in candidates:
        #print(k['Java'], k['Tomcat'])
        for skill in skillMaxScore:
            if isinstance(k[skill], (int, float)) and k[skill] > skillMaxScore[skill]:
                skillMaxScore[skill] = k[skill]
                #print(skill, k[skill])
        
    print('max value :', skillMaxScore)
    return skillList, skillMaxScore
        
@app.route("/details/")
def get_resume_details():
    param = request.args.get('param')
    print('param :', param)
    var = param.split("-")
    print(var[0], var[1])
    f = open(output_resource, 'r')
    string = f.read()
    f.close() 
    

    j = json.loads(string)
    
    #print('info :', j["category"][var[0]][var[1]]["files"])
    #print('info :', j["category"][var[0]][var[1]]["candidates"])
    info = {}
    info['files'] = j["category"][var[0]][var[1]]["files"]

    skillList, skillMaxScore=getScores(skill_resource, j["category"][var[0]][var[1]]["candidates"])
   
    info['fit'] = getBestFit(skillMaxScore, j["category"][var[0]][var[1]]["candidates"])
    info['skills'] = skillList

    return render_template('details.html',data=info)


#https://help.parsehub.com/hc/en-us/articles/217751808-API-Tutorial-How-to-get-run-data-using-Python-Flask
 

#app.run(host='0.0.0.0', port=12345)

if __name__ == "__main__":
    app.run()
