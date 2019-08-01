import nltk, subprocess, glob, sys

from PDF2TextConverter import convertPDFToText
from Docx2TextConverter import convertDocxToText

from collections import Counter

import json 

import textract 

class FileProcessor():
    def __init__(self, verbose=False):
        
        print('Starting Programme')
        file4RequiredSkills = "java-skills.txt"
        allowedFileExt = {"doc", "docx", "pdf", "rtf"}
        #resumeFolder = "../ncr-resumes/";
        #resumeFolder = "../resumes/test-resume/";
        resumeFolder = "../resumes/v2/"
        self.skills = self.readRequiredSkills(file4RequiredSkills) 
        t2 = self.skills
        print("....", t2)
        self.summary = {'data' : {}, 'category' : {}}
        #self.summary['data'] = {}
        #self.summary['category'] = {}
        
        files = []
        f = glob.glob(resumeFolder + "*.doc")
        for e in allowedFileExt:
            f = f + glob.glob(resumeFolder + "*." + e)
            
        files = list(set(f))
        #print(files)
        print ("%d files identified" %len(files))
        
        for f in files:
            print("Reading File %s"%f)
            info = {}

            self.inputString, info['extension'] = self.readFile(f)  
            #print('full text in result ', '\n', self.inputString)
            info['fileName'] = f
            
            #self.tokenize(self.inputString)
            self.cleanClutter(self.inputString)
            #self.candidateSkills = self.tokenize(self.inputString)
            self.candidateSkills = self.tokenize(self.inputString.upper())
            
            t1 = self.candidateSkills
            self.getStats(t1, t2, f)
            
        #print(self.summary)
        self.write2Afile()
       
    def write2Afile(self):
        file = open("output.txt","w")
        # convert dictionary into string 
        # using json.dumps() 
        result = json.dumps(self.summary) 
        file.write(result)
        file.close()
#Copy and paste
        
    def getStats(self, fContent, toSearch, fPath):
        print(toSearch, type(toSearch))
        cnt = dict(Counter(fContent))
        print(cnt)
        skillLen = len(toSearch)
        print('skillLen :', skillLen)
        
        p = {'missing' : 0}
        c = 0
        lst = []
        
        for x in set(toSearch):
            p[x] = cnt.get(x.upper())
            if isinstance(p[x], (int, float)):
                c = c + p[x]
                lst.append(x)
            else:
                p['missing'] = p['missing'] + 1
        
        print(fPath, "====", lst)
        p['total'] = c
        p['matchingSkills'] = skillLen - p['missing']
        #p['missing'] = c
        self.summary['data'][fPath] = p
        docs = self.summary['category'].get(p['matchingSkills'])
        k = 'no_match'
        if(len(lst) > 0 ):
            k = "".join(lst)
        print('docs :', docs)
        print('lst :', lst, k)
        if(docs == None):
            #docs = []
            #self.summary['category'][p['matchingSkills']] = docs
            docs = {k : {'skills' : lst, 'candidates': [], 'files': []}}
            self.summary['category'][p['matchingSkills']] = docs
        else:
            cds = docs.get(k)
            #print('cds :', cds)
            if(cds == None):
                cds = {}
                docs[k] = cds
                cds['skills'] = lst
                cds['candidates'] = []
                cds['files'] = []
            cds['candidates'].append(p)
            cds['files'].append(fPath)
        
        #docs.append(p)
        #print(p)
        
    def cleanClutter(self, fContent):
        return fContent;
    
    def preprocess(self, document):
        #print('preprocess started')
        try:
            try:
                document = document.decode('ascii', 'ignore')
            except:
                document = document.encode('ascii', 'ignore')
            
            lines = [el.strip() for el in document.splitlines() if len(el) > 0]  # Splitting on the basis of newlines 
            
            lines = [nltk.word_tokenize(str(el, 'utf-8')) for el in lines ]
            
            lines = [nltk.pos_tag(el) for el in lines]  # Tag them
            
            sentences = nltk.sent_tokenize(document.decode('utf-8'))    # Split/Tokenize into sentences (List of strings)
            
            sentences = [nltk.word_tokenize(sent) for sent in sentences]    # Split/Tokenize sentences into words (List of lists of strings)
            words = sentences
            
            dummy = []
            for el in words:
                dummy += el
            words = dummy
            
            return words
        except Exception as e:
            print(e)
            
    def tokenize(self, inputString):
        try:
            self.tokens = self.preprocess(inputString)
            return self.tokens
        except Exception as e:
            print(e)
            
    def readFile(self, fileName):
        
        extension = fileName.split(".")[-1]
        if extension == "txt":
            f = open(fileName, 'r')
            string = f.read()
            f.close() 
            return string, extension
        elif extension == "doc":
            #print('reading doc file')
            #return subprocess.Popen(['antiword', fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0], extension
            return textract.process(fileName, extension='doc'), extension
        elif extension == "docx":
            try:
                return convertDocxToText(fileName), extension
            except:
                return ''
                pass
        
        elif extension == "pdf":
            try:
                return convertPDFToText(fileName), extension
            except:
                return ''
                pass
        else:
            print('Unsupported format')
            return '', ''
        
        
    def readRequiredSkills(self, rFile):
        info = {}
        #print("rFile", rFile)
        inputSkills, info['extension'] = self.readFile(rFile)
        words = self.tokenize(inputSkills)
        #print("words", inputSkills)
        return words
    
if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = FileProcessor(verbose)