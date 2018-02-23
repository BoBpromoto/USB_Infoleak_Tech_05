#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp949 -*-

from winreg import *
import sys
import os
import platform
import pyevtx
import wmi

def D_classes() : 
    global d_class_id, d_unique_instance_id, search4log
    varSubkey = "SYSTEM" # 서브레지스트리 목록 지정
    varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE) # 루트 레지스트리 핸들 객체 얻기
    varinitKey = OpenKey(varReg, varSubkey) # 레지스트리 핸들 객체 얻기

    deviceclass = ['{10497b1b-ba51-44e5-8318-a65c837b6661}', '{53f56307-b6bf-11d0-94f2-00a0c91efb8b}', 
    '{53f5630d-b6bf-11d0-94f2-00a0c91efb8b}', '{6ac27878-a6fa-4155-ba85-f98f491d4f33}']
    d_class_id = list()
    d_unique_instance_id = list()
    search4log = list()

    for z in range(1024) :
        try :
            searchKey = OpenKey(varReg,varSubkey) 
            searchKeyname = EnumKey(varinitKey, z)
            for num in range(1000) :
                if len(str(num)) == 1 :
                    number = "00"+str(num)
                elif len(str(num)) == 2 :
                    number = "0"+str(num)
                else :
                    number = str(num)

                if searchKeyname in ("ControlSet"+number) :
                    firstsubKey = "%s\\%s" % (varSubkey, searchKeyname+"\control\DeviceClasses")
                    varKey = OpenKey(varReg, firstsubKey)
                    for i in range(1024):
                        try:
                            keyname = EnumKey(varKey, i)
                            if keyname in deviceclass :
                                # print(keyname)
                                varSubkey2 = "%s\\%s" % (firstsubKey, keyname) 
                                varKey2 = OpenKey(varReg, varSubkey2) 
                                for j in range(1024):
                                    try:
                                        keyname2 = EnumKey(varKey2, j)
                                        # print(keyname2)
                                        if "#USBSTOR#" in keyname2 :
                                        	varSubkey3 = "%s\\%s" % (varSubkey2, keyname2)
                                        	varKey3 = OpenKey(varReg, varSubkey3)
                                        	for k in range(1024) :
                                        		_name, _value, _type = EnumValue(varKey3, k)
                                        		# print (_value)
                                        		search4log.append(searchKeyname + " : " + _value)
                                        		d_class_id.append(searchKeyname + " : " + _value.split("\\")[1])
                                        		d_unique_instance_id.append(searchKeyname + " : " + _value.split("\\")[2].split("&")[1])
                                    except :
                                        errorMsg = "Exception Inner:", sys.exc_info()[0]
                                CloseKey(varKey3)
                                CloseKey(varKey2)
                        except :
                            errorMsg = "Exception Inner:", sys.exc_info()[0]
                    CloseKey(varKey)
            CloseKey(searchKey)
        except:
            errorMsg = "Exception Outter:", sys.exc_info()[0]
            break
        
    CloseKey(varinitKey)
    CloseKey(varReg)

def D_classes_1() :
    global stor_d_name
    stor_d_name = list()
    varSubkey = "SYSTEM"
    varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    varinitKey = OpenKey(varReg, varSubkey)
    for z in range(1024) :
        try :
            searchKey = OpenKey(varReg,varSubkey)
            searchKeyname = EnumKey(varinitKey, z)
            for num in range(1000) :
                if len(str(num)) == 1 :
                    number = "00"+str(num)
                elif len(str(num)) == 2 :
                    number = "0"+str(num)
                else :
                    number = str(num)

                if searchKeyname in ("ControlSet"+number) :
                    firstsubKey = "%s\\%s" % (varSubkey, searchKeyname+"\Enum\\USBSTOR")
                    varKey = OpenKey(varReg, firstsubKey)
                    for i in range(1024) :
                        try :
                            keyname = EnumKey(varKey, i)
                            stor_d_name.append(searchKeyname + " : " + keyname)
                        except:
                            errorMsg = "Exception Inner:", sys.exc_info()[0]
                            break
                        
                    CloseKey(varKey)
        except:
        	errorMsg = "Exception Outter:", sys.exc_info()[0]
        	break            
        CloseKey(searchKey)
    CloseKey(varinitKey)
    CloseKey(varReg)

