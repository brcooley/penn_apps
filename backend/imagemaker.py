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

class Maker:
    ff = flashfoto.FlashFoto('ncschaaf', 'DyRkKMSiYncpTaG2i7IuJy9FGA3bll5g')#not sure if i need to add a baseurl
    fgID = None
    def __init__(self, fgroundURL):
        self.fgID = self.ff.add(params = {"location":base64.urlsafe_b64encode(fgroundURL), 'privacy':'public'})['ImageVersion']['image_id']
        print "foreground id? " , self.fgID
        self.ff.mugshot(self.fgID)
        while self.ff.mugshot_status(self.fgID)['mugshot_status'] == 'pending' :
            time.sleep(10)
        print "\n STATUS " , self.ff.mugshot_status(self.fgID)
        if self.ff.mugshot_status(self.fgID) == 'failed':
            assert False


    def makePicture( self, bgroundURL ):
        bgID = self.ff.add(params = {"location":base64.urlsafe_b64encode(bgroundURL), 'privacy':'public'})['ImageVersion']['image_id']
        print "background added, with id " + bgID
        bgInfo = self.ff.info(bgID)
    #print bgInfo
        bgHeight = bgInfo['ImageVersion'][0]['height']
        bgWidth = bgInfo['ImageVersion'][0]['width']
        mergeX = int(bgWidth) / 3

        mergedata = [{"image_id":bgID}, {"image_id":self.fgID, "version":"MugshotMasked", "x":mergeX, "y":bgHeight , "scale":"75" , "angle":"0", "flip":0}]
        mergedID = self.ff.merge(mergedata, params = {'privacy':'public'} )['ImageVersion']['image_id']
        return "http://flashfotoapi.com/api/get/" + mergedID +"?partner_username=ncschaaf&partner_apikey=DyRkKMSiYncpTaG2i7IuJy9FGA3bll5g"

    
def batchImages(fgroundURL , backgroundList):
    photo = Maker(fgroundURL)
    pictureList = []
    for url in backgroundList:
        pictureList.append(photo.makePicture(url))

    
