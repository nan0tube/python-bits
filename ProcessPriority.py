from ctypes import windll, c_uint

OpenProcess         = windll.kernel32.OpenProcess
CloseHandle         = windll.kernel32.CloseHandle
GetPriorityClass    = windll.kernel32.GetPriorityClass
SetPriorityClass    = windll.kernel32.SetPriorityClass

ABOVE_NORMAL_PRIORITY_CLASS = 0x8000
BELOW_NORMAL_PRIORITY_CLASS = 0x4000
HIGH_PRIORITY_CLASS         = 0x0080
IDLE_PRIORITY_CLASS         = 0x0040
NORMAL_PRIORITY_CLASS       = 0x0020
REALTIME_PRIORITY_CLASS     = 0x0100

PROCESS_QUERY_INFORMATION   = 0x0400
PROCESS_SET_INFORMATION     = 0x0200

def GetProcessPriority(pid):
    ret = 0
    hProcess = OpenProcess(c_uint(PROCESS_QUERY_INFORMATION), 0, c_uint(pid))
    if hProcess:
        ret = GetPriorityClass(hProcess)
        CloseHandle(hProcess)
    return ret

def SetProcessPriority(pid, priority):
    ret = 0
    hProcess = OpenProcess(c_uint(PROCESS_SET_INFORMATION), 0, c_uint(pid))
    if hProcess:
        ret = SetPriorityClass(hProcess, c_uint(priority))
        CloseHandle(hProcess)
    return ret

if __name__ == '__main__':
    import argparse
    
    description = 'Get/Set the priority class for the specified process.'
    choices = {'ABOVE_NORMAL'   : 0x8000,
               'BELOW_NORMAL'   : 0x4000,
               'HIGH'           : 0x0080,
               'IDLE'           : 0x0040,
               'NORMAL'         : 0x0020,
               'REALTIME'       : 0x0100}
    
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('pid', type=int)
    parser.add_argument('priority', nargs='?', choices=choices)
    args = parser.parse_args()
    
    if args.priority:
        ret = SetProcessPriority(args.pid, choices[args.priority])
    else:
        ret = GetProcessPriority(args.pid)
        if ret:
            for k, v in choices.items():
                if ret == v:
                    ret = k
                    break
    print ret
