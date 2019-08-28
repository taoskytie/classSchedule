import configparser as ConfigParser
import copy
import time

import pandas as pd
import numpy as np
import random
import xlrd
# ['语文', '数 学', '英语', '政 治', '生 物', '历 史' ,'地 理' ,'体 育', '音 乐', '美 术', '健 康' ,'信 息' ,'综合实践']
commonClass=[23,24]
#每个学科的教研时间
classReserve={'语文':13,'数 学':29, '英语':13, '政 治':9, '生 物':25, '历 史':9, '地 理':9, '体 育':9, '音 乐':25, '美 术':25, '健 康':9, '信 息':25, '综合实践':25}
# 1-4classA，5-18classB
# classA={'语文':6,'数 学':6, '英语':5, '政 治':2, '生 物':2, '历 史':3, '地 理':2, '体 育':3, '音 乐':1, '美 术':1, '健 康':1, '信 息':1, '综合实践':1}
# classB={'语文':11,'数 学':5, '英语':5, '政 治':2, '生 物':2, '历 史':3, '地 理':2, '体 育':2, '音 乐':1, '美 术':1, '健 康':1, '信 息':1, '综合实践':1}
classA=[6,6,5,2,2,3,2,3,1,1,1,1,1]
classB=[11,5,5,2,2,3,2,2,1,1,1,1,1]
# 班级可用时间,去除第一节，八节班会，24、25社团
allClassTime=np.delete(np.arange(1,41),[0,7,22,23]).tolist()
# 教师可用时间,去除第一节
allclass=np.arange(2,41).tolist()
#数语外老师特殊时间,去除第一节
specialTime=[2,3,9,10,11,17,18,19,25,26,27,33,34,35]
class information():
    def __init__(self):
        # self.subject
        # self.classList
        # self.teacherinfo
        # self.classTeacher
        self.excelRead()

    def excelRead(self):
        masterTeacherList=[]

        teacherExcel = pd.read_excel("C:/Users/sky/Desktop/课表/2019.9月人事安排表(2019.8.25).xlsx", encoding='UTF-8')
        columns=teacherExcel.columns.values
        #班级时间表
        self.classList=teacherExcel.loc[:,columns[0]].values
        # 班主任名单
        self.masterTeacher=teacherExcel.loc[:,columns[1]].values
        #科目
        self.subject=np.delete(columns,[0,1])
        classNumIndex=0
        # 教师时间信息
        self.teacherinfo = {}
        for i in self.subject:
            allteacher=allclass.copy()
            # if语句可以注释掉，就是没有分特殊学科
            if i=="语文"or i=="数学" or i=="英语":
                allteacher=specialTime.copy()

            try:
                allteacher.remove(classReserve[i])
            except :
                print(i+"老师的时间不包含"+str(classReserve[i]))

            teacherTime=allteacher
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


