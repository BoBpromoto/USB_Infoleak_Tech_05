		===============================================================
		|| 	BoB 6th Digital_Forensic 3rd Stage Assignment	     ||
		||							     ||
		||	    Category : Tech 	      No. 05		     ||	
		||							     ||
		||		     @Author : L3ad0xff 	   	     ||
		||							     ||
		||    		 Information Leakage by USB		     ||
		===============================================================

  모든 개발은 python3.6 환경에서 이루어졌다.
  아래 python code를 실행 시키기 위해서는 추가 모듈이 필요하다.

======================================= 환경설정 ================================================

  1. Window
	- Window환경에서 python3를 설치, 실행 경로 지정

	- cmd화면에서 pip install pypiwin32을 실행

	- cmd화면에서 pip install https://github.com/libyal/libevtx/releases/download/20170122/libevtx-alpha-20170122.tar.gz 실행 (pyevtx 모듈 설치)
	  오류 시,
		- ,net framwork 4.51 이상 설치
		- landinghub.visualstudio.com/visual-cpp-build-tools에서 download visual c++ Build Tools 2015 설치
	  (단, python2와 같이 설치 되어 있을 경우 pip3를 이용하여 실행)

	- python2와 함께 설치가 되어 있을 경우 cmd에서 python 입력 시 python3가 실행되도록 설정

======================================== 실행방법 ===============================================

  1. USB_infoleak.py와 LNK_Parser.py를 같은 경로에 저장한다.

  2. python USB_infoleak.py를 실행한다. (evtx 접근을 위해 실행시 관리자 권한으로 실행한다.)

  3. 실행한 경로에 csv 파일 2개가 생성된다.
	- 2개의 csv file에서 Time 항목들의 경우 셀의 표시형식을 기타 형식 지정 -> 사용자 지정 -> 형식란에
	  yyyy-mm-dd hh:mm:ss로 변경한다.