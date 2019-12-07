# -*- coding: utf-8 -*-

import time
from pypylon import pylon
import cv2

class CameraPylon:
    # Init
    # When exposure_us is zero, auto exposure is enabled.
    # When gain is zero, auto gain is enabled.
    def __init__(self, id=0, exposure_us=30000, gain=1.0):
        self.factory = pylon.TlFactory.GetInstance()
        self.devices = self.factory.EnumerateDevices()
        if len(self.devices) == 0:
            raise Exception('no camera present.')
        else:
            print(self.devices[0].GetFriendlyName())
        self.converter_bgr = pylon.ImageFormatConverter()
        self.converter_bgr.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter_bgr.OutputBitAlignment = 'MsbAligned'
        self.camera = pylon.InstantCamera(self.factory.CreateDevice(self.devices[id]))
        self.camera.Open()
        if exposure_us == 0:
            self.camera.ExposureAuto.SetValue('Continuous')
        else:
            self.camera.ExposureAuto.SetValue('Off')
            self.camera.ExposureTimeRaw.SetValue(exposure_us)
        if gain == 0:
            self.camera.GainAuto.SetValue('Continuous')
        else:
            self.camera.GainAuto.SetValue('Off')
            self.camera.Gain.SetValue(gain)
        print('--------------------')
        print('CameraPylon.__init__')
        print('--------------------')
        print('Width = {0}'.format(self.camera.Width.GetValue()))
        print('Height = {0}'.format(self.camera.Height.GetValue()))
        print('ExposureAuto = {0}'.format(self.camera.ExposureAuto.GetValue()))
        print('ExposureTime = {0}[us]'.format(self.camera.ExposureTimeRaw.GetValue()))
        print('GainAuto = {0}'.format(self.camera.GainAuto.GetValue()))
        print('Gain = {0}'.format(self.camera.Gain.GetValue()))
        print('')
        self.camera.Close()
    # Open
    def open(self):
        self.camera.Open()
    # Close
    def close(self):
        self.camera.Close()
    # Exposure time
    def setExposureTime(self, exposure_us=10000):
        if not self.camera.IsOpen():
            raise Exception('camera is not open.')
        if exposure_us == 0:
            self.camera.ExposureAuto.SetValue('Continuous')
        else:
            self.camera.ExposureAuto.SetValue('Off')
            self.camera.ExposureTimeRaw.SetValue(exposure_us)
        print('ExposureAuto = {0}'.format(self.camera.ExposureAuto.GetValue()))
        print('ExposureTime = {0}[us]'.format(self.camera.ExposureTimeRaw.GetValue()))
    # Gain
    def setGain(self, gain=1.0):
        if gain == 0:
            self.camera.GainAuto.SetValue('Continuous')
        else:
            self.camera.GainAuto.SetValue('Off')
            self.camera.Gain.SetValue(gain)
        print('GainAuto = {0}'.format(self.camera.GainAuto.GetValue()))
        print('Gain = {0}'.format(self.camera.Gain.GetValue()))
    # Grab
    # All convert to 24-bit BGR.
    def grab(self, timeout=1000):
        if not self.camera.IsOpen():
            raise Exception('camera is not open.')
        t_start = time.time()
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        grabResult = self.camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
        img_conv = self.converter_bgr.Convert(grabResult)
        grabResult.Release()
        self.camera.StopGrabbing()
        proc_time = time.time() - t_start
        print('grab time : {0} ms'.format(proc_time))
        return img_conv.GetArray()
    # View
    # Close with ESC.
    def view(self, delay=1):
        if not self.camera.IsOpen():
            raise Exception('camera is not open.')
        k = 0
        while k != 27:
            img = self.grab()
            cv2.namedWindow("img", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
            cv2.imshow("img", img)
            k = cv2.waitKey(delay)
        cv2.destroyAllWindows()
