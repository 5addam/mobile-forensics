from ppadb.client import Client as AdbClient
import os, win32file, io, codecs, random, string
from ctypes import *


INTERNAL_STORAGE_PATH = '/mnt/m_internal_storage'
EXTERNAL_STORAGE_PATH = '/mnt/m_external_storage'

def checkMobile():
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    return devices


##################### TASK - 1 #################################
def displayInternalStorge(device):
    print(device.shell(f'ls -LR {INTERNAL_STORAGE_PATH}'))

def displayExternalStorge(device):
    print(device.shell(f'ls -LR {EXTERNAL_STORAGE_PATH}'))


    
def locate_usb():
    drive_list = []
    drivebits = win32file.GetLogicalDrives()
    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            # here if the drive is at least there
            drname = '%c:\\' % chr(ord('A') + d)
            t = win32file.GetDriveType(drname)
            if t == win32file.DRIVE_REMOVABLE:
                drive_list.append(drname)
    return drive_list




############################ TASK - 4 ############################################
def myFmtCallback(command, modifier, arg):
    print(command)
    return 1

def format_drive(Drive, Format, Title):
    fm = windll.LoadLibrary('fmifs.dll')
    FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
    FMIFS_UNKNOWN = 0
    fm.FormatEx(c_wchar_p(Drive), FMIFS_UNKNOWN, c_wchar_p(Format),
                c_wchar_p(Title), True, c_int(0), FMT_CB_FUNC(myFmtCallback))
    print('Format Successfull!! \n')                

############################ TASK - 4 ############################################

# format_drive('E:\\', 'FAT32', 'Some Disk')

# print(os.getcwd())


############################ TASK - 3 ############################################
def get_random_string():
    letters = string.ascii_lowercase
    t= int(random.randint(10,20))
    # print(t)
    result_str = ''.join(random.choice(letters) for i in range(t))
    # print(result_str)
    return (result_str)
    
def overrideData(ramdon_str, dir):
    for root, dirs, files in os.walk(os.path.abspath(dir)):
        for file in files:
            path = os.path.join(root, file)
            with open(path, "rb+") as f:
                data= f.read()
                f.seek(0)
                f.write(ramdon_str.encode("utf8"))
                f.truncate()
    print('Successfully Overriden!! \n')

############################ TASK - 3 ############################################

def main():
    bol = True
    while bol:
        opt = int(input('Press 1 for Mobile \nPress 2 for Other External Devices: '))
        if opt != 1 and opt != 2:
            print('invalid argument')
            continue

        if opt == 1:
            devices = checkMobile()
            if len(devices) <=0:
                print("No Mobile device is connected!! \n")
            else:
                for device in devices:
                    print(f'Device with Serial no.: {device.serial} found.')
                    m_opt = int(input('Enter 0 to list Internal Storage\nPress 1 for External Storage: '))
                    if m_opt == 0:
                        displayInternalStorge(device)
                        print('\n')
                    else:
                        displayExternalStorge(device)                    
                        print('\n')
        else:
            ####################### TASK - 2 ###############################
            usbs = locate_usb()
            if(len(usbs) < 1):
                print('No, Removable drive drive is connected!! \n')
            else:
                print(f'{len(usbs)} External Devices are connected!!')
                for i in usbs:
                    print(f'{i}')
                    usb = int(input(f'Select the external device from [1-{len(usbs)}]: '))
                e_opt = input('Do you want to format it?yes/no: ')
                if e_opt.lower() == 'yes':
                    format_type = input('Enter Format Type - NTFS, FAT32, exFAT: ')
                    if format_type != 'NTFS' and format_type != 'FAT32' and format_type != 'exFAT':
                        print('Invalid Format type entered!!')
                    else:
                        format_drive(usbs[usb-1], format_type, 'Removeable Drive')
                else:
                    e_opt = input('Do you want to override the drive?yes/no: ')
                    if e_opt.lower() == 'yes':
                        random_str = get_random_string()
                        overrideData(random_str, usbs[usb-1])
                    
                    else:
                        pass
                        
        exit_opt = input('Press q to exit OR any key to containue: ')
        if exit_opt.lower() == 'q':
            bol = False


if __name__ == "__main__":
    main()