from tqdm import tqdm
from time import sleep
from datetime import datetime
import sys,os
try: 
    import playsound
    alarm_path = os.path.join(os.path.dirname(__file__),'alarm.mp3')
    if not  os.path.exists(alarm_path):
        Salarm_path = None
except:
    alarm_path = None

try:
    import notify2
    notify2.init('pomodoro')
except:
    notify2=None
session_mins = 25
short_break_mins = 5
long_break_mins = 10
print('\033[H\033[2J',end='')
total_sessions = int(sys.argv[1]) if len(sys.argv) > 1 else 0
sessions_since_break = int(sys.argv[2]) if len(sys.argv) > 2 else 0
should_continue = True
extra_up = False

def run_progress(name,minutes):
    for _ in  tqdm(range(int(minutes*60*10)),bar_format='{l_bar}{bar} | {elapsed} < {remaining} ]',desc=name,leave=False,dynamic_ncols=True):
        sleep(0.1)
    if notify2 is not None:
        n = notify2.Notification('pomodoro', f'{name} is over!')
        n.show()
    if alarm_path is not None:
        playsound.playsound(alarm_path)

def session():
    global total_sessions
    global sessions_since_break
    run_progress(f'Session {total_sessions+1}',session_mins)
    total_sessions = total_sessions + 1
    sessions_since_break  = sessions_since_break + 1

def short_break():
    run_progress('Short Break',short_break_mins)

def long_break():
    global sessions_since_break
    run_progress('Long Break',long_break_mins)
    sessions_since_break = 0
last_session_type = None
try:
    while should_continue:
        print(f'Total Sessions: {total_sessions} ({total_sessions*25/60:.2f} hours worked), Sessions since long break: {sessions_since_break}')
        if last_session_type is not None:
            print(f'{last_session_type} ended at: {datetime.utcnow().isoformat()[len("2020-01-24T"):-7]}',end='')
            if sessions_since_break > 4:
                print(' - Long break recommended!')
            else:
                print()

        cmd = input('Next segment? --> [s]ession, Short [b]reak, Long [B]reak, [E]nd:   \033[2D\033[J')
        if cmd == 's':
            session()
            last_session_type = 'Session'
        elif cmd == 'b':
            short_break()
            last_session_type = 'Short break'
        elif cmd == 'B':
            long_break()
            last_session_type = 'Long break'
        elif cmd == 'E':
            break
        print('\033[2J\033[H',end='')
except KeyboardInterrupt:
    pass
finally:
    print(f'\nTotal sessions: {total_sessions} - hours worked: {total_sessions*25/60:.2f}')

