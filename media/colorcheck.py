from colorthief import ColorThief
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
imagepath = os.path.join(BASE_DIR,'/media/profilepics/')
color_thief = ColorThief('/home/manoj/Practice/Django/blogapp/media/profile_pics/itachi2.jpg')

dominant_color = color_thief.get_color(quality=1)
print('#%02x%02x%02x' % dominant_color)
print(imagepath)