def scheduleSys(infom):
    # 1-18班班级列表
    classList = infom.classList

    # 学科顺序表，['语文', '数 学', '英语', '政 治', '生 物', '历 史' ,'地 理' ,'体 育', '音 乐', '美 术', '健 康' ,'信 息' ,'综合实践']
    subject=info.subject

    #每个老师空余时间表
    teacherTime={}
    teacherTime = infom.teacherinfo.copy()
    # print(id(infom.teacherinfo))
    # print(id(teacherTime))
    # print(teacherTime["徐盛轶"])
    # aaa=teacherTime
    # aaa["徐盛轶"].remove(2)
    # print(id(aaa))
    # print(aaa["徐盛轶"])
    # print(teacherTime["徐盛轶"])
    # print(infom.teacherinfo["徐盛轶"])
    # return False

    # 所有班级空余时间表
    # classTime={}
    # for i in classList:
    #     signalClassTime={i:allClassTime.copy()}
    #     classTime.update(signalClassTime)
    # print(classTime)

    # 每班对应老师名单
    classTeacher=infom.classTeacher.copy()

    # 每班老师排版表，输出
    classTeacherPlan={}

    # 每班学科排班表，输出
    classSubjectPlan={}

    # 循环遍历每个班
    for i in classList:
        print("开始遍历班级："+str(i))
        if i<=4:
            classSubjectNum=classA.copy()
        else:
            classSubjectNum = classB.copy()
        currentClassTime=allClassTime.copy()
        teacherList=classTeacher[i]
        # print(currentClassTime)
        # print(teacherList)
        # 遍历每个班所有老师
        for teacherIndex in range(len(teacherList)):
            teacherName=teacherList[teacherIndex]
            print("开始遍历老师："+teacherName)
            subjectName=subject[teacherIndex]
            currentTeacherTime=teacherTime[teacherName]
            # 求老师时间和班级时间交集
            commonTime=list(set(currentClassTime).intersection(set(currentTeacherTime)))
            if len(commonTime)==0 or len(commonTime)<classSubjectNum[teacherIndex]:
                print(teacherName+"老师的空余时间为："+str(currentTeacherTime))
                print("班级和老师共同时间为"+str(commonTime))
                print("需要上课节数："+str(classSubjectNum[teacherIndex]))
                return False
            # 生成随机指数
            try:
                indexList=random.sample(range(0,len(commonTime)),classSubjectNum[teacherIndex])
            except:
                print(commonTime)
                print(classSubjectNum[teacherIndex])
            # print(currentClassTime)
            # print(currentTeacherTime)
            # print(commonTime)
            # print(indexList)
            # 遍历出该老师所有课次
            for timeindex in indexList:
                # 指定的哪节课
                try:
                    teacherClass=commonTime[timeindex]
                except:
                    print("需要上课节数：" + str(classSubjectNum[teacherIndex]))
                    print("随机选课指数为："+str(indexList))
                    print("班级和老师共同时间为"+str(commonTime))
                    return False
                # print("-----"+str(teacherClass))
                # 班级时间记录
                if i in classSubjectPlan.keys():
                    # 更新学科排班表
                    oldsubjectList={}
                    oldsubjectList=classSubjectPlan[i]
                    # print("++++"+str(i))
                    # print(classSubjectPlan)
                    # print(classSubjectPlan[i])
                    singleSubjectList={teacherClass:subjectName}
                    # print(singleSubjectList)
                    oldsubjectList.update(singleSubjectList)
                    # print(oldsubjectList)
                    classSubjectPlan[i]=oldsubjectList
                    # 更新教师排班表
                    oldTeacherList=classTeacherPlan[i]
                    singleTeacherList={teacherClass:teacherName}
                    oldTeacherList.update(singleTeacherList)
                    classTeacherPlan[i]=oldTeacherList
                else:
                    singleSubjectList = {teacherClass: subjectName}
                    classSubjectPlan[i]=singleSubjectList
                    singleTeacherList = {teacherClass: teacherName}
                    classTeacherPlan[i] =singleTeacherList
                # 从当前班级课表空闲时间中删除这节课
                currentClassTime.remove(teacherClass)
                # 当前这个教师空余时间删除这节课
                # print(teacherTime[teacherName])
                currentTeacherTime.remove(teacherClass)
                print(teacherTime[teacherName])
                print(infom.teacherinfo[teacherName])


    print(classTeacherPlan)
    print(classSubjectPlan)
    return True

if __name__ == '__main__':

    # print(information.masterTeacher)
    # for i in information.classList:
    #     print(i)
    # print(information.classList)
    # print(information.classTeacher)
    # print(len(information.classTeacher))
    # print(information.teacherinfo["徐盛轶"])
    # time.sleep(10)
    # print(scheduleSys(info))
    # info= information()

    # print(information.teacherinfo["徐盛轶"])
    # time.sleep(1)
    # # print(allclass)
    # print(scheduleSys(info))
    whileindex=False
    while(not whileindex):
        info = information()
        whileindex=scheduleSys(info)
        print(whileindex)
