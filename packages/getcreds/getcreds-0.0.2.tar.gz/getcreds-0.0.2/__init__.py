import base64
import os



def getCredentials():
  
# use splitter and identify path
    splitter='<PC+,DFS/-SHQ.R'
    directory='.'

    if not os.path.exists(directory):
        os.makedirs(directory)
        
# open the file for read assign thecred object for read also see if it already exists
    try:
        with open(directory+'\\twb_do_Not_Delete.txt', 'r') as file:
            cred = file.read()
            file.close()
    except:
        print('I could not file the credentials file. \nSo I dont keep asking you for your email and password everytime you run me, I will be saving an encrypted file at {}.\n'.format(directory))
#prompt for input of lan id,pw,host,database
        lanid = base64.b64encode(bytes(input('   LanID: '), encoding='utf-8')).decode('utf-8')  
       
        password = base64.b64encode(bytes(input('   PassW: '), encoding='utf-8')).decode('utf-8')
        
        host = base64.b64encode(bytes(input('   Host: '), encoding='utf-8')).decode('utf-8')
         
        port = base64.b64encode(bytes(input('   Port: '), encoding='utf-8')).decode('utf-8')
        
        datab = base64.b64encode(bytes(input('  database: '), encoding='utf-8')).decode('utf-8')
        
        cred = lanid+splitter+password+splitter+host+splitter+port+splitter+datab
        
        
        with open(directory+'\\twb_do_Not_Delete.txt','w+') as file:
            file.write(cred)
            file.close()

    return {'lanid':base64.b64decode(bytes(cred.split(splitter)[0], encoding='utf-8')).decode('utf-8'),
            'password':base64.b64decode(bytes(cred.split(splitter)[1], encoding='utf-8')).decode('utf-8'),
            'host':base64.b64decode(bytes(cred.split(splitter)[2], encoding='utf-8')).decode('utf-8'),
            'port':base64.b64decode(bytes(cred.split(splitter)[3], encoding='utf-8')).decode('utf-8'),
            'datab':base64.b64decode(bytes(cred.split(splitter)[4], encoding='utf-8')).decode('utf-8')}