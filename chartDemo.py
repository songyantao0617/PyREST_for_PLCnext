import matplotlib.pyplot as plt
import com.Phoenixcontact.REST as PLCnREST

'''
This Demo shows PLC's TICK_COUNT
Before run , creat an empty EHMI on PLCnext
make sure 'matplotlib' has been installed
'''


def chartDemo(ip, passwd):
    # creat client
    client = PLCnREST.NewClient(ip)
    client.PLCnPasswd = passwd  # default username = admin
    client.connect()
    plt.title('PLCnext  TICK_COUNT')
    plt.axis([0, 100, 0, 1000])
    plt.ion()
    xs = [0, 0]
    ys = [0, 0]
    for i in range(100):
        xs[0] = xs[1]
        ys[0] = ys[1]
        xs[1] = i
        ys[1] = int(client.readDatas_list(['ESM_DATA.ESM_INFOS[1].TICK_COUNT'])) % 1000  # read count value
        plt.plot(xs, ys)
        plt.pause(0.01)


if __name__ == "__main__":
    # set PLCnext's IP and Password here
    chartDemo('192.168.124.10', '42bad0fd')
