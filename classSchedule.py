import configparser as ConfigParser
import pandas as pd
import numpy as np
import xlrd
# ['语文' '数 学' '英语' '政 治' '生 物' '历 史' '地 理' '体 育' '音 乐' '美 术' '健 康' '信 息' '综合实践']
commonClass=[23,24]
#每个学科的教研时间
classReserve={'语文':13,'数 学':29, '英语':13, '政 治':9, '生 物':25, '历 史':9, '地 理':9, '体 育':9, '音 乐':25, '美 术':25, '健 康':9, '信 息':25, '综合实践':25}
classA={'语文':6,'数 学':6, '英语':5, '政 治':2, '生 物':2, '历 史':3, '地 理':2, '体 育':3, '音 乐':1, '美 术':1, '健 康':1, '信 息':1, '综合实践':1}
classB={'语文':11,'数 学':5, '英语':5, '政 治':2, '生 物':2, '历 史':3, '地 理':2, '体 育':2, '音 乐':1, '美 术':1, '健 康':1, '信 息':1, '综合实践':1}
allClassTime=np.delete(np.arange(1,41),[0,22,23]).tolist()
class information():
    def __init__(self):
        self.excelRead()

    def excelRead(self):
        masterTeacherList=[]

        teacherExcel = pd.read_excel("C:/Users/sky/Desktop/课表/2019.9月人事安排表(2019.8.25).xlsx", encoding='UTF-8')
        columns=teacherExcel.columns.values
        #班级时间表
        # classList=teacherExcel.loc[:,columns[0]].values
        #科目
        subject=np.delete(columns,[0,1])
        classNumIndex=0
        # 教师时间信息
        self.teacherinfo = {}
        for i in subject:

            allclass=np.arange(1,41).tolist()
            allclass.remove(classReserve[i])
            teacherTime=allclass
            # print(teacherTime)
            classNumIndex=classNumIndex+1
            list=teacherExcel.loc[:,i].values
            for name in list:
                sigalteacher={name:teacherTime}
                # print(sigalteacher)
                self.teacherinfo.update(sigalteacher)
        # 班级老师信息，班级时间信息
        self.classTeacher={}
        for index in range(len(teacherExcel)):

            line=teacherExcel.loc[index].values.copy()
            # print(line)
            classTeacher=np.delete(line,[0,1])
            sigalClass={index+1:classTeacher}
            self.classTeacher.update(sigalClass)







if __name__ == '__main__':
    information=information()
    print(information.teacherinfo)
    print(information.classTeacher)
    print(len(information.classTeacher))