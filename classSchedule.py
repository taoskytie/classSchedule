import configparser as ConfigParser
import pandas as pd
import numpy as np
# ['语文' '数 学' '英语' '政 治' '生 物' '历 史' '地 理' '体 育' '音 乐' '美 术' '健 康' '信 息' '综合实践']
commonClass=[23,24]
classReserve={'语文':13,'数 学':29, '英语':13, '政 治':9, '生 物':25, '历 史':9, '地 理':9, '体 育':9, '音 乐':25, '美 术':25, '健 康':9, '信 息':25, '综合实践':25}
allclass=np.delete(np.arange(1,41),[22,23])
class teacher():
    def __init__(self):
        self.excelRead()

    def excelRead(self):
        masterTeacherList=[]
        teacherinfo={}
        teacherExcel = pd.read_excel("C:/Users/sky/Desktop/课表/2019.9月人事安排表(2019.8.25).xlsx", encoding='UTF-8')
        columns=teacherExcel.columns.values
        #班级时间表
        classList=teacherExcel.loc[:,columns[0]].values
        #科目
        self.subject=np.delete(columns,[0,1])
        classNumIndex=0
        for i in self.subject:

            classNumIndex=classNumIndex+1
            list=teacherExcel.loc[:,i].values
            # teacherinfo.update(i)

        return columns






if __name__ == '__main__':
    teacher=teacher()
    print(teacher.subject)