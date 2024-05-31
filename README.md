# pypylon_sample01

This is a sample of pypylon.

Copy wk_camera_pylon.py to the Lib folder.

Try the following.

```
from wk_camera_pylon import *

cam = CameraPylon()
cam.open()
cam.view()
img = cam.grab()

help(wk_camera_pylon)
```