def V_id_P_id() :
	global v_id_p_id
	v_id_p_id = list()
	varSubkey = "SYSTEM"
	varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
	varinitKey = OpenKey(varReg, varSubkey)
	for z in range(1024) :
		try :
			searchKey = OpenKey(varReg,varSubkey)
			searchKeyname = EnumKey(varinitKey, z)
			for num in range(1000) :
				if len(str(num)) == 1 :
				    number = "00"+str(num)
				elif len(str(num)) == 2 :
				    number = "0"+str(num)
				else :
				    number = str(num)

				if searchKeyname in ("ControlSet"+number) :
				    firstsubKey = "%s\\%s" % (varSubkey, searchKeyname+"\Enum\\USB")
				    for i in range(1024) :
				        try :
				            varKey = OpenKey(varReg, firstsubKey)
				            keyname = EnumKey(varKey, i)
				            varSubkey2 = "%s\\%s" % (firstsubKey, keyname)
				            varKey2 = OpenKey(varReg, varSubkey2)
				            try :
				                for j in range(1024) :
				                    keyname2 = EnumKey(varKey2, j)
				                    varSubkey3 = "%s\\%s" % (varSubkey2, keyname2)
				                    # print (varSubkey3)
				                    varKey3 = OpenKey(varReg, varSubkey3)
				                    for k in range(1024) :
				                        n, v, t = EnumValue(varKey3, k)
				                        if ("ParentIdPrefix" in n) :
				                            for serial_loc in range (0, len(d_unique_instance_id)) :
				                            	if d_unique_instance_id[serial_loc].split(" : ")[0] == searchKeyname and d_unique_instance_id[serial_loc].split(" : ")[1] in v :
				                            		v_id_p_id.append(searchKeyname + " : " + keyname)
				            except :    
				                errorMsg = "Exception Inner:", sys.exc_info()[0]
				            CloseKey(varKey2)
				            CloseKey(varKeyK)
				        except :    
				            errorMsg = "Exception Inner:", sys.exc_info()[0]
		except:
		    errorMsg = "Exception Outter:", sys.exc_info()[0]
		    break

	CloseKey(varinitKey)
	CloseKey(varReg)

def mountDevice() :
    global logic_drive_name
    logic_drive_name = list()
    varSubkey = "SYSTEM\MountedDevices"
    varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    varKey = OpenKey(varReg, varSubkey)

    for i in range(1024) :
        try :
            _name, _value, _type = EnumValue(varKey, i)
            if "DosDevice" in _name :
                for serial_loc in range (0, len(d_unique_instance_id)) :
                    if d_unique_instance_id[serial_loc].split(" : ")[1] in str(_value).replace("\\x00","") :
                        logic_drive_name.append(d_unique_instance_id[serial_loc].split(" : ")[0] + " : " + _name[-2:])
        except :
            errorMsg = "Exception Outter:", sys.exc_info()[0]
            break   
    CloseKey(varKey)
    CloseKey(varReg)

def Volume_Deivce() :
    varSubkey = "SOFTWARE\Microsoft\Windows Search"
    varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    varKey = OpenKey(varReg, varSubkey)
    for i in range(1024) :
        try :
            keyname = EnumKey(varKey, i)
            # print (keyname, i)
        except :
            errorMsg = "Exception Outter:", sys.exc_info()[0]
            break 
    CloseKey(varKey)
    CloseKey(varReg)

