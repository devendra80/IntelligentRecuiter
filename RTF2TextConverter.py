from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter

def convertRtfToText(fPath):
	doc = Rtf15Reader.read(open(fPath))
	return PlaintextWriter.write(doc).getvalue()