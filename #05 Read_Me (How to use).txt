		===============================================================
		|| 	BoB 6th Digital_Forensic 3rd Stage Assignment	     ||
		||							     ||
		||	    Category : Tech 	      No. 05		     ||	
		||							     ||
		||		     @Author : L3ad0xff 	   	     ||
		||							     ||
		||    		 Information Leakage by USB		     ||
		===============================================================

  ��� ������ python3.6 ȯ�濡�� �̷������.
  �Ʒ� python code�� ���� ��Ű�� ���ؼ��� �߰� ����� �ʿ��ϴ�.

======================================= ȯ�漳�� ================================================

  1. Window
	- Windowȯ�濡�� python3�� ��ġ, ���� ��� ����

	- cmdȭ�鿡�� pip install pypiwin32�� ����

	- cmdȭ�鿡�� pip install https://github.com/libyal/libevtx/releases/download/20170122/libevtx-alpha-20170122.tar.gz ���� (pyevtx ��� ��ġ)
	  ���� ��,
		- ,net framwork 4.51 �̻� ��ġ
		- landinghub.visualstudio.com/visual-cpp-build-tools���� download visual c++ Build Tools 2015 ��ġ
	  (��, python2�� ���� ��ġ �Ǿ� ���� ��� pip3�� �̿��Ͽ� ����)

	- python2�� �Բ� ��ġ�� �Ǿ� ���� ��� cmd���� python �Է� �� python3�� ����ǵ��� ����

======================================== ������ ===============================================

  1. USB_infoleak.py�� LNK_Parser.py�� ���� ��ο� �����Ѵ�.

  2. python USB_infoleak.py�� �����Ѵ�. (evtx ������ ���� ����� ������ �������� �����Ѵ�.)

  3. ������ ��ο� csv ���� 2���� �����ȴ�.
	- 2���� csv file���� Time �׸���� ��� ���� ǥ�������� ��Ÿ ���� ���� -> ����� ���� -> ���Ķ���
	  yyyy-mm-dd hh:mm:ss�� �����Ѵ�.