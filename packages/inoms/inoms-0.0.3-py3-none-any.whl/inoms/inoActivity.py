import ctypes

def MsgBox(text,title):
    MessageBox = ctypes.windll.user32.MessageBoxW
    #returnValue = MessageBox(None,'Hello','Window Title',0x4000| 0x03 | 0x30)
    returnValue = MessageBox(0,text,title,0x01)
    print(returnValue)



"""
#Return Value
Ok          =   1
Cancel      =   2
Abort       =   3
Retry       =   4
Ignore      =   5
Yes         =   6
No          =   7
Try Again   =   10
Continue    =   11
-------------------------------

#Option
MB_OK = 0x0
MB_OKCXL = 0x01
MB_ABT_RETY_IGNR = 0x02
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_RETY_CXL = 0x05
MB_CXL_TYAGN_CTN = 0x06
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

"""