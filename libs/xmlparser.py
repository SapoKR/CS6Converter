from typing import Union
from io import TextIOWrapper
import xmltodict
from PIL import Image


#@njit(nopython=True, cache=True, fastmath=True)
#def AreaDetect(ImageSize: tuple, AreaSize: tuple):
#    area = list(range(*AreaSize))
#    if len([i for i in list(range(*ImageSize)) if i in area]):
#        return True
#    return False

class xmlparser():
    def __init__(self, file: Union[str, TextIOWrapper]):
        self.file : TextIOWrapper = open(file, "r", encoding='utf-16') if isinstance(file, str) else file
        self.content : str = ""
    
    def parse(self):
        self.file.seek(0)
        self.content = xmltodict.parse(self.file.read())
        return self.content

    def imageparse(self, ImageName: str = None):
        self.content = self.content or self.parse()
        img = Image.open(ImageName)
        imgs = {}
        for i in self.content['TextureAtlas']['SubTexture']:
            areas = {k: int(v) for k, v in dict(filter(lambda a: a[0] != "@name", i.items())).items()}
            imgs[i['@name']] = img.crop((areas['@x'], areas['@y'], areas['@x']+areas['@width'], areas['@y']+areas['@height']))
            imgs[i['@name']+"_position"] = (areas['@x'], areas['@y'], areas['@x']+areas['@width'], areas['@y']+areas['@height'])
        
        return imgs

    #def optimize(self, ImageName: str = None):
    #    self.content = self.content or self.parse()
    #    ImageName = ImageName or self.content['TextureAtlas']['@imagePath']
    #    imgs = self.imageparse(ImageName)
    #    sheet = Image.new("RGBA", (4096, 4096))
    #    position = [0, 0]
    #    lastpos = [0, 0]
    #    tmp = 0
    #    size = 0
    #    splitint = int(round(math.sqrt(sum([i.size[0] for i in list(imgs.values())]))) / len(imgs))
    #    while tmp < len(imgs):
    #        img = list(imgs.values())[tmp]
    #        print(sum([i.size[0] for i in list(imgs.values())]))
    #        Image.Image.paste(sheet, img, tuple(position))
    #        if tmp % splitint == 0 or sum([i.size[0] for i in list(imgs.values())[0:tmp+1]]) >= sum([i.size[0] for i in list(imgs.values())[tmp:len(imgs)-1]]):
    #            
    #            if len(imgs)-(tmp+1) >= splitint:
    #                position[1]+=img.size[1]
    #            position[0]=0
    #            
    #            lastpos[1]=position[1]
    #        else:
    #            position[0]+=img.size[0]
    #            lastpos[0] = position[0] if position[0] != 0 and lastpos[0] <= position[0] else lastpos[0]
    #        tmp+=1
    #    fullarea = [0, 0, *lastpos]
    #    return sheet#.crop(tuple(fullarea))


                
    def convert(self):
        self.content = self.content or self.parse()
        
        return xmltodict.unparse(self.content)
        


