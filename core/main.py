__author__ = 'gally'
import json
import os
import paramiko
import configparser
import threading
import multiprocessing


from bin.course import *
path = '%s\\conf\setting.txt'%base_dir
web_servers_conf_path = '%s\\conf\host_info.ini'%base_dir
db_path = '%s\\db\Lists_Of_Servers'%base_dir


def interactive(*args):
    Exit_Flag = True
    while Exit_Flag:
        print('*'*8 + 'Welcome Gally-J Jump Server' + 8*'*'+'\n'+
        '-'*8 + 'List of Groups of Servers' + '-'*8 + '\n')
        choice = input('''1:Show Groups
2:Conncet Servers
3:Exit
Please Inpurt Your Choice:''')
        if choice == '1':
            list_server()
        elif choice == '2':
            connect_server()
        elif choice == '3':
            Exit_Flag = False
        else:
            print('请输入正确选项！')

def list_server(*args):
    list_choice = input('''1: Web Servers
2: Mail Servers
3: Docker Servers
4: Exit
Please Inpurt Your Choice:''')
    while True:
        with open(db_path,'r') as f:
            lists_of_server = json.load(f)
        if list_choice == '1':
            print('Web Servers:%s'%lists_of_server['Web Servers'])
            break
        elif list_choice == '2':
            print('Mail Servers:%s'%lists_of_server['Mail Servers'])
        elif list_choice == '3':
            print('3')
        else:
            break





def exec_cmd(cmd,ip,username,password):
    trans = paramiko.Transport((ip,22))
    trans.connect(username=username,password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = trans
    stdin,stdout,stderr = ssh.exec_command(cmd)
    print('--------CMD SHOW OF %s--------'%ip +'\n'+ stdout.read().decode())

def put_file(local_file,distant_file,ip,username,password):
    trans = paramiko.Transport((ip, 22))
    trans.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(trans)
    sftp.put(local_file,distant_file)

def get_file(distant_file,local_file,ip,username,password):
    trans = paramiko.Transport((ip, 22))
    trans.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(trans)
    sftp.get(distant_file,local_file,)

def get_configure():
    config = configparser.ConfigParser()
    config.read(web_servers_conf_path)
    config_list = []
    total_config_list = []
    for i in config.sections():
        ret = config.items(i)
        host_config = ret[0][1] + ',' + ret[1][1] + ',' + ret[3][1] + ',' + ret[4][1]
        host_config_list = host_config.split(',')
        config_list.append(host_config)

    return config_list





def connect_server(*args):
    while True:
        choice = input('''1: Web Servers
2: Mail Servers
3: Docker Servers
4: Exit
Please Inpurt Your Choice:''')
        # config = configparser.ConfigParser()
        # config.read(web_servers_conf_path)
        if choice == '4':
            break
        else:
            print('1:exec cmd\n2:file operations')
            sub_choice = input('Please Inpurt Your Choice:')
            while True:
                if sub_choice == '1':
                    cmd = input('>>>:')
                    if cmd == 'exit':
                        break
                    else:
                        config = get_configure()
                        p_list = []
                        for i in config:
                            ip = i.split(',')[1]
                            username = i.split(',')[2]
                            password = i.split(',')[3]
                            p = multiprocessing.Process(target=exec_cmd,args=(cmd,ip,username,password,))
                            p.start()
                            p_list.append(p)
                        for res in p_list:
                            res.join()

                elif sub_choice == '2':
                    cmd = input('>>>')
                    if cmd == 'exit':
                        break
                    elif 'put' in cmd:
                        local_file = cmd.split()[1]
                        distant_file = cmd.split()[2]
                        p_list = []
                        config = get_configure()
                        for i in config:
                            ip = i.split(',')[1]
                            username = i.split(',')[2]
                            password = i.split(',')[3]
                            p = multiprocessing.Process(target=put_file,args=(local_file,distant_file,ip,username,password,))
                            p.start()
                            p_list.append(p)
                        for res in p_list:
                            res.join()


                    elif 'get' in cmd:
                        local_file = cmd.split()[2]
                        distant_file = cmd.split()[1]

                        p_list = []
                        config = get_configure()
                        for i in config:
                            ip = i.split(',')[1]
                            username = i.split(',')[2]
                            password = i.split(',')[3]
                            p = multiprocessing.Process(target=get_file,
                                                        args=(distant_file,local_file,ip,username,password,))
                            p.start()
                            p_list.append(p)
                        for res in p_list:
                            res.join()


def run():
    interactive()