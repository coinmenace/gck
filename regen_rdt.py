import pyminizip
import os


def generatePackage(imagefile,documentfile,audiofile,outputfile,secret,identifier):
    if not os.path.exists("static/rdt"):
        os.mkdir("static/rdt/")
    inputfiles =[]
    inputfiles.append(imagefile)
    inputfiles.append(documentfile)
    inputfiles.append(audiofile)
    print inputfiles
    try:
        pyminizip.compress_multiple(inputfiles, outputfile, secret, 5)
    except Exception as ex:
        print ex