#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp949 -*-

# @ Author L3ad0xFF

from winreg import *
import sys
import os
import platform
import pyevtx
import csv
import datetime
from LNK_Parser import *

# ==> * Registry Parsing Area *
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

# ==> * Find Install time from setupapi.dev.log Area *
def setupdevlog() :
	global initcontime, recentcontime
	initcontime = {}
	recentcontime = list()
	filepath = "C:\Windows\INF\setupapi.dev.log"
	file = open(filepath, 'r')
	contents = file.readlines()
	for i in range (0, len(search4log)) :
		for j in range (0, len(contents)) :
			if (search4log[i].split(" : ")[1] in contents[j] and "Install" in contents[j] and "start" in contents[j+1]) :
				initcontime = {search4log[i].split("\\")[1] : contents[j+1].split("start ")[1].replace("\n","").replace("/", "-")}
	file.close()

# ==> * EventLog Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx Parsing Area *
def xml_parser(xml_data) :
	if (xml_data[xml_data.find('<EventID>'):xml_data.find('</EventID>')][-4:] == '2003') :
		event_val = {}
		evtx_System = xml_data[xml_data.find('<System>') : xml_data.find('</System>')] # event_id, time, userid
		evtx_UserData = xml_data[xml_data.find('<UserData>') : xml_data.find('</UserData>')] # device name, lifetime

		e_id = xml_data[xml_data.find('<EventID>'):xml_data.find('</EventID>')][-4:]
		e_logtime = evtx_System[evtx_System.find('<TimeCreated SystemTime='):evtx_System.find('Z"/>')].split('="')[1].replace("T"," ")
		e_uid = evtx_System[evtx_System.find('<Security UserID='):].split('"')[1]
		e_device_name = evtx_UserData[evtx_UserData.find('instance='):].split("USBSTOR")[1].split("#")[1]
		e_serial = evtx_UserData[evtx_UserData.find('instance='):].split("USBSTOR")[1].split("#")[2].split("&")[1]
		e_liftime = evtx_UserData[evtx_UserData.find('lifetime='):].split('"')[1]

		event_val = {"Event_ID" : e_id, "Log_Time" : e_logtime, "User_ID" : e_uid, "Device_Name" : e_device_name,
		"Serial_Number" : e_serial, "Lifetime" : e_liftime}
		# print (event_val, end=" "); print ("\n")
		return event_val

	elif (xml_data[xml_data.find('<EventID>'):xml_data.find('</EventID>')][-4:] == '2100') :
		event_val = {}
		evtx_System = xml_data[xml_data.find('<System>') : xml_data.find('</System>')] # event_id, time, userid
		evtx_UserData = xml_data[xml_data.find('<UserData>') : xml_data.find('</UserData>')] # device name, lifetime

		e_id = xml_data[xml_data.find('<EventID>'):xml_data.find('</EventID>')][-4:]
		e_logtime = evtx_System[evtx_System.find('<TimeCreated SystemTime='):evtx_System.find('Z"/>')].split('="')[1].replace("T"," ")
		e_uid = evtx_System[evtx_System.find('<Security UserID='):].split('"')[1]
		e_device_name = evtx_UserData[evtx_UserData.find('instance='):].split("USBSTOR")[1].split("#")[1]
		e_serial = evtx_UserData[evtx_UserData.find('instance='):].split("USBSTOR")[1].split("#")[2].split("&")[1]
		e_liftime = evtx_UserData[evtx_UserData.find('lifetime='):].split('"')[1]

		event_val = {"Event_ID" : e_id, "Log_Time" : e_logtime, "User_ID" : e_uid, "Device_Name" : e_device_name,
		"Serial_Number" : e_serial, "Lifetime" : e_liftime}
		return event_val
		# print (event_val, end =" "); print("\n")
	else :
		return 0


def Eventlogload() : # https://github.com/libyal/libevtx/wiki/Development
	global file, csvWriter
	file_object = open("C:\Windows\System32\winevt\Logs\Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx", "rb")
	evtx_file = pyevtx.file()
	evtx_file.open_file_object(file_object)
	file = open("./regi_evtx.csv", 'w', newline = "\n")
	csvWriter = csv.writer(file)        
	csvWriter.writerow(['ControlSet', 'Device_Name', 'Serial_Number', 'Mounted_Volume_Name', 'Logical_Drive', 'Init Connected Time', 'Connected Time',
		'Disconnected Time', 'LifeTime'])

	# help(pyevtx.file) # How to use pyevtx
	# print ("\n================== * EventLog Contents * ==================")
	for event_cnt in range (0, evtx_file.number_of_records) :
		record = evtx_file.get_record(event_cnt)
		usb_event_log = xml_parser(record.xml_string)
		if usb_event_log != 0 :
			# print (usb_event_log, end=" "); print("\n")
			r_s_e_csv(usb_event_log)
		else :
			pass
	file.close()
	evtx_file.close()

