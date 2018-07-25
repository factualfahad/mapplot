import urllib
import matplotlib.pylab as plt
import math


w=640;
h=640;
zoom=17;
lat=42.372648;
lng=-71.117057;
scale=2;


def mapPoints(lats,lngs,args_corrected=False,args_center=[0,0],args_width=640,args_hight=640,args_zoom=17,args_scale=2):
    global zoom,scale,lat,lng,w,h;
    #this part handles arguments to the function and correction of coordinates
    w=args_width;
    h=args_hight;
    zoom=args_zoom;
    scale=args_scale;
    lat=args_center[0];
    lng=args_center[1];
    if scale>2:
        print('scale is too high, a maximum value of 2 will be used.');
        scale=2;
    if args_center[0]==0 and args_center[1]==0:
        print('no center coordinate was use, the default of (0.0,0.0) will be used.')
    if not args_corrected:
        lats_corrected=[];
        lngs_corrected=[];
        for i in range(0,len(lats)):
            x,y=reverse_getPointLatLng(lats[i],lngs[i]);
            lats_corrected.append(x);
            lngs_corrected.append(y);     
    else:
        lats_corrected=lats;
        lngs_corrected=lngs;

    ## this part is for plotting the data over an image 
    query="http://maps.googleapis.com/maps/api/staticmap?center="+str(lat)+","+str(lng)+"&zoom="+str(zoom)+"&size="+str(w)+"x"+str(h)+"&scale="+str(scale)+"&maptype=roadmap"
    pic=urllib.request.urlretrieve(query, "tmp.png")
    pic=plt.imread('tmp.png')
    plt.figure(figsize=(15,15))
    plt.imshow(pic)
    plt.plot(lats_corrected,lngs_corrected,'.')
    plt.xlim([0,scale*640]);
    mapplot=plt.ylim([scale*640,6]);
    return mapplot;


def getPointLatLng(x, y):
    parallelMultiplier = math.cos(lat * math.pi / 180)
    degreesPerPixelX = 360 / math.pow(2, zoom + 8)
    degreesPerPixelY = 360 / math.pow(2, zoom + 8) * parallelMultiplier;
    pointLat = lat - degreesPerPixelY * ( y - h / 2)
    pointLng = lng + degreesPerPixelX * ( x  - w / 2)

    return (pointLat, pointLng)

def reverse_getPointLatLng(pointLat, pointLng):
    parallelMultiplier = math.cos(lat * math.pi / 180)
    degreesPerPixelX = 360 / math.pow(2, zoom + 8)
    degreesPerPixelY = 360 / math.pow(2, zoom + 8) * parallelMultiplier;
    #pointLat = lat - degreesPerPixelY * ( y - h / 2)
    #pointLng = lng + degreesPerPixelX * ( x  - w / 2)
    y=scale*((2*(lat-pointLat)/(degreesPerPixelY))+h)/2;
    x=scale*((2*(pointLng-lng)/(degreesPerPixelX))+w)/2;
    return (x, y)



