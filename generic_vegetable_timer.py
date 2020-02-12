from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
from time import sleep
from datetime import datetime
import sys,os

try: 
    # to play alarm sound - optional
    import playsound
    sound_available=True
except:
        sound_available=False

try:
    # desktop notifications - optional
    import notify2
    notify2.init('pomodoro')
except:
    notify2=None

try:
    # progress bar
    from tqdm import tqdm
except ImportError:
    print('need tqdm for progress bar -->  pip install tqdm ')
    exit()

def main(args):
    timer = Pomodoro(args)
    timer.timer()

class Pomodoro():
    def __init__(self,args):
        self.session_mins = args.sess_mins
        self.short_break_mins = args.short_break_mins
        self.long_break_mins = args.long_break_mins
        self.total_sessions = args.resume_sess
        self.sessions_since_break = args.resume_breaks
        self.alarm_path = args.alarm_file
        if not os.path.exists(args.alarm_file) or not sound_available: 
            self.sound_available = False
        else:
            self.sound_available = True

    def run_progress(self,name,minutes):
        for _ in  tqdm(range(int(minutes*60*10)),bar_format='{l_bar}{bar} | {elapsed} < {remaining} ]',desc=name,leave=False,dynamic_ncols=True):
            sleep(0.1)
        if notify2 is not None:
            n = notify2.Notification('pomodoro', f'{name} is over!')
            n.show()
        if self.sound_available:
            playsound.playsound(self.alarm_path)
        self.last_segment_timestamp = datetime.now().isoformat()[len("2020-01-24T"):-7]

    def session(self):
        self.run_progress(f'Session {self.total_sessions+1}',self.session_mins)
        self.total_sessions += 1
        self.sessions_since_break  +=  1

    def short_break(self):
        self.run_progress('Short Break',self.short_break_mins)

    def long_break(self):
        self.run_progress('Long Break',self.long_break_mins)
        self.sessions_since_break = 0

    def timer(self):
        last_session_type = None
        should_continue = True
        print('\033[H\033[2J',end='')
        try:
            while should_continue:
                print(f'Total Sessions: {self.total_sessions} ({self.total_sessions*25/60:.2f} hours worked), Sessions since long break: {self.sessions_since_break}')
                if last_session_type is not None:
                    print(f'{last_session_type} ended at: {self.last_segment_timestamp}',end='')
                    if self.sessions_since_break > 4:
                        print(' - Long break recommended!')
                    else:
                        print()

                cmd = input('Next segment? --> [s]ession, Short [b]reak, Long [B]reak, [E]nd:   \033[2D\033[J')
                if cmd == 's':
                    self.session()
                    last_session_type = 'Session'
                elif cmd == 'b':
                    self.short_break()
                    last_session_type = 'Short break'
                elif cmd == 'B':
                    self.long_break()
                    last_session_type = 'Long break'
                elif cmd == 'E':
                    break
                print('\033[2J\033[H',end='')
        except KeyboardInterrupt:
            pass
        finally:
            print(f'\nTotal sessions: {self.total_sessions} - hours worked: {self.total_sessions*25/60:.2f}')

if __name__ == "__main__":
    parser = ArgumentParser(description="A simple timer to keep you productive!",formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--sess_mins',type=int,default=25)
    parser.add_argument('--short_break_mins',type=int,default=5)
    parser.add_argument('--long_break_mins',type=int,default=10)
    parser.add_argument('--alarm_file',default=os.path.join(os.path.dirname(__file__),'alarm.mp3'), help="Sound file to play at end of segment, requires playsound (pip install playsound)")
    parser.add_argument('--resume_sess',type=int,default=0,help='Set "Total Sessions" counter')
    parser.add_argument('--resume_breaks',type=int,default=0,help='Set "Sessions since long break" counter')
    args = parser.parse_args()
    main(args)