#print makePicture( "http://imgur.com/fYUug5Q.jpg" , "http://farm9.staticflickr.com/8334/8391368003_b4880e7de5_h.jpg")
list =  ['http://farm9.staticflickr.com/8091/8387181473_f33d68c037_h.jpg', 'http://farm9.staticflickr.com/8044/8387180633_49c0d05b47_h.jpg', 'http://farm9.staticflickr.com/8083/8388268908_b130731814_h.jpg', 'http://farm9.staticflickr.com/8215/8387182735_a250fe5ca4_h.jpg', 'http://farm9.staticflickr.com/8367/8388265882_eddcd26dcb_h.jpg', 'http://farm9.staticflickr.com/8367/8387179707_05d1309a43_h.jpg', 'http://farm9.staticflickr.com/8351/8387176941_7c6b0a4261_h.jpg', 'http://farm9.staticflickr.com/8049/8387178285_b6cc0f1dc2_h.jpg', 'http://farm9.staticflickr.com/8369/8387177617_f6e21b946f_h.jpg', 'http://farm9.staticflickr.com/8508/8388263356_d0390cd3c2_h.jpg', 'http://farm8.staticflickr.com/7053/6898598007_7b1542914b_o.jpg', 'http://farm3.staticflickr.com/2427/3741344756_10caca5fb7_b.jpg', 'http://farm9.staticflickr.com/8154/7190324391_ecc4ef31bc_h.jpg', 'http://farm9.staticflickr.com/8001/7375567756_91940e586c_h.jpg', 'http://farm9.staticflickr.com/8142/7375568384_997b3a96e5_h.jpg', 'http://farm8.staticflickr.com/7086/7375567518_0faac731b6_h.jpg', 'http://farm8.staticflickr.com/7081/7190240121_99d58716e4_h.jpg', 'http://farm8.staticflickr.com/7214/7190241531_61920c528a_h.jpg', 'http://farm8.staticflickr.com/7222/7375484322_0ff442d6b7_h.jpg', 'http://farm6.staticflickr.com/5466/7190240397_acf3c6e821_h.jpg', 'http://farm8.staticflickr.com/7224/7190240855_91289c23fb_h.jpg', 'http://farm8.staticflickr.com/7227/7190239517_07c7aa6590_h.jpg', 'http://farm9.staticflickr.com/8166/7190057019_5b89be36d8_h.jpg', 'http://farm9.staticflickr.com/8167/7375297830_e6a0c11ce6_h.jpg', 'http://farm8.staticflickr.com/7212/7190054021_7c3e984aae_h.jpg', 'http://farm6.staticflickr.com/5444/7190054565_9866624a11_h.jpg', 'http://farm8.staticflickr.com/7105/7375296178_55e1dd5fe0_h.jpg', 'http://farm8.staticflickr.com/7224/7375298838_a4e8851363_h.jpg', 'http://farm6.staticflickr.com/5323/7375298086_0fcec91395_h.jpg', 'http://farm6.staticflickr.com/5347/7375297406_698b5b69d8_h.jpg', 'http://farm8.staticflickr.com/7226/7375298254_5d23b47950_h.jpg', 'http://farm8.staticflickr.com/7048/6858752643_374ef747ac_o.jpg', 'http://farm8.staticflickr.com/7007/6680851205_1c8cb1949e_o.jpg', 'http://farm8.staticflickr.com/7027/6680852847_1730031191_o.jpg', 'http://farm7.staticflickr.com/6105/6339638785_6958ab97de_o.jpg', 'http://farm7.staticflickr.com/6037/6275030310_9e472c48c1_o.jpg', 'http://farm7.staticflickr.com/6040/6246783452_9cc1386f5e_o.jpg', 'http://farm7.staticflickr.com/6099/6246254897_d9f6cc3eb5_o.jpg', 'http://farm4.staticflickr.com/3043/5818196687_f429060648_o.jpg', 'http://farm3.staticflickr.com/2728/5818759654_4da5d887bb_o.jpg', 'http://farm3.staticflickr.com/2066/5818192573_311e4d420c_o.jpg', 'http://farm4.staticflickr.com/3519/5818193333_b427d5a78e_o.jpg', 'http://farm3.staticflickr.com/2377/5818763058_ea938f844d_o.jpg', 'http://farm4.staticflickr.com/3525/5818762078_a33a2c2bf6_o.jpg', 'http://farm6.staticflickr.com/5301/5817959540_fd97623307_o.jpg', 'http://farm4.staticflickr.com/3179/5817958446_e09b271f3b_o.jpg', 'http://farm3.staticflickr.com/2251/5817391003_5a84a64194_o.jpg', 'http://farm3.staticflickr.com/2098/5817391285_c4771af251_o.jpg', 'http://farm4.staticflickr.com/3578/5817958692_90c546baf4_o.jpg', 'http://farm6.staticflickr.com/5120/5817952888_773b5f3421_o.jpg', 'http://farm4.staticflickr.com/3374/5817388097_1fd76f66bb_o.jpg', 'http://farm3.staticflickr.com/2150/5817953922_1a84c50f0d_o.jpg', 'http://farm6.staticflickr.com/5145/5817953640_6fa2e6ea66_o.jpg', 'http://farm3.staticflickr.com/2766/5817952594_d0255cef3c_o.jpg', 'http://farm4.staticflickr.com/3565/5817954530_7210c405de_o.jpg', 'http://farm3.staticflickr.com/2348/5817953142_7ddd3b2dba_o.jpg', 'http://farm6.staticflickr.com/5263/5817389033_f58d72ba97_o.jpg', 'http://farm3.staticflickr.com/2054/5817955424_ce3941d20b_o.jpg', 'http://farm3.staticflickr.com/2628/5817953384_e06ef519fc_o.jpg', 'http://farm6.staticflickr.com/5267/5817386479_e25a487c68_o.jpg', 'http://farm4.staticflickr.com/3061/5817954882_a92d27fa13_o.jpg', 'http://farm3.staticflickr.com/2452/5817956204_08eb8d4954_o.jpg', 'http://farm4.staticflickr.com/3289/5815793618_e7000af2ff_o.jpg', 'http://farm4.staticflickr.com/3580/5815794622_9c82b5ee4a_o.jpg', 'http://farm4.staticflickr.com/3233/5815793172_e9f5b812e0_o.jpg', 'http://farm4.staticflickr.com/3006/5815792750_b01f268e97_o.jpg', 'http://farm3.staticflickr.com/2440/5815224877_50853fe669_o.jpg', 'http://farm6.staticflickr.com/5103/5815224355_22cb0c8eea_o.jpg', 'http://farm3.staticflickr.com/2750/5815791274_44d87e8cf0_o.jpg', 'http://farm3.staticflickr.com/2125/5815794246_034e312e12_o.jpg', 'http://farm6.staticflickr.com/5037/5815228315_ac204c6f8f_o.jpg', 'http://farm4.staticflickr.com/3345/5815223431_1a8a681072_o.jpg', 'http://farm3.staticflickr.com/2151/5815787172_313ca998d6_o.jpg', 'http://farm4.staticflickr.com/3075/5815788058_15b7bc93cd_o.jpg', 'http://farm4.staticflickr.com/3426/5815218641_1b6743bd80_o.jpg', 'http://farm4.staticflickr.com/3294/5815788622_a5615ce8bf_o.jpg', 'http://farm4.staticflickr.com/3371/5815221489_88d4201ccf_o.jpg', 'http://farm6.staticflickr.com/5191/5815786750_370002e319_o.jpg', 'http://farm5.staticflickr.com/4096/5610708300_35552f1396_b.jpg', 'http://farm3.staticflickr.com/2678/4216433869_cdb463eca6_b.jpg', 'http://farm3.staticflickr.com/2532/4216431569_a968e7955d_b.jpg', 'http://farm4.staticflickr.com/3513/3741344728_57eddc51ba_b.jpg', 'http://farm4.staticflickr.com/3434/3741344734_a0dbc291df_b.jpg']

print batchImages("http://imgur.com/fYUug5Q.jpg", list[3:6])