def VolumeName() :
    global win7_Volname, win10_Volname
    if os_release == '7' :
        win7_Volname = list()
        varSubkey = "SYSTEM\CurrentControlSet\Enum\WpdBusEnumRoot\\UMB"
        varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        varKey = OpenKey(varReg, varSubkey)
        for j in range (0, len(d_class_id)) :
        	for i in range (1024) :
        		try :
        			keyname = EnumKey(varKey, i)
        			if d_class_id[j].split(" : ")[1].upper() in keyname :
        				varSubkey2 = "%s\\%s" % (varSubkey, keyname)
        				varKey2 = OpenKey(varReg, varSubkey2)
        				for k in range(1024) :
        					_name, _value, _type = EnumValue(varKey2, k)
        					if "FriendlyName" in _name :                		
        						win7_Volname.append(d_class_id[j].split(" : ")[0] + " : " + _value)
        				CloseKey(varKey2)
        		except :
        		    errorMsg = "Exception Outter:", sys.exc_info()[0]
        		    break
        CloseKey(varKey)
        CloseKey(varReg)

    elif os_release == '10' :
        win10_Volname = list()
        varSubkey = "SYSTEM\CurrentControlSet\Enum\SWD\WPDBUSENUM"
        varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        varKey = OpenKey(varReg, varSubkey)
        for j in range (0, len(d_class_id)) :
        	for i in range (1024) :
        		try :
        			keyname = EnumKey(varKey, i)
        			if d_class_id[j].split(" : ")[1].upper() in keyname :
        				varSubkey2 = "%s\\%s" % (varSubkey, keyname)
        				varKey2 = OpenKey(varReg, varSubkey2)
        				for k in range(1024) :
        					_name, _value, _type = EnumValue(varKey2, k)
        					if "FriendlyName" in _name :                		
        						win7_Volname.append(d_class_id[j].split(" : ")[0] + " : " + _value)
        				CloseKey(varKey2)
        		except :
        		    errorMsg = "Exception Outter:", sys.exc_info()[0]
        		    break
        CloseKey(varKey)
        CloseKey(varReg)

def setupdevlog() :
	global initcontime, recentcontime
	initcontime = list()
	recentcontime = list()
	filepath = "C:\Windows\INF\setupapi.dev.log"
	file = open(filepath, 'r')
	contents = file.readlines()
	for i in range (0, len(search4log)) :
		for j in range (0, len(contents)) :
			if (search4log[i].split(" : ")[1] in contents[j] and "Install" in contents[j] and "start" in contents[j+1]) :
				initcontime.append(search4log[i].split("\\")[1] + " : " + contents[j+1].split("start ")[1].replace("\n",""))
	initcontime = list(set(initcontime))
	file.close()

def xml_parser(xml_data) :
	if (xml_data[xml_data.find('<EventID>'):xml_data.find('</EventID>')][-4:] == '2003') or (xml_data[xml_data.find('<EventID>'):xml_data.find('</EventID>')][-4:] == '2100') :
		print (xml_data)


def Eventlogload() : # https://github.com/libyal/libevtx/wiki/Development
	file_object = open("C:\Windows\System32\winevt\Logs\Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx", "rb")
	evtx_file = pyevtx.file()
	evtx_file.open_file_object(file_object)

	# help(pyevtx.file) # How to use pyevtx

	for event_cnt in range (0, evtx_file.number_of_records) :
		record = evtx_file.get_record(event_cnt)
		xml_parser(record.xml_string)

	evtx_file.close()



if __name__ == '__main__' :

	global os_release
	os_release = platform.release()
	D_classes()
	D_classes_1()
	V_id_P_id()
	mountDevice()
	Volume_Deivce()
	VolumeName()
	setupdevlog()
	Eventlogload()

	print ("OS System Info : ", end=" ");print (platform.platform())
	print ("Device Name : ", end=" "); print (d_class_id)
	print ("USBSTOR Device Name : ", end=" "); print (stor_d_name)
	print ("Serial_Number : ", end=" "); print (d_unique_instance_id)
	print ("Vander & Product ID : ", end=" "); print (v_id_p_id)
	print ("Logical Drive name : ", end=" "); print (logic_drive_name)
	if os_release == "7" :
		print ("Mount Volume Name : ", end=" "); print(win7_Volname)
	elif os_release == "10" :
		print ("Mount Volume Name : ", end=" "); print (win10_Volname)
	else :
		pass
	print ("Setupapi.dev.log : ", end=" "); print (search4log)
	print ("Device Install Time : ", end=" "); print(initcontime)

