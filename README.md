# pypylon_sanpmple001

This is a sample of pypylon.

Copy camera_pylon.py to the Lib folder.

Try the following.

```
from camera_pylon import *

cam = CameraPylon()
cam.open()
cam.view()
img = cam.grab()
```
