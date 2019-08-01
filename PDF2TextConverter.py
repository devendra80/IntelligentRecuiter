from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convertPDFToText(fPath):
    pdfRM = PDFResourceManager()
    strIO = StringIO()
    codec = 'utf-8'
    laParams = LAParams()
    tConverter = TextConverter(pdfRM, strIO, codec=codec, laparams=laParams)
    fp = open(fPath, 'rb')
    interpreter = PDFPageInterpreter(pdfRM, tConverter)
    docPW = ""
    maxPageCnt = 0
    cacheFlag = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxPageCnt, password=docPW,caching=cacheFlag, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    tConverter.close()
    fContent = strIO.getvalue()
    strIO.close()
    return fContent