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
        elif len(dPixels)== height-1 and cnt == width -1: #final case
            dPixels.append(curr_lst)
            break
        else:
            cnt+=1
            curr_lst.append(tup)

    return dPixels

def getUVDict(img_file):
    '''Returns dict where key= [u,v] and value= (R,G,B)'''
    width,height= getPicSize(img_file) #serve as step values
    uv_dict={}
    dPixels= get2DPicData(img_file)

    for r in range(height): #tracking row currently on
        #print(str(r))
        for c in range(width): #tracking column currently on
            uv=[(c+1.0)/width,1.0-(r+1.0)/height]
            # truncation process
            uv[0] = (int(width * uv[0])*1.0)/width
            uv[1] = (int(height * uv[1])*1.0)/height
            u,v = uv[0],uv[1]
            #print(str(uv))
            uv_dict[(u,v)]= dPixels[r-1][c-1]

    return uv_dict


'''
Test Area
'''
#print(str(getPicSize('test.jpg')))
#print(str(len(getPicData('test.jpg'))))
#print("getting tiny dimensions"+str(getPicSize('tiny.png')))
#tiny = get2DPicData('tiny.jpeg')
#print(str(tiny))
#print(str(len(tiny))) #rows
#print(str(len(tiny[0]))) #columns
# print(str(len(getUVDict('TEXTURE.jpg'))))
#print(str(len(get2DPicData('test.jpg')))) # rows
#print(str(len(get2DPicData('test.jpg')[0]))) #columns
