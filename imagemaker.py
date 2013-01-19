import flashfoto.py
import json, requests, urllib

def getBackground():
    #get stuff from mike's flickr scraper
    #should be a url

def getForeground():
    #get picture user uploads from filepicker.io
    #should be a url

def makePicture( fgroundURL , bgroundURL ):
    ff = FlashFoto('ncschaaf', 'DyRkKMSiYncpTaG2i7IuJy9FGA3bll5g')#not sure if i need to add a baseurl
    fgID = ff.add(params = getForeground()) #might need to parse out image id; not sure exactly what is returned by this method
    print "foreground id? "+ fgID
    ff.mugshot(fgID)
    while ff.mugshot_status(fgID) == 'pending' :
        pass
    print ff.mugshot_status(fgID)

    if ff.mugshot_status(fgID) == 'failed':
        assert False

    bgID = ff.add(params = getBackground())#need parsing??

    mergedata = [{"image_id":bgID}, {"image_id":fgID, "version":"MugshotMasked", "x":"200", "y":"100" , "scale":"75" , "angle":"0", "flip":0}]
    return ff.merge(mergedata)# might want to bring this out to a url; make it easier to proccess elsewhere
    #return ff.get(mergedID)
    
    
makePicture(http://flashfotoapi.com/img/tut_mugshot1.png , )
