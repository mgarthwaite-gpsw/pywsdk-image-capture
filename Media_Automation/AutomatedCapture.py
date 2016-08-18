import os
import sys

import argparse
import DownloadMedia as dl
import Verifier as vf
import RecordMedia as rdm

sys.path.append(os.path.abspath('..'))
from pywsdk import *

class AutomatedCapture:
    def __init__(self, duration, destinationPath):
        self.destinationPath = destinationPath
        self.camera = GpCamera.connectOnCurrentWiFiNetwork()
        self.duration = duration
        self.Downloader = dl.Downloader(self.camera)
        self.Verifier = vf.VideoVerify(destinationPath)



#    def runVideo(self):

#    def runPhoto(self):

#    def runMulti(self):

    def runConfig(self):
        subDir = self.camera.getCameraModelName().replace(" ", "") + "-" + self.camera.getFirmwareVersion()
        jsonFile = self.camera.getCameraModelName().replace(" ", "") + "-" + self.camera.getFirmwareVersion() + ".json"

        if not os.path.exists(self.destinationPath + subDir):
            os.mkdir(self.destinationPath + subDir)

        filePath =self.destinationPath + subDir + "/" + jsonFile
        if not os.path.exists(filePath):
            print filePath
            print "No JSON file detected, starting from zero."
        else:
            print "stuff is found"



    def runAutomation(self):
        self.runConfig()
        ##config
        ##record
        ##download
        ##verify





def parseCommandLine():

    duration = 10
    parser = argparse.ArgumentParser(add_help=False)

    requiredGroup = parser.add_argument_group('Required Arguments')
    optionalGroup = parser.add_argument_group('Optional Arguments')

    optionalGroup.add_argument('-v', '--verbose',
                               type=str)

    optionalGroup.add_argument('-f', '--fps',
                               type=int)

    optionalGroup.add_argument('-d','--duration',
                               type=int)

    optionalGroup.add_argument('-t', '--pt',
                               type=str)


    args = parser.parse_args()



    destinationPath = "media/"
    Capture = AutomatedCapture(duration,destinationPath)
    return Capture





if __name__ == "__main__":
    CaptureClass = parseCommandLine()
    CaptureClass.runAutomation()