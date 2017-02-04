'''
Program done by Derrick D'souza and Pavani Potluri
deds7325 and papo7882
'''

import string
import tftpy
import os
from time import strftime
from datetime import datetime

global version

def input_ipaddr():
    '''
    return a list of ip addresses
    '''
    ipaddr_list= []
    while True:
        ip_addr= raw_input("Enter Management IP (or done): ")
        if ip_addr != 'done':
            ipaddr_list.append(ip_addr)
        else:
            break;
    return ipaddr_list

def timeCalc():
    '''
    return the current time like 2015-01-28_22:30:46
    '''
    timeNow= datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    return timeNow

def read_file(ip_addr):
    '''
    takes the ip address of router as input
    returns the contents of the latest file if present
    '''
    dirList= sorted(os.listdir(os.getcwd()))
    dirList.reverse()
    if len(dirList)==0:
        return 'File not present'
    else:
        data= open(dirList[0])
        file_content= data.read()
        return file_content

def tftp_file(ip_addr):
    '''
    takes the ip address as input
    does comparison of files
    '''
    global savedpath
    os.chdir(savedPath)
    if not os.path.exists('RouterConfig'):
        os.makedirs('RouterConfig')
    os.chdir('RouterConfig')

    #create a router specific folder
    if not os.path.exists(ip_addr):
        os.makedirs(ip_addr)
    os.chdir(ip_addr)

    new_ip = ip_addr
    conn= tftpy.TftpClient(new_ip, 69)
    conn.download('/startup-config', 'temporary.cfg')
    new_ip_addr = open('temporary.cfg')
    newfile_content= new_ip_addr.read()
    os.remove('temporary.cfg')                       #remove file after extracting its contents
    comparison= compare_files(newfile_content,new_ip)

def compare_files(newfile_content,ip):
    '''
    compare file contents and create if different
    '''
    file_content = read_file(ip)
    if file_content != newfile_content:
        print "Saving new configuration for: %s"%(ip_addr)
        new_content= open(str(timeCalc())+'_'+ip_addr+'.cfg','w')
        new_content.write(newfile_content)
        print_output(newfile_content)
        return True
    else:
        print "No new configuration for: %s"%(ip_addr)
        print_output(file_content)
        return False

def print_output(data_in_file):
    '''
    takes file contents as input
    print IOS version and hostname of the router
    '''
    line1 = data_in_file.split()
    if 'version' in line1:
        print "IOS Version:", line1[2]
    line2= data_in_file.split('!')
    line3= line2[2].split(' ')
    print "Hostname is:", line3[1]

if __name__ == "__main__":
    global savedPath    #save original directory path
    savedPath = os.getcwd()
    ipaddr_list= input_ipaddr()
    for i in range(len(ipaddr_list)):
        ip_addr = ipaddr_list[i]
        tftp_file(ip_addr)





