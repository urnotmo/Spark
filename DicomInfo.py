# import cv2
#
# img = cv2.imread("img/img_1.png")
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# #锐化处理
# dst0 = cv2.GaussianBlur(img,(5,5),0)
# dst0 = cv2.addWeighted(img,2,dst0,-1,0)
#
# # print(img.shape)
# con = cv2.convertScaleAbs(gray,alpha=3,beta=15)
# ret,bin_img = cv2.threshold(con,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# clach = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(3,3))
# dst = clach.apply(con)
# cv2.imshow("img",img)
# cv2.imshow("gray",gray)
# cv2.imshow("bin",bin_img)
# cv2.imshow("con",con)
# cv2.imshow("dst",dst)
# cv2.imshow("dst0",dst0)
# cv2.waitKey(0)




import os
import numpy as np
import SimpleITK as sitk
from matplotlib import pyplot as plt

# img = sitk.ReadImage('study0/image7.dcm')
# img_data = np.squeeze(si.GetArrayFromImage(img))
# print(img_data.shape)
# plt.imshow(img_data,cmap='gray')
# plt.show()
# exit()

PathDicom = "study0/"  # 与python文件同一个目录下的文件夹
lstFilesDCM = []
for dirName, subdirList, fileList in os.walk(PathDicom):
    # print(dirName,subdirList,fileList)
    for filename in fileList:
        if ".dcm" in filename.lower():  # 判断文件是否为dicom文件
            # print(filename)
            lstFilesDCM.append(os.path.join(dirName, filename))  # 加入到列表中
fig = plt.figure(figsize=(500,500))
for i in range(len(lstFilesDCM)):
    plt.subplot(5,len(lstFilesDCM)//5+1,i+1)
    img = np.squeeze(sitk.GetArrayFromImage(sitk.ReadImage(lstFilesDCM[i])))
    plt.imshow(img,cmap='gray')
    # plt.imsave("img/img_{}.png".format(i),img)
plt.show()

# raw_data = si.ReadImage(lstFilesDCM[0])
# img = si.GetArrayFromImage(raw_data)
# print(raw_data)
