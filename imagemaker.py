import flashfoto
import json, requests, urllib
import base64, time

def getBackground():
    #get stuff from mike's flickr scraper
    #should be a url
    return

def getForeground():
    #get picture user uploads from filepicker.io
    #should be a url
    return

def makePicture( fgroundURL , bgroundURL ):
    ff = flashfoto.FlashFoto('ncschaaf', 'DyRkKMSiYncpTaG2i7IuJy9FGA3bll5g')#not sure if i need to add a baseurl
    fgID = ff.add(params = {"location":base64.urlsafe_b64encode(fgroundURL), 'privacy':'public'})['ImageVersion']['image_id']

    print
    print "foreground id? " , fgID
    print


    ff.mugshot(fgID)
    while ff.mugshot_status(fgID) == 'pending' :
        time.sleep(2)
    print "\n STATUS " , ff.mugshot_status(fgID)

    if ff.mugshot_status(fgID) == 'failed':
        assert False

    print "adding background..."

    bgID = ff.add(params = {"location":base64.urlsafe_b64encode(bgroundURL), 'privacy':'public'})['ImageVersion']['image_id']


    print
    print "background added, with id " + bgID
    print
    print 'merging...'

    mergedata = [{"image_id":bgID}, {"image_id":fgID, "version":"MugshotMasked", "x":"200", "y":"100" , "scale":"75" , "angle":"0", "flip":0}]
    return ff.merge(mergedata)# might want to bring this out to a url; make it easier to proccess elsewhere
    #return ff.get(mergedID)
    
    
print makePicture("http://us.123rf.com/400wm/400/400/gelpi/gelpi0705/gelpi070500114/926294-attractive-young-person-businessman-a-over-white-background.jpg" , "http://farm9.staticflickr.com/8334/8391368003_b4880e7de5_h.jpg")
