import subprocess
import psutil

class Aribox:
    def __init(self):
        # Welcome message
        print("    _____")
        print("   |     |")
        print("   | | | |")
        print("   |_____|")
        print("   __|_|__ ")
        print("Welcome to Aribox")
        print("RFID reader started... beep beep beep...")
        print("")
        print("Press Ctrl-C to stop.")
        print("Waiting for a card...")
        self.proc = None
        pass
    
       
    def launch_subprocess(self, action):
        print("Launching",action,"...")
        self.proc = subprocess.Popen(['/bin/sh', '-c', action],
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.STDOUT)
    
    def stop_subprocesses(self):
        if not self.proc:
            return
        
        proc_pid = self.proc.pid
        print(f"Stopping all subprocesses associated with {proc_pid}")
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
        self.proc = None