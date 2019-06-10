'''
img directory contains currently parsed texture
takes in image and breaks up into u,v
[0][0] at upper left
Note that .png images will NOT work
'''
from PIL import Image

def getPicSize(img_file):
    '''Getting image dimensions for scaling'''
    img = Image.open('img/'+ str(img_file))
    width, height = img.size
    return width,height

def getPicData(img_file):
    '''Returns a flat list of RGB tuples from opened image'''
    img = Image.open('img/'+ str(img_file))
    pixels = list(img.getdata())
    return pixels

def get2DPicData(img_file): #possibly wrong?
    '''Returns a 2D array of RGB tuples from opened image.
    (broken up for testing)'''
    pixels= getPicData(img_file)
    width,height= getPicSize(img_file)
    #2D array building
    dPixels=[]
    curr_lst=[]
    cnt=0
    for tup in pixels:
        if width == cnt:
            dPixels.append(curr_lst)
            #print('curr_list'+str(len(curr_lst)))
            curr_lst= [] #reset
            curr_lst.append(tup)
            cnt=1
        elif len(dPixels)== height-1 and cnt == width -1:
            dPixels.append(curr_lst)
            break
        else:
            cnt+=1
            curr_lst.append(tup)

    return dPixels

def getUVScale(img_file):
    pass
def getUVDict(img_file):
    pass

#print(str(getPicSize('test.jpg')))
#print(str(len(getPicData('test.jpg'))))
#print("getting tiny dimensions"+str(getPicSize('tiny.png')))
tiny = get2DPicData('tiny.jpeg')
#print(str(tiny))
print(str(len(tiny))) #rows
print(str(len(tiny[0]))) #columns
#print(str(len(get2DPicData('test.jpg')))) # rows
#print(str(len(get2DPicData('test.jpg')[0]))) #columns
