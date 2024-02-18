import os
def shutdown_logout(msg):
    if "SHUTDOWN".lower() in msg.lower():
        os.system('shutdown -s -t 15')
        return ["1","shutdown"]
    elif "LOGOUT".lower() in msg.lower():
        os.system('shutdown -l')
        return ["1","logout"]
    else:
        return ["0","0"]