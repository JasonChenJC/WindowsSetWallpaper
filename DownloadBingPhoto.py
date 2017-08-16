import urllib.request
from urllib import request
import os
from PIL import Image
import win32api,win32con,win32gui

print('Download data......')
url = 'http://cn.bing.com'
urlFile = urllib.request.urlopen(url)
data = urlFile.read()
urlFile.close()
data = data.decode('utf-8', errors='ignore')

# 图片路径的开始 g_img={url: "
# 图片路径的结束 #",id:'bgDiv'
pre = u'g_img={url: \"'
urlstart = data.find(pre) + len(pre)
urlend = data.find(u'\",id:', urlstart)
imgUrl = data[urlstart: urlend]

# 图片名称的开始
preImg = u'<a id=\"sh_cp\" class=\"sc_light\" title=\"'
imgnameStart = data.find(preImg) + len(preImg)
imgnameend = data.find('\" aria-label=\"', imgnameStart)
# print("start:"+str(imgnameStart))
# print("end:"+str(imgnameend))
imgName = data[imgnameStart: imgnameend] + u'.jpg'
imgName = imgName.replace("©", "")
imgName = imgName.replace("/", " ")
# imgName = "C:\\Users\\Public\\Pictures\\Sample Pictures\\" + imgName
imgName = "D:\\BingPhoto\\" + imgName
# print(url+imgUrl)
# print(imgName)
if os.path.exists(imgName) == False:
    print('Download image......')
    urllib.request.urlretrieve(url + imgUrl, imgName)

print('Download complete')

def set_wallpaper_from_bmp(bmp_path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_path, win32con.SPIF_SENDWININICHANGE)

# 需要把图片转换为BMP格式，否则win32gui.SystemParametersInfo会报错！
def setWallPaper(imagePath):
    bmpImage = Image.open(imagePath)
    newPath = imagePath.replace('.jpg', '.bmp')
    bmpImage.save(newPath, "BMP")
    set_wallpaper_from_bmp(newPath)

setWallPaper(imgName)

print("Set wallpaper complete!")