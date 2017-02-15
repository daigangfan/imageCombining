import os,sys
from PIL import Image
import numpy as np
OUT_PATH='output-image'
INPUT_DIR='input-image'
TARGET_DIR='target-image'
VERTICAL_NUM=100
HORIZONTAL_NUM=100


class Tile:
    def __init__(self,path,size):#size is a tuple with (x,y),calculated by class target,path is the input path
        self.image=Image.open(path)
        self.pixels=self.process(path,size)
        self.average_dict=self.calculate_average(self.pixels,size)
    def process(self,path,size):
        self.image=self.image.resize(size,Image.ANTIALIAS)
        image_pixels=self.image.load()
        return image_pixels

    def calculate_average(self,pixels,size):
        pixdict={"r":[],"g":[],"b":[]}
        for x in range(size[0]):
            for y in range(size[1]):
                pixdict['r'].append(pixels[x,y][0])
                pixdict['g'].append(pixels[x,y][1])
                pixdict['b'].append(pixels[x,y][2])
        for k in pixdict.keys():
            pixdict[k]=np.average(pixdict[k])
        return pixdict


class Target:
    def __init__(self,path):
        self.image=Image.open(path)
        self.image=self.image.resize((self.image.size[0]*5,self.image.size[1]*5),Image.ANTIALIAS)
        self.tile_size=self.calculate_size()
        self.image=self.image.resize((self.tile_size[0]*HORIZONTAL_NUM,self.tile_size[1]*VERTICAL_NUM),Image.ANTIALIAS)
        self.aver_array=self.split_target(self.tile_size)

    def calculate_size(self):
        vertical_size=int(round(self.image.size[1]/VERTICAL_NUM,0))
        horizontal_size=int(round(self.image.size[0]/HORIZONTAL_NUM,0))
        return horizontal_size,vertical_size

    def split_target(self,size):
        img_size=self.image.size
        array=np.zeros((3,HORIZONTAL_NUM,VERTICAL_NUM))
        for i in range(0,img_size[0],size[0]):
            for j in range(0,img_size[1],size[1]):
                pix_dict={'r':[],'g':[],'b':[]}
                crop=self.image.crop((i,j,i+size[0],j+size[1]))
                crop_size=crop.size
                for x in range(crop_size[0]):
                    for y in range(crop_size[1]):
                        pix_dict['r'].append(crop.load()[x,y][0])
                        pix_dict['g'].append(crop.load()[x,y][1])
                        pix_dict['b'].append(crop.load()[x,y][2])
                pix_dict['r']=np.average(pix_dict['r'])
                pix_dict['g']=np.average(pix_dict['g'])
                pix_dict['b']=np.average(pix_dict['b'])
                x_n=int(i/size[0])
                y_n=int(j/size[1])
                array[0,x_n,y_n]=pix_dict['r']
                array[1,x_n,y_n]=pix_dict['g']
                array[2,x_n,y_n]=pix_dict['b']
        return array


if __name__=='__main__':
    target_image=os.listdir(TARGET_DIR)
    tile_list=[]
    input_image=os.listdir(INPUT_DIR)
    best_index=0
    for name in target_image:
        path=os.path.join(TARGET_DIR,name)
        target=Target(path)
        outImage=Image.new('RGB',target.image.size)
        for in_name in input_image:
            in_path=os.path.join(INPUT_DIR,in_name)
            tile=Tile(in_path,target.tile_size)
            tile_list.append(tile)

        for x_tile in range(HORIZONTAL_NUM):
            for y_tile in range(VERTICAL_NUM):
                min_diff = sys.maxsize
                target_r=target.aver_array[0,x_tile,y_tile]
                target_g=target.aver_array[1,x_tile,y_tile]
                target_b=target.aver_array[2,x_tile,y_tile]
                for index,tile in enumerate(tile_list):
                    diff=(tile.average_dict['r']-target_r)**2+(tile.average_dict['g']-target_g)**2+(tile.average_dict['b']-target_b)**2
                    if diff<min_diff:
                        min_diff=diff
                        best_index=index
                outImage.paste(tile_list[best_index].image,(x_tile*target.tile_size[0],y_tile*target.tile_size[1]))
        outImage.save(os.path.join(OUT_PATH,'out_'+name))








