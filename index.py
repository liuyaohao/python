from tkinter import *
from tkinter.messagebox import *
import socket
udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
import random
window = Tk()
window.geometry("350x500")
window.title("极域控制")
localhost = socket.gethostbyname(socket.gethostname())
iplist = localhost.split('.')
res = ""  #获取本身的ip地址，以十六进制
for i in iplist:
    res = res + "{:02x}".format(int(i))  

def getRandomString():
    stringRes = ""
    for i in range(17-1):
        temp = random.randint(0,255)
        stringRes = stringRes + "{:02x}".format(temp)
    return stringRes + '20'

def sendData(type,ip,other):
    if ip == '':
        showinfo('警告','ip地址不能为空!')
        return 1
    else:
        addr = (ip,4705)
        wol = (ip,9)
        data = ""
        hexAddr =  "{:02x}".format(int(ip.split('.')[0])) +  "{:02x}".format(int(ip.split('.')[1]))+"{:02x}".format(int(ip.split('.')[2]))+"{:02x}".format(int(ip.split('.')[3]))
        match type:
            case 'start':
                data ="ffffffffffff" + (''.join(other[0:].split('-'))*16)
                udp.sendto(bytes.fromhex(data),wol)
                return 1
            case 'shutdown':
                data = "444d4f43000001002a0200005c0d179e4e8d594383b6735b98b80c25204e0000" + res + "1d0200001d0200000002000000000000140000000f00000001000000000000005965085e065c7351ed95a8608476a18b977b3a670230000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            case 'setPW':
                if len(other) <1 or len(other) > 10:
                    showinfo('警告','设置的密码长度不能低于1且不能大于10')
                    return 0
                else:
                    data = "444d4f430000010095000000" + getRandomString() +"4e0000"+res +"88000000880000000040000000000000060000007b00000000000000010000000a000000000000000000000000000000500000005000000001000000"
                    for t in other:
                        data += "{:02x}".format(ord(t))+'00'
                    data = data.ljust(354,'0')
            case 'close':
                data = "444d4f43000001002a020000"+ getRandomString() + "4e0000" + res+"1d0200001d0200000002000000000000020000100f00000001000000000000005965085e065c7351ed95a8608476945e28750b7a8f5e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            case 'msg':
                data = "444d4f43000001009e030000"+ getRandomString() + "4e0000" + res + "9103000091030000000800000000000005000000"
                for t in other:
                    data+="{:04x}".format(ord(t))[-2:]
                    data+="{:04x}".format(ord(t))[:2]
                data = data.ljust(1908,'0')
            case 'open':
                if len(other) <1 and len(other)>100:
                    showinfo('警告','输入地址不能为空且长度不能超过100')
                    return 0
                data = "444d4f43000001006e030000"+getRandomString()+"4e0000"+res+"610300006103000000020000000000000f00000001000000"
                if " " in other:
                    for t in other.split(" ",1)[0]:
                        data+="{:04x}".format(ord(t))[-2:]
                        data+="{:04x}".format(ord(t))[:2]
                    data = data.ljust(1144,'0')
                    data+="{:04x}".format(ord(" "))[-2:]
                    data+="{:04x}".format(ord(" "))[:2]
                    for t in other.split(" ",1)[1]:
                        data+="{:04x}".format(ord(t))[-2:]
                        data+="{:04x}".format(ord(t))[:2]
                    data=data.ljust(1812,'0')
                else:
                    for t in other:
                        data+="{:04x}".format(ord(t))[-2:]
                        data+="{:04x}".format(ord(t))[:2]
                    data = data.ljust(1812,'0')
            case 'url':
                data = "444d4f4300000100"+"{:02x}".format(36+len(other*2))+"000000"+getRandomString()+"4e0000"+res+"{:02x}".format(23+len(other*2))+"000000"+"{:02x}".format(23+len(other*2))+"00000000020000000000001800000000000000"
                for t in other:
                    data+="{:04x}".format(ord(t))[-2:]
                    data+="{:04x}".format(ord(t))[:2]
                data +="00000000"
            case 'wallpaper':
                one = ''
            case 'black':
                data = "4d4553530100000001000000"+hexAddr+"27000000200000000000008001000000010000000a00000000000000ffffff0000000000a00520"
                udp.sendto(bytes.fromhex(data),(ip,5512))
                return 1
        udp.sendto(bytes.fromhex(data),addr)
        showinfo("提示","已完成操作!")
        
def createWindow(title,label,type,ip):
    if ip == '':
        showinfo('警告','ip地址不能为空!')
        return 1
    else:
        startWindow = Toplevel(window,)
        startWindow.geometry("300x300")
        startWindow.grab_set()
        startWindow.title(title)
        Label(startWindow,text=label).pack()
        input = Entry(startWindow,width=30)
        input.pack()
        Button(startWindow,text="确定",width=18,command=lambda:sendData(type,ip,input.get())).pack()

                 
                

Label(window,text="请输入目标的ip地址:",width=50).pack()
ipaddr = Entry(window,width=30)
ipaddr.pack()
Button(window,text="开机",command=lambda:createWindow("开机","请输入mac地址 格式:fa-4d-89-ce-fd-64","start",ipaddr.get()),width=10,height=2).place(relx=0.06,rely=0.1)  #启动计算机 需要mac地址
Button(window,text="关机",command=lambda:sendData('shutdown',ipaddr.get(),'other'),width=10,height=2).place(relx=0.38,rely=0.1)  #关闭计算机
Button(window,text="修改管理密码",command=lambda:createWindow("修改管理密码","请输入新设置的密码","setPW",ipaddr.get()),width=10,height=2).place(relx=0.68,rely=0.1)  #修改管理密码
Button(window,text="关闭所有程序",command=lambda:sendData('close',ipaddr.get(),'other'),width=10,height=2).place(relx=0.06,rely=0.2) #关闭所有程序
Button(window,text="发送消息",command=lambda:createWindow("发送消息","请输入需要发送的消息","msg",ipaddr.get()),width=10,height=2).place(relx=0.38,rely=0.2) #发送消息
Button(window,text="远程打开文件",command=lambda:createWindow("远程打开文件","文件地址(目标电脑路径)","open",ipaddr.get()),width=10,height=2).place(relx=0.68,rely=0.2) #远程打开文件
Button(window,text="远程打开网页",command=lambda:createWindow("远程打开网页","url地址(网址地址例http://www.baidu.com)","url",ipaddr.get()),width=10,height=2).place(relx=0.06,rely=0.3) #远程打开网页
# Button(window,text="远程设置壁纸",command=lambda:createWindow("远程设置壁纸","图片地址(目标电脑图片路径)","wallpaper",ipaddr.get()),width=10,height=2).place(relx=0.38,rely=0.3) #远程设置壁纸
Button(window,text="黑屏安静",command=lambda:sendData('black',ipaddr.get(),'other'),width=10,height=2).place(relx=0.68,rely=0.3) #黑屏安静
window.resizable(0,0)
window.mainloop()