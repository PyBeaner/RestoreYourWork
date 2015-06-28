import os
import subprocess
import psutil
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
sessionPath = os.path.join(base_dir, "sessions")
if not os.path.exists(sessionPath):
    os.mkdir(sessionPath)

logPath = os.path.join(base_dir, "logs")
if not os.path.exists(logPath):
    os.mkdir(logPath)


def backup():
    """
    Backup your current running processes
    """
    while 1:
        procs = psutil.process_iter()
        session = []
        for proc in procs:
            try:
                path = proc.exe()
                if path not in session:
                    session.append(path)
            except psutil.AccessDenied:
                pass

        print("Backing up your current work")
        now = time.strftime("%Y-%m-%d %H.%M.%S")
        f = open(r"{}\{}.session".format(sessionPath, now), "wt")
        for line in session:
            f.write(line)
            f.write(os.linesep)
        f.close()
        time.sleep(300)


def restore():
    """
    Restore you last workspace
    """
    sessions = list(file for file in os.listdir(sessionPath) if file.endswith(".session"))
    if not sessions:
        if not sessions:
            now = time.strftime("%Y-%m-%d %H.%M.%S")
            print("No session found", file=open(r"{}\{}.log".format(logPath, now)))
            return
    sessions.sort()
    last_session = sessions[-1]
    print("Starts to restore your last session")
    with open(os.path.join(sessionPath, last_session)) as session_file:
        for proc in session_file:
            dir, exe = os.path.dirname(proc), os.path.basename(proc)
            start_process(dir, exe, abs_path=proc)
            time.sleep(2)


def start_process(dir, exe, abs_path=None):
    try:
        if abs_path:
            dir = os.path.abspath(os.path.dirname(abs_path))
            exe = os.path.basename(abs_path)
        else:
            dir = os.path.abspath(dir)
        exe = exe.strip()
        if not exe:
            return
        print("working on path:", dir)
        os.chdir(dir)
        print("start process:", exe)
        subprocess.Popen([exe])
    except FileNotFoundError:
        print("cannot open:", abs_path)


if __name__ == '__main__':
    restore()
    backup()
