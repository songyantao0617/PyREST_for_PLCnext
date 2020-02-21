import logging
import os
import random
import com.Phoenixcontact.REST as PLCnREST
import com.Phoenixcontact.utils as PLCnUtils
from com.Phoenixcontact.REST.RESTException import RESTException
'''
--PhoenixContect-China
--STE : SongYantao@Phoenixcontact.com.cn

Version :   V0.2

Notice : 

    require package :requests

    Variables on PLC should have HMI_tag
    EHMI is required ,just create an empty page
    
    set the following vars in PLC
    
     |---global    
        |-A (DWORD)
        |-B (TIME)
        |-C (BOOL)
        |
        |---MainInstance
           |-Value1 (INT)
           |-Value2 (REAL)
           |-Value3 (STRING)
'''

def Demo():


    # 创建客户端
    # Create a client attach to PLCnext
    client = PLCnREST.NewClient('192.168.124.10')
    client.PLCnUserName = 'admin'
    client.PLCnPasswd = '42bad0fd'
    client.connect()

    # 创建读取组(方便管理)
    # Creat some Group for read function
    GlobalGroup = client.registerReadGroups(['A', 'B', 'C'])  # 全局变量组 An example group with some global variables
    MainInstanceGroup = client.registerReadGroups(
        ['MainInstance.Value1', 'MainInstance.Value2',
         'MainInstance.Value3'])  # 任务实例组 An example group with some variables in MainInstance

    # if the variable doesn't exist (or doesn't have HMI_Tag) ,the  RESTException will be throwed
    print('异常处理实验')
    print('If there is no variable called \'AAA\',you will see the following message')
    try:
        errorGroup = client.registerReadGroups(['AAA'])
    except RESTException as E:
        print('\t{}'.format(E.message))


    def WriteData():
        # 写变量
        # Write data to plc
        tmp1 = random.randint(0, 3000)
        tmp2 = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 10))
        tmp3 = True if tmp1 < 1500 else False
        # Send data
        client.writeDatas({'A': tmp1, 'C': tmp3, 'MainInstance.Value3': str(tmp2)})

    # 获取组内成员数据类型：
    print("Here we can get the variables' type of group")
    print("组成内成员数据类型：")
    print('\t{}'.format(GlobalGroup.checkMemberType()))
    print('\t{}'.format(MainInstanceGroup.checkMemberType()))
    print('*' * 100)

    # 输出组内所有成员值：
    # Here we get all values of group
    print('get all values of group:')
    print('输出组内所有成员值:')
    for i in range(2):
        WriteData()
        print('\t' + str(GlobalGroup.results))
        print('\t' + str(MainInstanceGroup.results))
        print('\t------')
    print('*' * 100)


    # 从组内提取单个变量值：
    #Or we just want only one variable's value of group
    #But Notice it will handle requests everytime we call,this is just an additional function in some situation
    print("Get values by \"group['member']\" ")
    print('直接从组内提出某一变量值')
    print('\tA : {}\tB : {}\tC:{}'.format(GlobalGroup['A'], GlobalGroup['B'], GlobalGroup['C']))
    print('\tValue1 : {}\tValue2 : {}\tValue3 : {}'.format(MainInstanceGroup['MainInstance.Value1'],
                                                           MainInstanceGroup['MainInstance.Value2'],
                                                           MainInstanceGroup['MainInstance.Value3']))
    print('\t------')
    for i in range(2):
        WriteData()
        print('\tA : {}\tC : {}\tvalue3:{}'.format(GlobalGroup['A'], GlobalGroup['C'],MainInstanceGroup['MainInstance.Value3']))
        print('\t------')
    print('*' * 100)

    # 独立方法读取随机若干变量
    # Also we can read variables without group
    # 'readDatas_dict' function's return type is dict
    WriteData()
    print('使用readDatas_dict方法：')
    print('Get variables without group by readDatas_dict ')
    Res = client.readDatas_dict(['A', 'C', 'F', 'MainInstance.Value3'])
    print('\t--{}--{}--{}--{}--'.format(Res['A'], Res['C'], Res['F'], Res['MainInstance.Value3']))

    WriteData()
    # 'readDatas_list' function's return type is list
    print('使用readDatas_list方法：')
    print('Get variables without group by readDatas_list ')
    varA, varC, varF, var3 = client.readDatas_list(['A', 'C', 'F', 'MainInstance.Value3'])
    print('\t--{}--{}--{}--{}--'.format(varA, varC, varF, var3))
    print('*' * 100)

    # 显示客户端的所有组信息
    #show the group information belongs to client
    print('show the group information belongs to client:')
    print('显示客户端的所有组信息')
    print('\t{}'.format(client.reportGroups()))
    print('*' * 100)

    print('-----Enjoy !\t------')


if __name__ == '__main__':
    # setting log function
    _localpath = os.path.split(os.path.abspath(__file__))[0]
    _logpath = os.path.join(_localpath, 'log/')
    log = PLCnUtils.Logger.Log()
    log.setLogConfig(level=logging.INFO, logPath=_logpath, logFilename='Outputs.log')

    # start Demo
    Demo()
