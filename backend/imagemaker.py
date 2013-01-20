import flashfoto
import json, requests, urllib
import base64, time
import random

# Peter's api stuff
# api:      A4jqruA3HggxWDxXQsIfnO9qoSnrkdZj
# username: nejstastnejsistene

# api:		IRAY8h1P1jyG7rKSuNc5rLMncWTvPJNm
# username: hrex

#def getBackground():
    #get stuff from mike's flickr scraper
    #should be a url
    #return

#def getForeground():
    #get picture user uploads from filepicker.io
    #should be a url
    #return

#retrieved at 1:15am
mikes_key = 'K6kNLOkY3TFkpHCw1HdIauVM9F5j83IH'

class Maker:
    fgID = None
    def __init__(self, fgroundURL):
        self.ff = flashfoto.FlashFoto(*random.choice([
            ('hrex', 'IRAY8h1P1jyG7rKSuNc5rLMncWTvPJNm'),
            ('nejstastnejsistene', 'A4jqruA3HggxWDxXQsIfnO9qoSnrkdZj'),
            ('Mike', 'K6kNLOkY3TFkpHCw1HdIauVM9F5j83IH')]))


        self.fgID = self.ff.add(params = {
            "location": base64.urlsafe_b64encode(fgroundURL),
            'privacy':'public'
        })['ImageVersion']['image_id']
        #print "foreground id? " , self.fgID
        self.ff.mugshot(self.fgID)
        while self.ff.mugshot_status(self.fgID) \
                ['mugshot_status'] == 'pending' :
            time.sleep(10)
        #print "\n STATUS " , self.ff.mugshot_status(self.fgID)
        if self.ff.mugshot_status(self.fgID) == 'failed':
            assert False


    def makePicture( self, bgroundURL ):
        bgID = self.ff.add(params = {
            "location": base64.urlsafe_b64encode(bgroundURL),
            'privacy': 'public'
            })['ImageVersion']['image_id']
        #print "background added, with id " + bgID
        bgInfo = self.ff.info(bgID)
    #print bgInfo
        bgHeight = bgInfo['ImageVersion'][0]['height']
        bgWidth = bgInfo['ImageVersion'][0]['width']
        mergeX = int(bgWidth) / 3

        mergedata = [{ "image_id": bgID }, {
            "image_id": self.fgID,
            "version": "MugshotMasked",
            "x": mergeX,
            "y": bgHeight ,
            "scale":"75" ,
            "angle":"0",
            "flip": 0
            }]
        mergedID = self.ff.merge(mergedata, params = {
            'privacy': 'public' } )['ImageVersion']['image_id']
        return "http://flashfotoapi.com/api/get/" + mergedID + \
            "?partner_username=ncschaaf&partner_apikey=DyRkKMSiYncpTaG2i7IuJy9FGA3bll5g"

    
def batchImages(fgroundURL , backgroundList):
    photo = Maker(fgroundURL)
    pictureList = []
    for url in backgroundList:
        pictureList.append(photo.makePicture(url))
    return pictureList
