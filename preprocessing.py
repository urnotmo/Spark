# import SimpleITK as sitk
#
# def dicom_metainfo(dicm_path, list_tag):
#     '''
#     获取dicom的元数据信息
#     :param dicm_path: dicom文件地址
#     :param list_tag: 标记名称列表,比如['0008|0018',]
#     :return:
#     '''
#     reader = sitk.ImageFileReader()
#     reader.LoadPrivateTagsOn()
#     reader.SetFileName(dicm_path)
#     reader.ReadImageInformation()
#     return [reader.GetMetaData(t) for t in list_tag]
#
#
# def dicom2array(dcm_path):
#     '''
#     读取dicom文件并把其转化为灰度图(np.array)
#     https://simpleitk.readthedocs.io/en/master/link_DicomConvert_docs.html
#     :param dcm_path: dicom文件
#     :return:
#     '''
#     image_file_reader = sitk.ImageFileReader()
#     image_file_reader.SetImageIO('GDCMImageIO')
#     image_file_reader.SetFileName(dcm_path)
#     image_file_reader.ReadImageInformation()
#     image = image_file_reader.Execute()
#     if image.GetNumberOfComponentsPerPixel() == 1:
#         image = sitk.RescaleIntensity(image, 0, 255)
#         if image_file_reader.GetMetaData('0028|0004').strip() == 'MONOCHROME1':
#             image = sitk.InvertIntensity(image, maximum=255)
#         image = sitk.Cast(image, sitk.sitkUInt8)
#     img_x = sitk.GetArrayFromImage(image)[0]
#     return img_x
#
# # studyUid='0020|000d',seriesUid='0020|000e',instanceUid='0008|0018'
# if __name__ == '__main__':
#     import cv2
#     dcm_path=r'D:\Spark_data\lumbar_train51\train\study23\image6.dcm'
#     # list_tag = [0o018, 0o050]
#     img_x= dicom2array(dcm_path)
#     img_info = dicom_metainfo(dcm_path, )
#     cv2.imshow('0',img_x)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#



#将所有的数据处理函数都包含到此文件下
import SimpleITK as sitk
import os
import json
import glob
import SimpleITK as sitk
import pandas as pd
import matplotlib.pyplot as plt
import time


# dcm数据处理函数
def dicom_metainfo(dicm_path, list_tag):
    '''
    获取dicom的元数据信息
    :param dicm_path: dicom文件地址
    :param list_tag: 标记名称列表,比如['0008|0018',]
    :return:
    '''
    reader = sitk.ImageFileReader()
    reader.LoadPrivateTagsOn()
    reader.SetFileName(dicm_path)
    reader.ReadImageInformation()
    return [reader.GetMetaData(t) for t in list_tag]


def dicom2array(dcm_path):
    '''
    读取dicom文件并把其转化为灰度图(np.array)
    https://simpleitk.readthedocs.io/en/master/link_DicomConvert_docs.html
    :param dcm_path: dicom文件
    :return:
    '''
    image_file_reader = sitk.ImageFileReader()
    image_file_reader.SetImageIO('GDCMImageIO')
    image_file_reader.SetFileName(dcm_path)
    image_file_reader.ReadImageInformation()
    image = image_file_reader.Execute()
    if image.GetNumberOfComponentsPerPixel() == 1:
        image = sitk.RescaleIntensity(image, 0, 255)
        if image_file_reader.GetMetaData('0028|0004').strip() == 'MONOCHROME1':
            image = sitk.InvertIntensity(image, maximum=255)
        image = sitk.Cast(image, sitk.sitkUInt8)
    img_x = sitk.GetArrayFromImage(image)[0]
    return img_x

# json文件处理函数
def get_info(train_path,json_path):
    annotation_info = pd.DataFrame(columns=('studyUid','seriesUid','instanceUid','annotation'))
    json_df = pd.read_json(json_path)

    for idx in json_df.index:
        studyUid = json_df.loc[idx,"studyUid"]
        seriesUid = json_df.loc[idx,"data"][0]['seriesUid']
        instanceUid =  json_df.loc[idx,"data"][0]['instanceUid']
        annotation =  json_df.loc[idx,"data"][0]['annotation']
        row = pd.Series({'studyUid':studyUid,'seriesUid':seriesUid,'instanceUid':instanceUid,'annotation':annotation})
        annotation_info = annotation_info.append(row,ignore_index=True)
    dcm_paths = glob.glob(os.path.join(train_path,"**","**.dcm"))

    tag_list = ['0020|000d','0020|000e','0008|0018']
    dcm_info = pd.DataFrame(columns=('dcmPath','studyUid','seriesUid','instanceUid'))


    for dcm_path in dcm_paths:
        try:
            studyUid,seriesUid,instanceUid = dicom_metainfo(dcm_path,tag_list)
            row = pd.Series({'dcmPath':dcm_path,'studyUid':studyUid,'seriesUid':seriesUid,'instanceUid':instanceUid })
            dcm_info = dcm_info.append(row,ignore_index=True)
        except:
            continue
    result = pd.merge(annotation_info,dcm_info,on=['studyUid','seriesUid','instanceUid'])
    result = result.set_index('dcmPath')['annotation'] #返回图片路径与标注信息
    return result

# 得到数据（array类型）和标签的函数
def DataLabelGenerator(DATA_PATH,JSON_PATH,idx):
    result=get_info(DATA_PATH,JSON_PATH)
    #将读图转换为array
    img_dir=result.index[idx] #第idx的图片路径
    img_arr=dicom2array(img_dir)
    #获取标注信息
    tags=result[idx]
    annoation=tags[0]['data']['point']
    #坐标
    coord=[]
    #脊椎ID
    id=[]
    #腰间盘
    disc=[]
    #腰椎
    vertebra=[]
    for j in range(len(annoation)):
        coord_list=annoation[j]['coord']
        coord.append(coord_list)

        id_name=annoation[j]['tag']['identification']
        id.append(id_name)

        name=annoation[j]['tag']
        vertebra_label=name.get('vertebra')
        vertebra.append(vertebra_label)

        disc_label=name.get('disc')
        disc.append(disc_label)
    return img_arr,coord,id,disc,vertebra

# 一下代码是测试，也可以做模板
DATA_PATH=r"D:\Spark_data\lumbar_train51\train"
JSON_PATH=r"C:\Users\lieweiai\Desktop\json1.txt"
idx=50
tic = time.time()
img_arr,coord,id,disc,vertebra=DataLabelGenerator(DATA_PATH,JSON_PATH,idx)

plt.title("{}\'s img ".format(idx))
for j in coord:
    x,y=j
    plt.scatter(x,y,c='r',s=3)
plt.imshow(img_arr,cmap='gray')
plt.show()
toc = time.time()
print(toc-tic)