def regi2dic() :
	global usb_info

	usb_info = {}
	for j in range (0, len(controlSetinfo)) :
		device_list = list()
		stor_device_list = list()
		serial_list = list()
		v_p_list = list()
		logic_drive_list = list()
		volumename_list = list()
		for i in range (0, len(d_class_id)) :
			if controlSetinfo[j] == d_class_id[i].split(" : ")[0] :
				device_list.append(d_class_id[i].split(" : ")[1])
				stor_device_list.append(stor_d_name[i].split(" : ")[1])
				serial_list.append(d_unique_instance_id[i].split(" : ")[1])
				v_p_list.append(v_id_p_id[i].split(" : ")[1])
				logic_drive_list.append(logic_drive_name[i].split(" : ")[1])
				volumename_list.append(win7_Volname[i].split(" : ")[1])

				device_list = list(set(device_list))
				stor_device_list = list(set(stor_device_list))
				serial_list = list(set(serial_list))
				v_p_list = list(set(v_p_list))
				logic_drive_list = list(set(logic_drive_list))
				volumename_list = list(set(volumename_list))

				usb_info[controlSetinfo[j]] = {"Device_Name" : device_list	, "USBSTOR_Device_Name" : stor_device_list,
				"Serial_Number" : serial_list, "Vander & Product" :v_p_list,
				"Logical_Drive" : logic_drive_list, "Mounted_Volume_Name" : volumename_list}

	for j in range (0, len(controlSetinfo)) :
		initcon_list = list()
		for i in range (0, len(usb_info[controlSetinfo[j]]["USBSTOR_Device_Name"])) :
			if usb_info[controlSetinfo[j]]["USBSTOR_Device_Name"][i] in initcontime.keys() :
				initcon_list.append(initcontime[usb_info[controlSetinfo[j]]["USBSTOR_Device_Name"][i]])
				initcon_list = list(set(initcon_list))
				usb_info[controlSetinfo[j]]["Init Connect Time"] = initcon_list

def r_s_e_csv(events) :
	# print (events, end=" "); print("\n")
	if events["Event_ID"] == '2003' :
		for i in range (0, len(controlSetinfo)) :
			for j in range (0, len(usb_info[controlSetinfo[i]]["USBSTOR_Device_Name"])) :
				if ((usb_info[controlSetinfo[i]]["USBSTOR_Device_Name"][j].upper() == events["Device_Name"]) and (usb_info[controlSetinfo[i]]["Serial_Number"][j].upper() == events["Serial_Number"])) :
					csvWriter.writerow([list(usb_info.keys())[i], usb_info[controlSetinfo[i]]["Device_Name"][j], usb_info[controlSetinfo[i]]["Serial_Number"][j],
					usb_info[controlSetinfo[i]]["Mounted_Volume_Name"][j], usb_info[controlSetinfo[i]]["Logical_Drive"][j], usb_info[controlSetinfo[i]]["Init Connect Time"][j],
					events["Log_Time"], "", events["Lifetime"]])
				else :
					pass
	elif events["Event_ID"] == '2100' :
		for i in range (0, len(controlSetinfo)) :
			for j in range (0, len(usb_info[controlSetinfo[i]]["USBSTOR_Device_Name"])) :
				if ((usb_info[controlSetinfo[i]]["USBSTOR_Device_Name"][j].upper() == events["Device_Name"]) and (usb_info[controlSetinfo[i]]["Serial_Number"][j].upper() == events["Serial_Number"])) :
					csvWriter.writerow([list(usb_info.keys())[i], usb_info[controlSetinfo[i]]["Device_Name"][j], usb_info[controlSetinfo[i]]["Serial_Number"][j],
					usb_info[controlSetinfo[i]]["Mounted_Volume_Name"][j], usb_info[controlSetinfo[i]]["Logical_Drive"][j], usb_info[controlSetinfo[i]]["Init Connect Time"][j],
					"", events["Log_Time"], events["Lifetime"]])
				else :
					pass
	else :
		pass

def linkfile() :
	# "C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu" # 시작메뉴
	# "C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Recent" # 최근문서
	# "C:\Users\<username>\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch" # 빠른실행
	# "C:\Users\<username>\Desktop" #바탕화면

	for (path, dirs, files) in os.walk("C:\\"):
		for filename in files:
			ext = os.path.splitext(filename)[-1]
			if (ext == '.lnk') or (ext == '.LNK'):
				lnkfile = "%s/%s" % (path, filename)
				print (lnkfile)
				parse_lnk (lnkfile)

if __name__ == '__main__' :
	global os_release, controlSetinfo
	print ("OS System Info : ", end=" ");print (platform.platform())
	os_release = platform.release()
	controlSetinfo = list()
	D_classes()
	for i in range (0, len(d_class_id)) :
		controlSetinfo.append(d_class_id[i].split(" : ")[0])
		controlSetinfo = list(set(controlSetinfo))
	D_classes_1()
	V_id_P_id()
	mountDevice()
	Volume_Deivce()
	VolumeName()
	setupdevlog()
	regi2dic()
	Eventlogload()
	linkfile()
