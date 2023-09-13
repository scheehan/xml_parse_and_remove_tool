import re
import xml.dom.minidom
import tempfile
import os,sys
from abc import abstractmethod
import logging
import socket


class Remediation:
    def __init__(self):
        self.tmpFileList = []
        self.log = Logger(os.path.basename(sys.argv[0])[:-3])
        pass

    def __del__(self):
        for tmpFile in self.tmpFileList:
            if os.path.isfile(tmpFile):
                os.remove(tmpFile)
        pass

    def check_usage(self, args):
        if len(args) != 2 and len(args) != len(self.get_arg_list()) + 2:
            print 'Usage: %s incident.xml %s' % (args[0], self.get_arg_list())
            exit(1)

    @abstractmethod
    def get_arg_list(self):
        print 'Cannot run Base.get_arg_list'
        raise NotImplementedError

    @abstractmethod
    def parse_args(self, args):
        print 'Cannot run Base.parse_args'
        raise NotImplementedError


    @abstractmethod
    def run_remediation(self, args):
        print 'Cannot run Base.run_remediation'
        raise NotImplementedError

    def execute(self, args):
        self.check_usage(args)
        if 2 == len(args):
            self.detect_enforce_on(args[1])
        else:
            self.parse_args(args)
            self.run_remediation(args)

    @staticmethod
    def get_incident_attribute(incident_xml, incident_tag, attr_name):
        doc = xml.dom.minidom.parse(incident_xml)

        nodes = doc.getElementsByTagName(incident_tag)
        if nodes.length < 1:
            print "Cannot find xml element %s" % incident_tag
            return None
        else:
            target = nodes[0]
        for node in target.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.getAttribute("attribute") == attr_name:
                    if node.firstChild:
                        return node.firstChild.data.strip().replace('\r', '').replace('\n', '')
                    else:
                        return None

    def detect_enforce_on(self, incident_xml):
        enforce_on = self.get_incident_attribute(incident_xml, "incidentTarget", "hostIpAddr")

        if not enforce_on or enforce_on == '':
            enforce_on = self.get_incident_attribute(incident_xml, "incidentTarget", "destIpAddr")

        if not enforce_on or enforce_on == '':
            print "Cannot detect enforceOn"
            exit(1)

        # trim IP, e.g. 10.1.20.189(SH-Quidway-SW1)
        enforce_on = re.sub(r'\(.+\)', '', enforce_on)
        enforce_on = enforce_on.strip()

        # only print enforce_on
        print 'ENFORCE_ON:[%s]' % enforce_on
        exit(0)

    def create_temp_file(self):
        tmpFileObj = tempfile.NamedTemporaryFile(dir="/opt/phoenix/cache/tmp", delete=False, prefix="remediation_")
        self.tmpFileList.append(tmpFileObj.name)
        return tmpFileObj.name


class WindowsRemediation(Remediation):
    def get_arg_list(self):
        return ["user", "password", "accessIp"]

    def parse_args(self, args):
        self.mIncidentXML = args[1]
        self.mUser = args[2]
        self.mPassword = args[3]
        self.mAccessIp = args[4]

    @abstractmethod
    def run_remediation(self, args):
        print 'Cannot run WindowsRemediation.run_remediation'
        raise NotImplementedError


class SshRemediation(Remediation):
    def get_arg_list(self):
        return ["user", "password", "superPassword", "accessIp"]

    def parse_args(self, args):
        self.mIncidentXML = args[1]
        self.mUser = args[2]
        self.mPassword = args[3]
        self.mSuperPassword = args[4]
        self.mAccessIp = args[5]

    @abstractmethod
    def run_remediation(self, args):
        print 'Cannot run SshRemediation.run_remediation'
        raise NotImplementedError


class HttpRemediation(Remediation):
    def get_arg_list(self):
        return ["user", "password", "accessIp", "hostName", "port"]

    def parse_args(self, args):
        self.mIncidentXML = args[1]
        self.mUser = args[2]
        self.mPassword = args[3]
        self.mAccessIp = args[4]
        self.mHostName = args[5]
        self.mPort = args[6]

    @abstractmethod
    def run_remediation(self, args):
        print 'Cannot run HttpRemediation.run_remediation'
        raise NotImplementedError


def Logger(name, level=logging.INFO, formatter=None, stdoutStream=False):
    """ Usage:
        log = Logger(name)
        log = Logger(name, logging.DEBUG)
    """
    log = logging.getLogger(name)
    log.setLevel(level)
    hdlr = logging.FileHandler('/tmp/%s.log' % name)
    formatter = logging.Formatter(formatter or '%(asctime)s[%(levelname)s]%(filename)s:%(lineno)d(%(funcName)s) %(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    if stdoutStream == True:
        streamHdlr = logging.StreamHandler()
        streamHdlr.setLevel(logging.ERROR)
        streamFormatter = logging.Formatter('%(levelname)s: %(message)s')
        streamHdlr.setFormatter(streamFormatter)
        log.addHandler(streamHdlr)
    return log


def is_valid_ipv6_address(address):
  try:
    socket.inet_pton(socket.AF_INET6, address)
  except socket.error:  # not a valid address
    return False
  return True

# Check whether the ip is internal ip
def ip_into_int(ip):
    return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c
