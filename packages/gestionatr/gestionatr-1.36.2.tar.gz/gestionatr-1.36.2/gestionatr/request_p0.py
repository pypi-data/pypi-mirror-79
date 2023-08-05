from __future__ import absolute_import
"""
atr p0 --url https://viesgop0.app.viesgo.com/syncRequest.wsdl?WSDL -s 0762 -p SOMENE.62 -f p0_test.xml
"""
url = "https://viesgop0.app.viesgo.com/syncRequest.wsdl"
user = "0706"
pssw = "ENE190#06"
fil = """
LOL
"""

from gestionatr.cli import request_p0
res = request_p0(url, user, pssw, fil)
print res
