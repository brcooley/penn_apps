import flashfoto
import json, requests, urllib
import base64, time

#def getBackground():
    #get stuff from mike's flickr scraper
    #should be a url
    #return

#def getForeground():
    #get picture user uploads from filepicker.io
    #should be a url
    #return

def makePicture( fgroundURL , bgroundURL ):
    ff = flashfoto.FlashFoto('ncschaaf', 'DyRkKMSiYncpTaG2i7IuJy9FGA3bll5g')#not sure if i need to add a baseurl
    fgID = ff.add(params = {"location":base64.urlsafe_b64encode(fgroundURL), 'privacy':'public'})['ImageVersion']['image_id']

    #print
    print "foreground id? " , fgID
    #print
    #ff.findfaces(fgID)

    ff.mugshot(fgID)
    while ff.mugshot_status(fgID)['mugshot_status'] == 'pending' :
        time.sleep(10)

    print "\n STATUS " , ff.mugshot_status(fgID)

    if ff.mugshot_status(fgID) == 'failed':
        assert False
        
    
    #print '\n is the mugshot here??? '
    #ff.get(fgID, {'version':'MugshotMask'})


    print "adding background..."

    bgID = ff.add(params = {"location":base64.urlsafe_b64encode(bgroundURL), 'privacy':'public'})['ImageVersion']['image_id']


    #print
    print "background added, with id " + bgID
    #print

    bgInfo = ff.info(bgID)
    #print bgInfo
    bgHeight = bgInfo['ImageVersion'][0]['height']
    bgWidth = bgInfo['ImageVersion'][0]['width']
    mergeX = int(bgWidth) / 3


    print 'merging...'

    mergedata = [{"image_id":bgID}, {"image_id":fgID, "version":"MugshotMasked", "x":mergeX, "y":bgHeight , "scale":"75" , "angle":"0", "flip":0}]
    mergedID = ff.merge(mergedata, params = {'privacy':'public'} )['ImageVersion']['image_id']
    return "http://flashfotoapi.com/api/get/" + mergedID +"?partner_username=ncschaaf&partner_apikey=DyRkKMSiYncpTaG2i7IuJy9FGA3bll5g"
    #return ff.get(mergedID)
    
    
print makePicture("http://us.123rf.com/400wm/400/400/gelpi/gelpi0705/gelpi070500114/926294-attractive-young-person-businessman-a-over-white-background.jpg" , "http://farm9.staticflickr.com/8334/8391368003_b4880e7de5_h.jpg")