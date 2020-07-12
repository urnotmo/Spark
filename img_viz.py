from json_read import get_info
from json_read import dicom2array
import matplotlib.pyplot as plt
import os
train_path=r"C:\project\lumbar\Project-111\dataset\train_train51"
json_path=r"C:\project\lumbar\Project-111\dataset\train_train51\lumbar_train51_annotation.json"
# train_path=r"C:\Users\Administrator\Desktop\lumbar\dataset\lumbar_train51\train"
# json_path=r"C:\Users\Administrator\Desktop\lumbar\dataset\lumbar_train51\lumbar_train51_annotation.json"
#https://tianchi.aliyun.com/forum/postDetail?spm=5176.12586969.1002.12.46023a71FYtdgp&postId=113064

result=get_info(train_path,json_path)#图片路径以及标注


# plt.ion()
# for i in range(len(result)):
#     img_dir=result.index[i]#图片路径
#     print('图片{}路径'.format(i))
#     print(img_dir)
#     studyPath=os.path.split(img_dir)
#     # print(studyPath)
#     studyPath=os.path.split(studyPath[0])
#     studyID=studyPath[1]
#     # print(studyID)
#     img_arr=dicom2array(img_dir)
#     plt.title('{}‘s img'.format(studyID))
#     plt.imshow(img_arr,cmap='gray')
#     plt.show()
#     plt.pause(1)
#     plt.clf()
# plt.ioff()

tags=result[1]#图片的标注信息
# 如何索引Series类型？
print(result)
exit()
coord=tag['coord']#获取这个标签所在的坐标
#显示图片
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
#把这个图片所有的tags都加上去
for tag in tags:
    coord=tag['coord']
    top_left_x,top_left_y=coord[0]-7,coord[0]-7
    width,height=14,14
    rect=plt.Rectangle((top_left_x,top_left_y),width,height,fill=False,edgecolor='red',linewidth=1)
    ax.add_patch(rect)
# plt.imshow(img_arr,cmap='gray')
# plt.show()
