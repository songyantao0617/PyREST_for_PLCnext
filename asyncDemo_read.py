import time
import com.Phoenixcontact.REST as PLCnREST

'''
This is a async read demo
using this method the communicating is fast than sync
'''


def asyncDemo(ip, passwd):
    # creat client
    client = PLCnREST.NewClient(ip)
    client.PLCnPasswd = passwd  # default username = admin
    client.connect()
    # use asyncFunction ,'ESM_DATA.ESM_INFOS[1].TICK_COUNT' must in the group
    asyncGroup = client.registerReadGroups(['ESM_DATA.ESM_INFOS[1].TICK_COUNT', 'A'])

    asyncGroup.asyncStart()

    lastStamp = time.time()
    lastValue = 0
    exit = 0

    while exit < 100:

        # use asyncMode, Just read values (non-block)
        result = asyncGroup.results_dict

        itc = int(result.get('ESM_DATA.ESM_INFOS[1].TICK_COUNT', 0))
        if itc != lastValue:
            currentStamp = time.time()

            # the time will show the speed of communication
            print(
                'tickCount:' + str(itc) + '----A:' + str(result.get('A', 0)) + '-----' + str(currentStamp - lastStamp))

            lastStamp = currentStamp
            lastValue = itc
            exit += 1

    asyncGroup.asyncStop()


if __name__ == "__main__":
    # set PLCnext's IP and Password here
    asyncDemo('192.168.124.10', '42bad0fd')
    exit()
