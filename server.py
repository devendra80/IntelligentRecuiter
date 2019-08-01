from flask import Flask, render_template, request, url_for
import time
import json
#from AsyncTask import AsyncGitTask

data = {
  "data": [
    {
      "id": "1",
      "name": "Tiger Nixon",
      "position": "System Architect",
      "salary": "$320,800",
      "start_date": "2011/04/25",
      "office": "Edinburgh",
      "extn": "5421"
    },
    {
      "id": "2",
      "name": "Garrett Winters",
      "position": "Accountant",
      "salary": "$170,750",
      "start_date": "2011/07/25",
      "office": "Tokyo",
      "extn": "8422"
    }]
}
 

app = Flask(__name__)

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
    f = open('output.txt', 'r')
    string = f.read()
    f.close() 
    #params = {   'api_key': '{API_KEY}'  }
    #return json.dumps(data)
    j = json.loads(string)
    print('json.dumps(string) :', j["category"])
    return j["category"]

@app.route("/details/")
def get_resume_details():
    param = request.args.get('param')
    print('param :', param)
    var = param.split("-")
    print(var[0], var[1])
    f = open('output.txt', 'r')
    string = f.read()
    f.close() 
    
    f1 = open('java-skills.txt', 'r')
    sk1 = f1.read()
    f1.close() 
    
    #params = {   'api_key': '{API_KEY}'  }
    #return json.dumps(data)
    j = json.loads(string)
    '''j1 = json.loads(sk1)
    print('json.loads(string) :', j["category"][var[0]][var[1]]["files"])
    '''
    #return j["category"][var[0]][var[1]]["files"]
    '''info = {}
    for f in j["category"][var[0]][var[1]]["files"]:
        info[f] = []
        for a in j1:
            info[f].append(10)
            '''
    #return render_template('details.html',data=j["category"][var[0]][var[1]]["files"])
    print('info :', j["category"][var[0]][var[1]]["files"])
    print('info :', j["category"][var[0]][var[1]]["candidates"])
    info = {}
    info['files'] = j["category"][var[0]][var[1]]["files"]
    maxJava = 1
    maxTomact = 1
    for k in j["category"][var[0]][var[1]]["candidates"]:
        print(k['Java'], k['Tomcat'])
        if isinstance(k['Java'], (int, float)) and k['Java'] > maxJava:
            maxJava = k['Java']
            print("k['Java']", k['Java'])
        if isinstance(k['Tomcat'], (int, float)) and  k['Tomcat'] > maxTomact:
            maxTomact = k['Tomcat']
            print("k['Tomcat']", k['Tomcat'])
    print('max value :', maxJava, maxTomact)
    skInfo = []
    for k in j["category"][var[0]][var[1]]["candidates"]:
        j = 0
        t = 0
        if isinstance(k['Java'], (int, float)):
            j = k['Java'] * 100 / maxJava; 
        if isinstance(k['Tomcat'], (int, float)):
            t = k['Tomcat'] * 100 / maxTomact; 
        skInfo.append({'Java' :  j, 'Tomcat' :  t})
    print(skInfo)
    info['fit'] = skInfo
    #return render_template('details.html',data=j["category"][var[0]][var[1]]["files"])
    return render_template('details.html',data=info)


#https://help.parsehub.com/hc/en-us/articles/217751808-API-Tutorial-How-to-get-run-data-using-Python-Flask
 

#app.run(host='0.0.0.0', port=12345)

if __name__ == "__main__":
    app.run()