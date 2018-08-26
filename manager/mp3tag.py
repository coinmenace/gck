import eyed3

class Tag:
    def __init__(self,filename,author,album,title,trackno):
        self.audiofile = eyed3.load(filename)
        self.audiofile.tag.artist = author
        self.audiofile.tag.album = album
        self.audiofile.tag.title = title
        self.audiofile.tag.track_num = trackno
        imagedata = open(albumcover,"rb").read()
        # append image to tags
        #The constant 3 means Front Cover, 4 means Back Cover, 0 for other
        self.audiofile.tag.images.set(3,imagedata,"image/jpeg",albumdescription)
        self.audiofile.tag.save()