import os
import sys
import pprint
sys.path.append(os.path.abspath('..'))
from pywsdk import *


class VideoVerify():

    camera = None
    validate = None

    ##options set for the recording
    file = None
    res = None
    fps = None
    fov = None
    pt = None
    ev = None
    eis = None
    spot = None
    color = None
    ex = None
    iso = None
    wb = None
    sharp = None

    ##mp4_meta from ffprfobe
    mp4_meta = None
    lrv_meta = None


    ##pathTofileatDownload
    path = None
    thm = None
    lrv = None
    mp4 = None
    tags = None

    def __init__(self, res, fps, fov, pt, ev, eis, spot, color, ex, iso, wb, sharp):
        self.res = res
        self.fps = fps
        self.fov = fov
        self.pt = pt
        self.ev = ev
        self.eis = eis
        self.spot = spot
        self.color = color
        self.ex = ex
        self.iso = iso
        self.wb = wb
        self.sharp = sharp

    def setCamera(self, camera):
        self.camera = camera

    def setValidate(self, validate):
        self.validate = validate

    def setMp4Path(self,path,mp4 ):
        self.path = path
        self.mp4 = mp4

    def setLrvPath(self,lrv):
        self.lrv = lrv

    def setThm(self,thm):
        self.thm = thm

    def setTags(self, tags):
        self.tags = tags


def downloadLastVideo(camera, fileDestinationPath):
    videoFilePath = camera.getNewestMediaItem("mp4")
    videoFilename = videoFilePath.split("/")[-1]

    camera.downloadMedia(videoFilePath, GpMediaType.LOW_RES_VIDEO,fileDestinationPath + videoFilename.replace("MP4", "LRV"))
    camera.waitForPollingPeriod()

    camera.downloadMedia(videoFilePath, GpMediaType.FULL,fileDestinationPath + videoFilename)
    camera.waitForPollingPeriod()

    camera.downloadMedia(videoFilePath, GpMediaType.THUMBNAIL,fileDestinationPath + videoFilename.replace("MP4", "THM"))
    camera.waitForPollingPeriod()



def recordVideo(camera, duration):
    milliDuration = duration * 1000
    camera.setShutter(True)
    camera.sleep(milliDuration)
    camera.setShutter(False)
    camera.waitForPollingPeriod()

def configureSettings(camera, VIDEO_OPTIONS_LIST):
    for setting in VIDEO_OPTIONS_LIST:
        if len(setting) != 2:
            camera.setSubmode(setting[0])
        else:

            camera.setSetting(setting[0],setting[1])
    camera.waitForPollingPeriod()


if __name__ == "__main__":


    VIDEO_OPTIONS_LIST = [
        [GpCameraSubmodes.VIDEO],
        [GpCameraSetting.VIDEO_RESOLUTION, GpCameraSettingOption.VIDEO_RESOLUTION_WVGA],
        [GpCameraSetting.VIDEO_FPS, GpCameraSettingOption.VIDEO_FPS_60],
        [GpCameraSetting.VIDEO_FOV, GpCameraSettingOption.VIDEO_FOV_WIDE],
        [GpCameraSetting.VIDEO_EIS, GpCameraSettingOption.VIDEO_EIS_ON],
        [GpCameraSetting.VIDEO_SPOT_METER, GpCameraSettingOption.VIDEO_SPOT_METER_ON],
        [GpCameraSetting.VIDEO_PROTUNE, GpCameraSettingOption.VIDEO_PROTUNE_ON],
        [GpCameraSetting.VIDEO_PROTUNE_EV, GpCameraSettingOption.VIDEO_PROTUNE_EV_2_0],
        [GpCameraSetting.VIDEO_PROTUNE_COLOR,GpCameraSettingOption.VIDEO_PROTUNE_COLOR_GOPRO_COLOR],
        [GpCameraSetting.VIDEO_PROTUNE_ISO, GpCameraSettingOption.VIDEO_PROTUNE_ISO_6400],
        [GpCameraSetting.VIDEO_PROTUNE_WHITE_BALANCE, GpCameraSettingOption.VIDEO_PROTUNE_WHITE_BALANCE_3000K],
        [GpCameraSetting.VIDEO_PROTUNE_SHARPNESS,GpCameraSettingOption.VIDEO_PROTUNE_SHARPNESS_HIGH],
    ]



    camera = GpCamera.connectOnCurrentWiFiNetwork()
    camera.deleteAllFilesOnSdCard()
    camera.waitForPollingPeriod()
    configureSettings(camera,VIDEO_OPTIONS_LIST)
    recordVideo(camera, 5)

    downloadLastVideo(camera, "media/")