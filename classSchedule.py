import configparser as ConfigParser
import copy
import time

import pandas as pd
import numpy as np
import random
import xlrd
import xlwt

allClassList=['语文', '数 学', '英语', '政 治', '生 物', '历 史' ,'地 理' ,'体 育', '音 乐', '美 术', '健 康' ,'信 息' ,'综合实践']
# commonClass=[23,24]
#每个学科的教研时间
classReserve={'语文':13,'数 学':29, '英语':13, '政 治':9, '生 物':25, '历 史':9, '地 理':9, '体 育':9, '音 乐':25, '美 术':25, '健 康':9, '信 息':25, '综合实践':25}
# 1-4classA，5-18classB
# classA={'语文':6,'数 学':6, '英语':5, '政 治':2, '生 物':2, '历 史':3, '地 理':2, '体 育':3, '音 乐':1, '美 术':1, '健 康':1, '信 息':1, '综合实践':1}
# classB={'语文':11,'数 学':5, '英语':5, '政 治':2, '生 物':2, '历 史':3, '地 理':2, '体 育':2, '音 乐':1, '美 术':1, '健 康':1, '信 息':1, '综合实践':1}
# 班主任对应的学科指数,从0开始计数
masterSubject=[5,0,2,0,0,0,2,1,1,3,0,2,0,2,2,0,1,0]
masterteacherSubject=['历 史','语文','英语','语文','语文','语文', '英语','数 学','数 学','政 治','语文','英语','语文','英语','英语','语文', '语文','数 学' ]
# 课程设置
classA=[6,6,5,2,2,3,2,3,1,1,1,1,1]
classB=[11,5,5,2,2,3,2,2,1,1,1,1,1]
# classDayA=[[1,1,1,1,2],[1,1,1,1,2],[1,1,1,1,1],[1,1,0,0,0],[1,1,0,0,0],[1,1,1,0,0],[1,1,0,0,0],[1,1,1,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]]
# classDayB=[[3,2,2,2,2],[1,1,1,1,1],[1,1,1,1,1],[1,1,0,0,0],[1,1,0,0,0],[1,1,1,0,0],[1,1,0,0,0],[1,1,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]]
# 班级可用时间,去除第一节，八节班会，24、25节课社团
allClassTime=np.delete(np.arange(1,41),[0,7,22,23]).tolist()
# 教师可用时间,去除第一节
allclass=np.arange(2,41).tolist()
#数语外老师特殊时间,去除第一节
specialTime=[2,3,9,10,11,17,18,19,25,26,27,33,34,35]
# 按照excel表中表头顺序，具体见上面。数字越大，权重越大
classWeight={'语文':8,'数 学':8, '英语':8, '政 治':2, '生 物':2, '历 史':2, '地 理':2, '体 育':1, '音 乐':1, '美 术':1, '健 康':1, '信 息':1, '综合实践':1}
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
            # if i=="语文"or i=="数学" or i=="英语":
            #     allteacher=specialTime.copy()

            try:
                allteacher.remove(classReserve[i])
            except :
                print(i+"老师的时间不包含"+str(classReserve[i]))

            teacherTime=allteacher.copy()
            # print(teacherTime)
            classNumIndex=classNumIndex+1
            list=teacherExcel.loc[:,i].values
            for name in list:
                sigalteacher={name:teacherTime.copy()}
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

