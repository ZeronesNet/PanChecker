import requests
import re

def connect_Check():
    '''检查是否能联通各个网盘'''

    print("进行网盘连通性检查")
    
    url_List = [
        "https://pan.quark.cn",
        "https://pan.baidu.com",
        "https://www.alipan.com",
        "https://pan.xunlei.com"
        ]

    for url in url_List:
        
        connect_Request = requests.get(url)
        status_Code = connect_Request.status_code

        if status_Code == 200:
            print(url + "\t\t\t" + "[\033[32m OK \033[0m]")
        else:
            print(url + "\t\t\t" + "[\033[31m NO \033[0m]")
        connect_Request.close()
    print("\n")

    

def quark_Check(Url):
    '''夸克网盘的检查方法'''

    header_quark = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "Referer":"https://pan.quark.cn",
        "Content-type":"application/json"
            }  # 构建夸克请求方法的header
    
    quark_pwd_id = re.search(r"/s/(.*)#",Url) # 保存从Url中提取出夸克要求的pwd_id字段
    quark_Pwd = ""  # 保存从Url中提取出夸克要求的pwd字段

    # 向state_Request_url发送POST请求并获取返回的状态代码
    status_Request_url = "https://drive-h.quark.cn/1/clouddrive/share/sharepage/token?pr=ucpro&fr=pc"
    status_Code_request = requests.post(status_Request_url,json={"pwd_id": quark_pwd_id.group(0)[3:-1],"passcode": quark_Pwd},headers=header_quark)
    status_Code = status_Code_request.status_code

    if status_Code == 200:
        print(Url + "\t\t\t" + "[\033[32m OK \033[0m]")
    else:
        print(Url + "\t\t\t" + "[\033[31m NO \033[0m]")

    status_Code_request.close()

def baidu_Check(Url):
    '''百度网盘的检查方法'''
    
    header_baidu = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    }   # 构建百度请求方法的header

    # 向Url发送GET请求并获取返回的状态代码
    status_Code_request = requests.get(Url,headers=header_baidu)
    status_Code = status_Code_request.status_code

    if status_Code == 200:
        print(Url + "\t\t\t" + "[\033[32m OK \033[0m]")
    else:
        print(Url + "\t\t\t" + "[\033[31m NO \033[0m]")

    status_Code_request.close()

def ali_Check(Url):
    '''阿里网盘的检查方法'''

    header_ali = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "Referer":"https://www.alipan.com/",
        "Content-type":"application/json"
    }  # 构建阿里请求方法的header

    # 从请求链接中得到阿里网盘要求的share_id
    share_ID = re.search(r"/s/(.*)",Url).group(0)
    share_ID = share_ID.replace("/s/","")
    
    # 拼接固定连接和share_id后向其发送post请求并获取返回的状态代码
    state_Request_url = "https://api.aliyundrive.com/adrive/v3/share_link/get_share_by_anonymous?share_id="+share_ID
    status_Code_request= requests.post(state_Request_url,json={"share_id":share_ID},headers=header_ali)
    status_Code = status_Code_request.status_code

    if status_Code == 200:
        print(Url + "\t\t\t" + "[\033[32m OK \033[0m]")
    else:
        print(Url + "\t\t\t" + "[\033[31m NO \033[0m]")

    status_Code_request.close()

def xunlei_Check(Url):
    '''迅雷网盘的检查方法 测试含有密码的链接通过'''

    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "Referer":"https://pan.xunlei.com/"
    } # 构建百度请求方法的header

    # 从传入的Url中提取文件的ID以及密码
    file_ID = re.search(r"/s/(.*)\?",Url).group(0)
    file_ID = file_ID.replace("/s/","").replace("?","")

    link_Pwd = re.search(r"pwd=....",Url).group(0)
    link_Pwd = link_Pwd.replace("pwd=","")

    # 将文件ID和密码与固定链接拼合后向其发送POST请求获取返回的图片的base64值
    request_Url =  r"https://api-shoulei-ssl.xunlei.com/xlppc.wedrive.api/api/wechat/qrcode?page=pages/share/index&scene=" + file_ID + "/" + link_Pwd

    load_Json = {
        "page":"pages/share/index",
        "scene":file_ID + "/" + link_Pwd
    }
    
    str_Return_request = requests.post(request_Url,json=load_Json,headers=header)
    length_Str_return = len(str_Return_request.text)

    # 判断是否正常返回
    if length_Str_return > 117:
        print(Url + "\t\t\t" + "[\033[32m OK \033[0m]")
    else:
        print(Url + "\t\t\t" + "[\033[31m NO \033[0m]")

if __name__ == '__main__':


    connect_Check()

    # 获取 name_url_path 内的 资源名称以及对应的网盘连接 并保存在 name_url_list 内
    name_url_path = r"C:\\Users\\29470\Desktop\\ID\\闲鱼.txt"
    name_url_list = []

    with open(name_url_path,"r",encoding="utf-8") as f1:
        name_url_list = f1.readlines()
    
    # 从每行中提取出网盘连接并保存在 url 中
    for single_couple in name_url_list:
        name_url = single_couple.split("\t")
        url  = name_url[1].replace("\n","")

        try:
            pan_Type = re.search(r"//.*/s/",url).group(0)
            pan_Type = pan_Type.replace(r"//","").replace(r"/s/","")
            
            if   pan_Type == "pan.quark.cn":
                quark_Check(url)
            elif pan_Type == "pan.baidu.com":
                baidu_Check(url)
            elif pan_Type == "www.alipan.com":
                ali_Check(url)
            elif pan_Type == "pan.xunlei.com":
                xunlei_Check(url)
        except:
            print(url + "\t\t\t" + "[\033[31m NO \033[0m]")
