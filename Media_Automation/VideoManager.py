import os
import sys
import requests
import subprocess
sys.path.append(os.path.abspath('..'))
from pywsdk import *
class RecordVideo:
    VIDEO_FORMAT_LIST = [
        GpCameraSettingOption.SETUP_VIDEO_FORMAT_NTSC,
        GpCameraSettingOption.SETUP_VIDEO_FORMAT_PAL
    ]
    VIDEO_PROTUNE_LIST = [
        GpCameraSettingOption.VIDEO_PROTUNE_ON,
        GpCameraSettingOption.VIDEO_PROTUNE_OFF,
    ]
    VIDEO_EIS_LIST = [
        GpCameraSettingOption.VIDEO_EIS_OFF,
        GpCameraSettingOption.VIDEO_EIS_ON
    ]
    VIDEO_SPOT_METER_LIST = [
        GpCameraSettingOption.VIDEO_SPOT_METER_ON,
        GpCameraSettingOption.VIDEO_SPOT_METER_OFF,
    ]
    VIDEO_PROTUNE_COLOR_LIST = [
        GpCameraSettingOption.VIDEO_PROTUNE_COLOR_FLAT,
        GpCameraSettingOption.VIDEO_PROTUNE_COLOR_GOPRO_COLOR,
    ]
    VIDEO_LOW_LIGHT_LIST = [
        GpCameraSettingOption.VIDEO_LOW_LIGHT_OFF,
        GpCameraSettingOption.VIDEO_LOW_LIGHT_ON,
    ]
    VIDEO_PROTUNE_EV_LIST = [
        GpCameraSettingOption.VIDEO_PROTUNE_EV_NEG2_0,
        GpCameraSettingOption.VIDEO_PROTUNE_EV_0_0,
        GpCameraSettingOption.VIDEO_PROTUNE_EV_2_0,
    ]
    VIDEO_PROTUNE_ISO_LIST = [
        GpCameraSettingOption.VIDEO_PROTUNE_ISO_400,
        GpCameraSettingOption.VIDEO_PROTUNE_ISO_6400,
    ]
    VIDEO_PROTUNE_WHITE_BALANCE_LIST = [
        GpCameraSettingOption.VIDEO_PROTUNE_WHITE_BALANCE_AUTO,
        GpCameraSettingOption.VIDEO_PROTUNE_WHITE_BALANCE_NATIVE,
    ]
    VIDEO_PROTUNE_SHARPNESS_LIST = [
        GpCameraSettingOption.VIDEO_PROTUNE_SHARPNESS_HIGH,
        GpCameraSettingOption.VIDEO_PROTUNE_SHARPNESS_LOW,
    ]

    #VIDEO_EXPOSURE_TIME_LIST
    #VIDEO_LOOPING_LIST
    #VIDEO_PIV_LIST
    #VIDEO_TIMELAPSE_RATE_LIST

    def __init__(self,camera, duration, Downloader, Verifier, filePath = None ):
        self.camera = camera
        self.duration = duration
        self.configPath = filePath
        self.TerryCrews = GpBouncer(self.camera.getSettingsJson())
        self.downloader = Downloader
        self.verifier = Verifier

    def captureVideo(self):

        self.recordVideo()
        self.downloader.downloadLastVideo(self.verifier)
        self.verifier.verify(self.camera)
        self.camera.deleteLastFileOnSdCard()

    def recordVideo(self):
        milliDuration = self.duration * 1000
        self.camera.setShutter(True)
        self.camera.sleep(milliDuration)
        self.camera.setShutter(False)


    def setBanner(self, serverIP,port):
        self.bannerIP = serverIP
        self.bannerPort = port

    def CheckIfDone(self,optionsString):
        print optionsString
        try:
            with open(self.configPath,"r")as file:
                completedData = json.load(file)
            for i in completedData:
                for key, value in i.iteritems():
                    if key == 'camera' and value == optionsString:
                        print key,value
                        return True
        except IOError:
            print "No JSON. Ok."
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        }
        optionsString = optionsString.replace("_", "\n")
        data = json.dumps({'banner':optionsString})
        r = requests.post("http://%s:%s/banner" % (self.bannerIP,self.bannerPort),headers=headers,data=data)
        return False

    def configureVideoSettings(self):
        for setting in self.videoSetList:
            self.camera.setSetting(setting[0],setting[1])

    def getVideoSettings(self):
        return self.settingsList

    def setVideoSettings(self, settingsAndOptions):
        self.videoSettingsList = settingsAndOptions
        self.verifier.setExpectedSettings(self.videoSettingsList)

    def protunePermutations(self,optionsString,pt,fov,fps,res,form):
        oldOptionsString = optionsString
        for sharp in self.VIDEO_PROTUNE_SHARPNESS_LIST:
            sharpString = GpCameraSetting.VIDEO_PROTUNE_SHARPNESS[0].replace("_", "").upper() + "-" + str(sharp[0]) + "_"
            if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_PROTUNE_SHARPNESS, sharp, self.camera.getStatusJson()):
                self.camera.setSetting(GpCameraSetting.VIDEO_PROTUNE_SHARPNESS, sharp)
                for color in self.VIDEO_PROTUNE_COLOR_LIST:
                    colorString = GpCameraSetting.VIDEO_PROTUNE_COLOR[0].replace("_", "").upper() + "-" + str(color[0]) + "_"
                    if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_PROTUNE_COLOR, color, self.camera.getStatusJson()):
                        self.camera.setSetting(GpCameraSetting.VIDEO_PROTUNE_COLOR, color)
                        for whiteBalance in self.VIDEO_PROTUNE_WHITE_BALANCE_LIST:
                            balanceString = GpCameraSetting.VIDEO_PROTUNE_WHITE_BALANCE[0].replace("_", "").upper() + "-" + str(whiteBalance[0]) + "_"
                            if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_PROTUNE_WHITE_BALANCE, whiteBalance,self.camera.getStatusJson()):
                                self.camera.setSetting(GpCameraSetting.VIDEO_PROTUNE_WHITE_BALANCE,  whiteBalance)
                                for iso in self.VIDEO_PROTUNE_ISO_LIST:
                                    isoString = GpCameraSetting.VIDEO_PROTUNE_ISO[0].replace("_", "").upper() + "-" + str(iso[0]) + "_"
                                    if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_PROTUNE_ISO, iso,self.camera.getStatusJson()):
                                        self.camera.setSetting(GpCameraSetting.VIDEO_PROTUNE_ISO, iso)
                                        for ev in self.VIDEO_PROTUNE_EV_LIST:
                                            evString = GpCameraSetting.VIDEO_PROTUNE_EV[0].replace("_","").upper() + "-" + str(ev[0]) + "_"
                                            if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_PROTUNE_EV,ev, self.camera.getStatusJson()):
                                                self.camera.setSetting(GpCameraSetting.VIDEO_PROTUNE_EV,ev)
                                                #TODO: FIX THIS MESSSSSSSSSSSSSSS
                                                #_,.-~-.,_,.-~-.,_
                                                ####Camera-Specific-Options
                                                #_,.-~-.,_,.-~-.,_
                                                # if self.camera.getCameraModelName() == "HERO5 Black": #possibly MR as well
                                                #     for eis in self.VIDEO_EIS_LIST:
                                                #         eisString = GpCameraSetting.VIDEO_EIS[0].replace("_","").upper() + "-" + str(eis[0]) + "_"
                                                #         if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_EIS, eis,self.camera.getStatusJson()):
                                                #             self.camera.setSetting(GpCameraSetting.VIDEO_EIS,eis)
                                                #             eisString = GpCameraSetting.VIDEO_EIS[0].replace("_","").upper() + "-OFF_"
                                                #         else:
                                                #             print "EIS cant be done with current settings."
                                                #         for ll in self.VIDEO_LOW_LIGHT_LIST:
                                                #             llString = GpCameraSetting.VIDEO_LOW_LIGHT[0].replace("_","").upper() + "-" + str(ll[0]) + "_"
                                                #             if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_LOW_LIGHT, ll,self.camera.getStatusJson()):
                                                #                 self.camera.setSetting(GpCameraSetting.VIDEO_LOW_LIGHT,ll)
                                                #             else:
                                                #                 print "Low light cant be done with current settings"
                                                #                 llString = GpCameraSetting.VIDEO_LOW_LIGHT[0].replace("_","").upper() + "-OFF_"
                                                #             protuneOptionsString = oldOptionsString + sharpString + colorString + balanceString + isoString + evString + llString + eisString
                                                #             if not self.CheckIfDone(protuneOptionsString):
                                                #                 self.verifier.setCameraString(protuneOptionsString)
                                                #                 self.setVideoSettings(
                                                #                 self.setupForOptions(eis, ll, ev, iso, whiteBalance, color,sharp, pt, fov, fps, res, form))
                                                #                 self.captureVideo()
                                                #             else:
                                                #                 print "this permutation has been done already."
                                                #
                                                # else:
                                                #     for ll in self.VIDEO_LOW_LIGHT_LIST:
                                                #         llString = GpCameraSetting.VIDEO_LOW_LIGHT[0].replace("_","").upper() + "-" + str(ll[0]) + "_"
                                                #         if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_LOW_LIGHT,ll, self.camera.getStatusJson()):
                                                #              self.camera.setSetting(GpCameraSetting.VIDEO_LOW_LIGHT, ll)
                                                #              for spot in self.VIDEO_SPOT_METER_LIST:
                                                #                 spotString = GpCameraSetting.VIDEO_SPOT_METER[0].replace("_","").upper() + "-" + str(spot[0]) + "_"
                                                #                 if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_SPOT_METER, spot,self.camera.getStatusJson()):
                                                #                     self.camera.setSetting(GpCameraSetting.VIDEO_SPOT_METER,spot)
                                                #                     protuneOptionsString = oldOptionsString + sharpString + colorString + balanceString + isoString + evString + llString + spotString
                                                #                     if not self.CheckIfDone(protuneOptionsString):
                                                #                         self.verifier.setCameraString(protuneOptionsString)
                                                #                         self.setVideoSettings(self.setupForOptions(spot,ll,ev,iso,whiteBalance,color,sharp,pt, fov, fps, res, form))
                                                #                         self.captureVideo()
                                                #                     else:
                                                #                         print "this permutation has been done already."
                                                protuneOptionsString = oldOptionsString + sharpString + colorString + balanceString + isoString + evString
                                                if not self.CheckIfDone(protuneOptionsString):
                                                    self.verifier.setCameraString(protuneOptionsString)
                                                    self.setVideoSettings(self.setupForOptions(ev,iso,whiteBalance,color,sharp,pt,fov,fps,res,form))
                                                    self.captureVideo()
                                                else:
                                                    print "SKIP: This permutation has been done already"


                                                #         if self.TerryCrews.doesCameraSupportSetting(GpCameraSetting.VIDEO_EIS):#EIS CHECK
                                                #
                                                #                     protuneOptionsString = oldOptionsString + sharpString + colorString + balanceString + isoString + evString + llString + eisString
                                                #                     if not self.CheckIfDone(protuneOptionsString):
                                                #                         self.verifier.setCameraString(protuneOptionsString)
                                                #                         self.setVideoSettings(self.setupForOptions(eis,ll,ev,iso,whiteBalance,color,sharp,pt, fov, fps, res, form))
                                                #                         self.captureVideo()
                                                #
                                                #                     else:
                                                #                         print "this permutation has been done already."
                                                #                 else:
                                                #                     protuneOptionsString = oldOptionsString + sharpString + colorString + balanceString + isoString + evString + llString
                                                #                     if not self.CheckIfDone(protuneOptionsString):
                                                #                         self.verifier.setCameraString(protuneOptionsString)
                                                #                         self.setVideoSettings(self.setupForOptions(ll,ev,iso,whiteBalance,color,sharp,pt, fov, fps, res, form))
                                                #                         self.captureVideo()
                                                #         else:#must be spot meter
                                                #             for spot in self.VIDEO_SPOT_METER_LIST:
                                                #                 spotString = GpCameraSetting.VIDEO_SPOT_METER[0].replace("_","").upper() + "-" + str(spot[0]) + "_"
                                                #                 if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_SPOT_METER, spot,self.camera.getStatusJson()):
                                                #                     self.camera.setSetting(GpCameraSetting.VIDEO_SPOT_METER,spot)
                                                #                     protuneOptionsString = oldOptionsString + sharpString + colorString + balanceString + isoString + evString + llString + spotString
                                                #                     if not self.CheckIfDone(protuneOptionsString):
                                                #                         self.verifier.setCameraString(protuneOptionsString)
                                                #                         self.setVideoSettings(self.setupForOptions(spot,ll,ev,iso,whiteBalance,color,sharp,pt, fov, fps, res, form))
                                                #                         self.captureVideo()
                                                #                     else:
                                                #                         print "this permutation has been done already."

    def setupForOptions(self, *args):
        settingsAndOptionsList = []
        for options in args:
            if options[2] > 10: #tribal magic of group IDs in GPcamerasettings and options. Protune is 10. Protune options are <10.
                #hardcoded findings
                if options[2] == 11:
                    optionTuple = (GpCameraSetting.VIDEO_PROTUNE_WHITE_BALANCE,options)
                elif options[2] == 12:
                    optionTuple = (GpCameraSetting.VIDEO_PROTUNE_COLOR, options)
                elif options[2] == 13:
                    optionTuple = (GpCameraSetting.VIDEO_PROTUNE_ISO, options)
                elif options[2] == 14:
                    optionTuple = (GpCameraSetting.VIDEO_PROTUNE_SHARPNESS, options)
                else:
                    optionTuple = (GpCameraSetting.VIDEO_PROTUNE_EV, options)
            else:
                optionTuple = (GpCameraFannyPack.getSettingFromOption(options),options)
            print optionTuple
            settingsAndOptionsList.append(optionTuple)
        return settingsAndOptionsList

    def permutateOptions(self):
        self.camera.setSubmode(GpCameraModesAndSubmodes.GpCameraSubmodes.VIDEO)
        self.camera.setSetting(GpCameraSetting.VIDEO_PROTUNE, GpCameraSettingOption.VIDEO_PROTUNE_OFF)
        for form in self.VIDEO_FORMAT_LIST:
            formString = GpCameraSetting.SETUP_VIDEO_FORMAT[0].replace("_", "").upper() + "-" + str(form[0]) + "_"
            if self.TerryCrews.isOptionValid(GpCameraSetting.SETUP_VIDEO_FORMAT,form,self.camera.getStatusJson()):
                self.camera.setSetting(GpCameraSetting.SETUP_VIDEO_FORMAT,form)
                for res in self.camera.getOptionsForSetting(GpCameraSetting.VIDEO_RESOLUTION):
                    resString = GpCameraSetting.VIDEO_RESOLUTION[0].replace("_","").upper() + "-" + str(res[0]) + "_"
                    if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_RESOLUTION,res, self.camera.getStatusJson()):
                        self.camera.setSetting(GpCameraSetting.VIDEO_RESOLUTION,res)
                        for fps in self.camera.getOptionsForSetting(GpCameraSetting.VIDEO_FPS):
                            fpsString = GpCameraSetting.VIDEO_FPS[0].replace("_","").upper() + "-" + str(fps[0]) + "_"
                            if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_FPS,fps,self.camera.getStatusJson()):
                                self.camera.setSetting(GpCameraSetting.VIDEO_FPS,fps)
                                for fov in self.camera.getOptionsForSetting(GpCameraSetting.VIDEO_FOV):
                                    fovString = GpCameraSetting.VIDEO_FOV[0].replace("_","").upper() + "-" + str(fov[0]) + "_"
                                    if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_FOV, fov,self.camera.getStatusJson()):
                                        self.camera.setSetting(GpCameraSetting.VIDEO_FOV, fov)
                                        for pt in self.VIDEO_PROTUNE_LIST:
                                            ptString = GpCameraSetting.VIDEO_PROTUNE[0].replace("_","").upper() + "-" + str(pt[0]) + "_"
                                            if self.TerryCrews.isOptionValid(GpCameraSetting.VIDEO_PROTUNE, pt,self.camera.getStatusJson()):
                                                self.camera.setSetting(GpCameraSetting.VIDEO_PROTUNE, pt)
                                                optionsString = formString + resString + fpsString + fovString + ptString
                                                #######################################################Protune starts here
                                                if pt == GpCameraSettingOption.VIDEO_PROTUNE_ON:
                                                    self.protunePermutations(optionsString,pt,fov,fps,res,form)
                                                    #print "stuff"
                                                else:
                                                    if not self.CheckIfDone(optionsString):
                                                        self.verifier.setCameraString(optionsString)
                                                        self.setVideoSettings(self.setupForOptions(pt,fov,fps,res,form))
                                                        self.captureVideo()
                                                    else:
                                                        print "this permutation has been done already."
                                                ##check if we have done it before
                                                ##record and download
                                                #######################################################








    #
    # def recursiveVideoSetter(self, settingList, origListLength, CurrentOptions=[]):
    #     #        TODO: Protune Settings and Camera-Specfic
    #     """
    #     A recursive method to go though options of settings for a camera. The settingList needs to be predefined
    #
    #     :param settingList: the list of tuples with lists that is being recursed though
    #     :param origListLength: the original list length to determine permutation
    #     :param CurrentOptions: the current "depth" of settings with set options
    #     :return: void. After a permutation is found, another function should be used to set the options and do stuff
    #     """
    #
    #     # copied to preserve data
    #     optionCopiedList = copy.copy(settingList[0][1])
    #     while len(optionCopiedList) is not 0:
    #         # check if first option in option list is valid
    #         if self.TerryCrews.isOptionValid(settingList[0][0], optionCopiedList[0], self.camera.getStatusJson()):
    #             CurrentOptions.append([settingList[0][0], optionCopiedList[0]])
    #             # if we hit our limit for setting/options
    #             if len(CurrentOptions) == origListLength:
    #                 return CurrentOptions
    #             else:
    #                 # else, we need to go one setting deeper
    #                 self.recursiveThing(settingList[1:], origListLength, CurrentOptions)
    #             CurrentOptions.pop()
    #         # we have completed this option in our setting(valid or not). pop from option list
    #         if len(optionCopiedList) is not 0:
    #             optionCopiedList.pop(0)
    #


if __name__ == "__main__":
    camera = GpCamera.connectOnCurrentWiFiNetwork()
    re = RecordVideo(camera)
    re.permutateOptions()