import json
import os
import re
import subprocess
from collections import OrderedDict


def getJson(path):
    with open(path) as f:
        j = json.loads(f.read())

    return j

os.chdir(os.path.dirname(__file__))
remote_path = os.getcwd()
config = getJson(remote_path + '/../updater.config')


class VersionData:

    def __init__(self, d=None, string=None):
        self.string = None
        self.dict = OrderedDict.fromkeys(['MAJOR', 'MINOR', 'PATCH', 'BUILD'])

        if d is not None:
            self._loadDict(d)
            self.string = makeStr(self.dict)

        elif(string is not None):
            self.string = string
            self._loadDict(self._makeDict(self.string))

        else:
            raise Exception

    def _makeStr(self, d):
        return "{}.{}.{}.{}".format(
            d['MAJOR'],
            d['MINOR'],
            d['PATCH'],
            d['BUILD'])

    def _makeDict(self, str):
        s = str.split(".")

        _d = {"MAJOR": int(s[0]), "MINOR": int(
            s[1]), "PATCH": int(s[2]), "BUILD": int(s[3])}
        return _d

    def _loadDict(self, oldDict):
        for key in self.dict:
            self.dict[key] = oldDict[key]


def validateVersionFile(file):
    pass


def makeStr(d):
    return "{}.{}.{}.{}".format(
        d['MAJOR'],
        d['MINOR'],
        d['PATCH'],
        d['BUILD'])

def updateVersionFile(path, remoteData, newVersion):
    remoteData["VERSION"] = newVersion

    #print(json.dumps(remoteData, sort_keys=False, indent=4, separators=(',', ': ')))
    try:
        with open(path, 'w') as f:
            json.dump(remoteData, f, sort_keys=False, indent=4,
                      separators=(',', ': '), ensure_ascii=False)
    except Exception as e:
        raise e


def parseMechJeb(r):
    d = re.search("AssemblyFileVersion\((.*)\)]", r.text).group(1)
    return d.strip("\"")

def tagCurrent(repPath):
    subprocess.check_output(["git", "-C", repPath, "tag", "-f", "current"])

def removeTag(repPath):
    subprocess.check_output(["git", "-C", repPath, "tag", "-d", "current"])

def commitVersion(repPath, version, rBranch="master"):
    subprocess.check_call(["git", "-C", repPath, "checkout", rBranch], stdout=subprocess.DEVNULL)
    commitStr = "Updated to version {}!".format(version)
    subprocess.check_call(["git", "-C", repPath, "commit", "-a", "-m", commitStr])

def pushUpdate(repPath, newVersion, rBranch="master"):
    subprocess.check_output(["git", "-C", repPath, "push", "origin", rBranch])


def syncUpstream(repPath, rBranch="master", uBranch="MuMech"):
    subprocess.check_output(["git", "-C", repPath, "fetch", "upstream"])
    subprocess.check_call(["git", "-C", repPath, "checkout", rBranch], stdout=subprocess.DEVNULL)
    subprocess.check_output(
        ["git", "-C", repPath, "rebase", "upstream/" + rBranch])

def rollbackCommit(repPath):
    print("Rolling back commit...")
    subprocess.check_output(["git", "-C", repPath, "reset", "--hard", "current"])


def compareVersions(v1, v2):
    if(v1.dict == v2.dict):
        return True
    else:
        return False


def testObj(t):
    print("Testing {}".format(t))
    print(t.string)
    print(t.dict)