def numToDay(numList):
	dayList={}
	for i in numList:
		i=i-1
		if i//8 in dayList.keys():
			dayList[i//8].append(i%8)
		else:
			dayList.update({i//8:[i%8]})
	return dayList

def classTakeOutMaster(classNum):
    # 班级号是从1开始的
    if classNum<=4:
        classSubjectNum = classA.copy()
        classSubjectNum[masterSubject[classNum-1]]=classSubjectNum[masterSubject[classNum-1]]-1
        return classSubjectNum
    else:
        classSubjectNum = classB.copy()
        classSubjectNum[masterSubject[classNum-1]] = classSubjectNum[masterSubject[classNum-1]] - 1
        return classSubjectNum
def numToList(numList):
	lastSubjectList=[]
	for num in numList:
		a=[num//5]*(5-num%5)
		b=[num//5+1]*(num%5)
		c=a+b
		lastSubjectList.append(c)
	return lastSubjectList

def scheduleSys(infom):
    # 1-18班班级列表
    classList = infom.classList

    # 学科顺序表，['语文', '数 学', '英语', '政 治', '生 物', '历 史' ,'地 理' ,'体 育', '音 乐', '美 术', '健 康' ,'信 息' ,'综合实践']
    subject=info.subject

    #每个老师空余时间表
    teacherTime={}
    teacherTime = infom.teacherinfo.copy()


    # 所有班级空余时间表
    classRemainTime={}

    # 每班对应老师名单
    classTeacher=infom.classTeacher.copy()

    # 每班老师排版表，输出
    classTeacherPlan={}

    # 每班学科排班表，输出
    classSubjectPlan={}

    # 循环遍历每个班语数外
    spicalErrorIndex=0
    spicalClassNum=1
    while spicalClassNum<=len(classList):
        # spicalErrorIndex = 0
        # print("开始遍历班级(语数外)："+str(spicalClassNum))
        classSubjectNum=classTakeOutMaster(spicalClassNum)
        classSubjectDayNum=numToList(classSubjectNum)
        # if i<=4:
        #     classSubjectNum=classA.copy()
        #     classSubjectDayNum=classDayA.copy()
        # else:
        #     classSubjectNum = classB.copy()
        #     classSubjectDayNum = classDayB.copy()
        # if spicalErrorIndex==0:
        #     currentClassTime=specialTime.copy()
        # else:
        currentClassTime=allClassTime.copy()
        teacherList=classTeacher[spicalClassNum]
        # print(currentClassTime)
        # print(teacherList)
        weekDayIndex=[0,0,1,1,2,2]
        random.shuffle(weekDayIndex)
        # 遍历每个班数语外老师
        for teacherIndex in [0,1,2]:
            teacherName=teacherList[teacherIndex]
            # print("开始遍历老师："+teacherName)
            subjectName=subject[teacherIndex]
            currentTeacherTime=teacherTime[teacherName]
            # 求老师时间和班级时间交集
            commonTime=list(set(currentClassTime).intersection(set(currentTeacherTime)))
            if len(commonTime)==0 or len(commonTime)<classSubjectNum[teacherIndex]:
                print(teacherName+"老师的空余时间为："+str(currentTeacherTime))
                print("班级和老师共同时间为"+str(commonTime))
                print("需要上课节数："+str(classSubjectNum[teacherIndex]))
                print(classTeacherPlan)
                print(classSubjectPlan)
                return False
            # 生成随机指数
            teacherClassList=[]
            # try:
            mydayList=numToDay(commonTime)
            dayClassNum=classSubjectDayNum[teacherIndex].copy()
            random.shuffle(dayClassNum)
            for classDayIndex in range(0,5):
                singleDayIndex=random.sample(range(0,len(mydayList[classDayIndex])),dayClassNum[classDayIndex])
                for n in singleDayIndex:
                    teacherClassList.append(mydayList[classDayIndex][n]+1+classDayIndex*8)

                minNum=min(mydayList[classDayIndex])+1+classDayIndex*8
                if (minNum not in teacherClassList)and(len(teacherClassList)>0)and(weekDayIndex[classDayIndex]==teacherIndex):
                    teacherClassList[teacherClassList.index(max(teacherClassList))]=minNum
                    # print(min(mydayList[classDayIndex]))
                    # print(teacherClassList)
            # print(teacherClassList)
            # time.sleep(1000)
            # indexList=random.sample(range(0,len(commonTime)),classSubjectNum[teacherIndex])
            # print(teacherClassList)
            # except:
            #     print("时间不对")
                # spicalErrorIndex+=1
                # continue
            # 遍历出该老师所有课次
            for teacherClass in teacherClassList:

                # 班级时间记录
                if spicalClassNum in classSubjectPlan.keys():
                    # 更新学科排班表
                    oldsubjectList={}
                    oldsubjectList=classSubjectPlan[spicalClassNum]
                    # print("++++"+str(i))
                    # print(classSubjectPlan)
                    # print(classSubjectPlan[i])
                    singleSubjectList={teacherClass:subjectName}
                    # print(singleSubjectList)
                    oldsubjectList.update(singleSubjectList)
                    # print(oldsubjectList)
                    classSubjectPlan[spicalClassNum]=oldsubjectList
                    # 更新教师排班表
                    oldTeacherList=classTeacherPlan[spicalClassNum]
                    singleTeacherList={teacherClass:teacherName}
                    oldTeacherList.update(singleTeacherList)
                    classTeacherPlan[spicalClassNum]=oldTeacherList
                else:
                    singleSubjectList = {teacherClass: subjectName}
                    classSubjectPlan[spicalClassNum]=singleSubjectList
                    singleTeacherList = {teacherClass: teacherName}
                    classTeacherPlan[spicalClassNum] =singleTeacherList
                # 从当前班级课表空闲时间中删除这节课
                currentClassTime.remove(teacherClass)
                # 当前这个教师空余时间删除这节课
                # print(teacherTime[teacherName])
                currentTeacherTime.remove(teacherClass)
                # print(teacherTime[teacherName])
                # print(infom.teacherinfo[teacherName])
        classRemainTime.update({spicalClassNum:currentClassTime})
        spicalClassNum+=1
    # print(classTeacherPlan)
    # print(classSubjectPlan)
    # 遍历每个班语数外以外其他课程
    i=1
    while(i<=len(classList)):
        # print("开始遍历班级（其他）："+str(i))
        classSubjectNum = classTakeOutMaster(i)
        # if i<=4:
        #     classSubjectNum=classA.copy()
        #
        # else:
        #     classSubjectNum = classB.copy()

        currentClassTime=classRemainTime[i].copy()
        teacherList=classTeacher[i]
        # 遍历每个其他老师,[3,4,5,6,7,8,9,10,11,12]

        teacherIndex=3
        while(teacherIndex<=12):
            # for teacherIndex in [3]:
            teacherName = teacherList[teacherIndex]

            subjectName = subject[teacherIndex]
            # print(subjectName)
            currentTeacherTime = teacherTime[teacherName]

            # print("开始遍历老师：" + teacherName+str(i)+ ",空闲时间："+str(currentTeacherTime))
            # 求老师时间和班级时间交集
            commonTime = list(set(currentClassTime).intersection(set(currentTeacherTime)))
            # if len(commonTime) == 0 or len(commonTime) < classSubjectNum[teacherIndex]:
            #     print(teacherName + "老师的空余时间为：" + str(currentTeacherTime))
            #     print("班级和老师共同时间为" + str(commonTime))
            #     print("需要上课节数：" + str(classSubjectNum[teacherIndex]))
            #     print(classTeacherPlan)
            #     print(classSubjectPlan)
            #     return False
            # 生成随机指数
            # try:

            teacherClassList = []
            mydayList = numToDay(commonTime)
            dayClassNum = classSubjectNum[teacherIndex]
            dayNum=list(mydayList.keys())
            random.shuffle(dayNum)
            if len(dayNum)<dayClassNum:
                # print("匹配空闲天数："+str(len(dayNum))+",课程需要天数："+str(dayClassNum))
                if len(commonTime)<dayClassNum:
                    # print("遍历班级（其他）：" + str(i)+"，学科："+subjectName+",老师："+teacherName)
                    # print("当前班级课程剩余时间："+str(currentClassTime))
                    # print("当前班级课程时间："+str(len(classSubjectPlan[i]))+str(classSubjectPlan[i]))
                    # print("匹配空闲课数：" + str(len(commonTime)) + ",课程需要节数：" + str(dayClassNum))
                    return False
                indexList=random.sample(range(0,len(commonTime)),dayClassNum)
                for chooseIndex in indexList:
                    teacherClassList.append(commonTime[chooseIndex])
            else:
                for chooseIndex in range(0,dayClassNum):
                    classDayIndex=dayNum[chooseIndex]
                    singleDayIndex = random.randint(0, len(mydayList[classDayIndex])-1)
                    # print("classDayIndex"+str(classDayIndex))
                    # print("singleDayIndex"+str(singleDayIndex))
                    # print("mydayList"+str(mydayList))
                    # print("mydayList[classDayIndex][singleDayIndex]"+str(mydayList[classDayIndex][singleDayIndex]))
                    teacherClassList.append(mydayList[classDayIndex][singleDayIndex] + 1 + classDayIndex * 8)
            # indexList=random.sample(range(0,len(commonTime)),classSubjectNum[teacherIndex])
            # print("++++"+str(teacherClassList))
            # except Exception as e:
            #     print(e)
            #     print(commonTime)
            #     print(classSubjectNum[teacherIndex])
            # print(currentClassTime)
            # print(currentTeacherTime)
            # print(commonTime)
            # print(indexList)
            # 遍历出该老师所有课次
            for teacherClass in teacherClassList:
                # 班级时间记录
                if i in classSubjectPlan.keys():
                    # 更新学科排班表
                    oldsubjectList = {}
                    oldsubjectList = classSubjectPlan[i]
                    # print("++++"+str(i))
                    # print(classSubjectPlan)
                    # print(classSubjectPlan[i])
                    singleSubjectList = {teacherClass: subjectName}
                    # print(singleSubjectList)
                    oldsubjectList.update(singleSubjectList)
                    # print(oldsubjectList)
                    classSubjectPlan[i] = oldsubjectList
                    # 更新教师排班表
                    oldTeacherList = classTeacherPlan[i]
                    singleTeacherList = {teacherClass: teacherName}
                    oldTeacherList.update(singleTeacherList)
                    classTeacherPlan[i] = oldTeacherList
                else:
                    singleSubjectList = {teacherClass: subjectName}
                    classSubjectPlan[i] = singleSubjectList
                    singleTeacherList = {teacherClass: teacherName}
                    classTeacherPlan[i] = singleTeacherList
                # 从当前班级课表空闲时间中删除这节课
                currentClassTime.remove(teacherClass)
                # 当前这个教师空余时间删除这节课
                # print(teacherTime[teacherName])
                currentTeacherTime.remove(teacherClass)
                # print(teacherTime[teacherName])
                # print(infom.teacherinfo[teacherName])
            teacherIndex=teacherIndex+1
        i=i+1
    # print(classTeacherPlan)
    # print(classSubjectPlan)
    value=[classSubjectPlan,classTeacherPlan]
    lastclassSubjectPlan=classSubjectPlan.copy()
    lastclassTeacherPlan=classTeacherPlan
    return value

# 计算所有课程课课程时间权重
def checkWight(classPlan):
    best=0
    for classNum in classPlan.keys():
        for courseNum in classPlan[classNum].keys():
            best=best+((courseNum-1)%8+1)*classWeight[classPlan[classNum][courseNum]]
    return best

#计算每个老师4,5节课的次数，方差要最小
def averageFourAndFive(teacherPlan,teacheCourseNum):
    teacherVari=0
    for classNum in teacherPlan.keys():
        for courseNum in teacherPlan[classNum].keys():
            if (courseNum%8==4 or courseNum%8==5):
                teacherName=teacherPlan[classNum][courseNum]
                teacheCourseNum[teacherName]+=1
    FourAndFiveList=list(teacheCourseNum.values())
    teacherVari=np.var(FourAndFiveList)
    # print(teacherVari)
    return  teacherVari

def allTeacherList(teacherPlan,teacheCourseList):
    for classNum in teacherPlan:
        for courseNum in teacherPlan[classNum]:

            teacherName = teacherPlan[classNum][courseNum]
            # 周一第二节课[2,1，班级]
            argList=[(courseNum-1)%8+1,(courseNum-1)//8+1,classNum]
            if teacheCourseList[teacherName]==0:
                teacheCourseList[teacherName]=[]
                teacheCourseList[teacherName].append(argList)
            else:
                teacheCourseList[teacherName].append(argList)
    return teacheCourseList

def excelWrite(classList,excelTeacher,masterTeacherList,iteatorNum,classBestIndex):
    book = xlwt.Workbook()
    titleRow = ["星期一", "星期二", "星期三", "星期四", "星期五"]
    titleCol = ["第1节", "第2节", "第3节", "第4节", "第5节", "第6节", "第7节", "第8节"]
    sheetName=["班级课程表","班级教师表"]
    sheetindex=0
    for classdict in classList:
        sheet = book.add_sheet(sheetName[sheetindex])
        for classNum in classdict:
            rowIdex=int(((classNum-1)//3)*11)
            colIndex=int(((classNum-1)%3)*7)
            sheet.write(rowIdex+8,colIndex+1,"班会")
            sheet.write(rowIdex + 8, colIndex + 3, "社团")
            sheet.write(rowIdex + 7, colIndex + 3, "社团")
            if sheetindex==0:
                sheet.write(rowIdex+1,colIndex+1,masterteacherSubject[classNum - 1])
            else:
                sheet.write(rowIdex+1, colIndex+1,masterTeacherList[classNum-1])
            sheet.write(rowIdex,colIndex,str(classNum)+"班")
            row=rowIdex
            while(row<=7+rowIdex):
                sheet.write(row+1,colIndex,titleCol[row-rowIdex])
                row=row+1
            col=colIndex
            while(col<=4+colIndex):
                sheet.write(rowIdex,col+1,titleRow[col-colIndex])
                col=col+1
            for timeNum in classdict[classNum]:
                sheet.write((timeNum-1)%8+1+rowIdex,(timeNum-1)//8+1+colIndex,classdict[classNum][timeNum])
        sheetindex += 1
    sheet = book.add_sheet("教师上课班级表")
    teacherIndex=1
    for teacherName in excelTeacher:
        rowIdex = int(((teacherIndex - 1) // 3) * 11)
        colIndex = int(((teacherIndex - 1) % 3) * 7)
        sheet.write(rowIdex, colIndex,teacherName)
        row = rowIdex
        while (row <= 7 + rowIdex):
            sheet.write(row + 1, colIndex, titleCol[row - rowIdex])
            row = row + 1
        col = colIndex
        while (col <= 4 + colIndex):
            sheet.write(rowIdex, col + 1, titleRow[col - colIndex])
            col = col + 1
        for x in excelTeacher[teacherName]:
            try:
                sheet.write(int(x[0]+rowIdex),int(x[1]+colIndex),int(x[2]))
            except Exception as e:
                print(e)
                print(teacherName)
                print(x)
                # time.sleep(10000)
                break
        if teacherName in masterTeacherList:
            sheet.write(rowIdex + 1, colIndex + 1,masterTeacherList.index(teacherName)+1)
        teacherIndex+=1
    book.save('C:/Users/sky/Desktop/课表/乌鲁木齐市58中2019-2020学年第一学期课表('+str(iteatorNum)+"_"+str(int(classBestIndex))+').xls')

if __name__ == '__main__':
    # 初始化老师名单课表，keys为老师姓名，teacheCourseNum值为0，teacheCourseList值为[]
    info = information()
    # teacheCourseNum={}.fromkeys(list(info.teacherinfo.keys()), 0)
    teacheCourseList = {}.fromkeys(list(info.teacherinfo.keys()), 0)
    masterTeacherList=list(info.masterTeacher)
    # print(masterTeacherList)
    # time.sleep(10000)
    # 课程排课指标，越小越好
    classBestIndex=float("inf")
    classBestplan=[]
    # 迭代次数
    iteatorNum=1000
    iteatorIndex=0
    while(iteatorIndex<iteatorNum):
        teacheCourseNum = {}.fromkeys(list(info.teacherinfo.keys()), 0)
        whileindex=False
        while(not whileindex):
            info = information()
            whileindex=scheduleSys(info)
        numWeight=checkWight(whileindex[0])
        numVari=averageFourAndFive(whileindex[1],teacheCourseNum)
        # 课程权重：中午课程=6:1（权重130000多点，var2左右），修改课程权重后，最好修改下两者比例
        # print("numWeigrt"+str(numWeight))
        # print("numVari"+str(numVari))
        classBestNum=numWeight+numVari*1000
        if classBestNum<classBestIndex:
            classBestIndex=classBestNum
            classBestplan=copy.deepcopy(whileindex)
        print("+++++++++++++++++++++++++++++迭代了" + str(iteatorIndex + 1) + "次。指标数："+str(classBestIndex)+"。最新指标数："+str(classBestNum))
        iteatorIndex=iteatorIndex+1
    print(classBestIndex)
    print(classBestplan)
    excelTeacherList=allTeacherList(classBestplan[1],teacheCourseList)
    print(excelTeacherList)
    excelWrite(classBestplan,excelTeacherList,masterTeacherList,iteatorNum,classBestIndex)
