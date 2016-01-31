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
        processes = get_current_processes()
        print("Backing up your current work")
        now = time.strftime("%Y-%m-%d.%H.%M.%S")
        f = open(r"{}/{}.session".format(sessionPath, now), "wt")
        for line in processes:
            f.write(line)
            f.write(os.linesep)
        f.flush()
        f.close()

        sessions = get_backups()
        if len(sessions) > 5:
            sessions.sort()
            for s in sessions[:len(sessions) - 5]:
                os.remove(s)
        time.sleep(60)


def get_backups():
    """
    获取备份文件列表
    :return:
    """
    sessions = list(os.path.join(sessionPath, file) for file in os.listdir(sessionPath) if file.endswith(".session"))
    return sessions


def get_current_processes():
    """
    获取当前的进程列表

    :return:
    """
    procs = psutil.process_iter()
    session = []
    for proc in procs:
        try:
            path = proc.exe()
            if path not in session:
                session.append(path)
        except psutil.AccessDenied:
            pass
    return session


def restore():
    """
    Restore you last workspace
    """
    sessions = get_backups()
    if not sessions:
        if not sessions:
            print("No session found")
            return
    sessions.sort()
    last_session = sessions[-1]
    started_processes = get_current_processes()
    print("Starts to restore your last session")
    with open(last_session) as session_file:
        for proc in session_file:
            proc = proc.strip()
            if proc in started_processes:
                continue
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
        subprocess.Popen(["./" + exe])  # linux/Mac下需加上当前目录（.）
    except FileNotFoundError:
        print("cannot open:", abs_path)


if __name__ == '__main__':
    restore()
    backup()
