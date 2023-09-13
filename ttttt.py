#!/usr/bin/env python2

import re
import sys
import os
import tempfile
import requests
import xml.dom.minidom
from ftntlib import FortiOSREST
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sys.path.append('/opt/phoenix/data-definition/remediations')
from remediation import HttpRemediation, Logger


class FortiGateBlockIpWithApiRemediation(HttpRemediation):
    def run_remediation(self, args):
        doc = xml.dom.minidom.parse(self.mIncidentXML)

        # to block
        nodes = doc.getElementsByTagName('incidentSource')
        if nodes.length < 1:
            self.log.error("no incident Source found!")
        else:
            targetNode = nodes[0]

        srcIp = ''
        for node in targetNode.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.getAttribute("attribute") == "srcIpAddr":
                    srcIp = node.firstChild.data
        if srcIp == '':
            self.log.error("no incident source found!")
            exit(1)

        # trim IP, e.g. 10.1.20.189(SH-Quidway-SW1)
        srcIp = re.findall( r'[0-9]+(?:\.[0-9]+){3}', srcIp )[0]

        #To add ip to block in fortiOS using ftntlib package

        fgt = FortiOSREST()
        # fgt.debug('on')
        fgt.login(self.mAccessIp, self.mPort, self.mUser, self.mPassword)
        response = fgt.post('monitor', 'user', 'banned','add_users', parameters={'vdom': 'root'}, data={'ip_addresses':['' + srcIp + ''],'expiry':86400})
        # self.log.info("returned by FortiClient EMS:\n%s" % response)
        fgt.logout()

        # ToDo: maybe some verification tasks
        exit(0)

if __name__ == "__main__":
    remediation = FortiGateBlockIpWithApiRemediation()
    remediation.execute(sys.argv)