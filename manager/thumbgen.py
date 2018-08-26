from PIL import Image, ImageFile
import glob, os
from threading import *
ImageFile.LOAD_TRUNCATED_IMAGES = True
class Thumbgen:
    def __init__(self,file,fullname,identifier):
        sizes = [(32, 32),(64, 64),(128, 128),(256, 256),(512, 512),(1024, 1024),(2048, 2048)]
        self.generateThumb(identifier,file,fullname,sizes)

    def generateThumb(self,identifier,file,fullname,sizes):
        for size in sizes:
            t=Thread(target=generateImages,args=(identifier,file,fullname,size,))
            t.start()
            t.join()
        


def generateImages(identifier,file,fullname,size):
    #print "Open "+fullname
    im = Image.open(fullname)
    im.thumbnail(size)
    if not os.path.exists("website/static/thumbs/"+identifier+"/"):
        os.mkdir("website/static/thumbs/"+identifier+"/")
    file="website/static/thumbs/"+identifier+"/"+file.split(".")[0]+"_"+str(size[0])+"_"+str(size[1])
    im.save(file + ".png",format="PNG", quality=95, optimize=True, progressive=True)


if __name__=="__main__":
    filename="sample.png"
    t=Thumbgen(filename)
