import cv2
import numpy as np
import os
from math import ceil

BLACK = [0,0,0]

data_dir=r'D:\17_png_dcxr\all_cxr\1'
save_dir=r'D:\17_png_dcxr\cropped_all\1'





def padding_to_findbox(datapath):
    ul_x = 10000
    ul_y = 10000
    dr_x = 0
    dr_y = 0
    data_dir=datapath
    for phase in os.listdir(data_dir):

        phase_dir=os.path.join(data_dir,phase)
        phase_img=cv2.imread(phase_dir)
        phase_img=cv2.cvtColor(phase_img,cv2.COLOR_BGR2GRAY)

        shape=phase_img.shape
        ori_h=shape[0]
        ori_w=shape[1]
        l=max(ori_w,ori_h)
        p_h1=int(0.5*(l-ori_h))
        p_h2=ceil(0.5*(l-ori_h))
        p_w1=int(0.5*(l-ori_w))
        p_w2=ceil(0.5 * (l - ori_w))

        padded = cv2.copyMakeBorder(phase_img,p_h1,p_h2,p_w1,p_w2, cv2.BORDER_CONSTANT, value=BLACK)
        mask= (padded>0).astype(np.uint8)
        print(type(mask),mask.shape,np.max(mask))
        x,y,w,h=cv2.boundingRect(mask)
        ul_x=min(ul_x,x)
        ul_y=min(ul_y,y)
        dr_x=max(dr_x,x+w)
        dr_y=max(dr_y,y+h)
        print(x,y,w,h)

        # #change bounding rectangle to bounding square
    b_h=dr_y-ul_y
    b_w=dr_x-ul_x
    l = max(b_h,b_w)
    if b_w>b_h:
        ul_y=int(ul_y-0.5*(b_w-b_h))
    else:
        ul_x=int(ul_x-0.5*(b_h-b_w))


    #-10 and +20 is to leave some space at the border
    return (ul_x-10,ul_y-10,l+20)



def padding_and_segmentation(datapath,savepath,plots):
    (ul_x,ul_y,ls)=plots
    data_dir = datapath
    save_dir=savepath
    for phase in os.listdir(data_dir):
        phase_dir = os.path.join(data_dir, phase)
        phase_img = cv2.imread(phase_dir)
        phase_img = cv2.cvtColor(phase_img, cv2.COLOR_BGR2GRAY)

        shape = phase_img.shape
        ori_h = shape[0]
        ori_w = shape[1]
        l = max(ori_w, ori_h)
        p_h1 = int(0.5 * (l - ori_h))
        p_h2 = ceil(0.5 * (l - ori_h))
        p_w1 = int(0.5 * (l - ori_w))
        p_w2 = ceil(0.5 * (l - ori_w))

        padded = cv2.copyMakeBorder(phase_img, p_h1, p_h2, p_w1, p_w2, cv2.BORDER_CONSTANT, value=BLACK)
        segged=padded[ul_y:ul_y+ls,ul_x:ul_x+ls]
        save_path=os.path.join(save_dir,phase)
        cv2.imwrite(save_path,segged)

plots=padding_to_findbox(data_dir)
print(plots)
padding_and_segmentation(data_dir,save_dir,plots)


all_data_dir=r'D:\17_png_dcxr\all_cxr'
all_cropped_dir=r'D:\17_png_dcxr\all_cropped'

for case in os.listdir(all_data_dir):
    case_data_dir=os.path.join(all_data_dir,case)
    case_save_dir=os.path.join(all_cropped_dir,case)
    if not os.path.exists(case_save_dir):
        os.makedirs(case_save_dir)
    plots = padding_to_findbox(case_data_dir)

    padding_and_segmentation(case_data_dir, case_save_dir, plots)


