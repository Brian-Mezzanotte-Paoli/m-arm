from threading import Thread
from time import sleep
import cmd
import pytesseract
from PIL import Image

from sock.server import Server

class Cli(cmd.Cmd):
    def __init__(self, program):
        cmd.Cmd.__init__(self)
        self.program = program
        self.get_coords = self.program.data.get_coords
        self.prompt = '>>> '

    def do_wait_arm(self, arg=""):
        arm = self.program.arm
        sleep(0.1)
        while arm.running:
            sleep(0.1)
        
        
    def do_quit(self, args):
        ft = self.program.arm.ft
        ft.stopOnline()
        print("\nArresto sistema in corso...\n")
        self.program.arm.playing = False
        return True

    def help_quit(self): print ("Close program")

    def do_state(self, args):
        print(self.program.arm)
    def help_state(self): print ("Show state of buttons and motors of arm")

    def do_show(self, args):
        print(self.program.table)
    def help_show(self): print ("Show the table of the game")

    def do_go_back(self, args):
        self.program.arm.goto_back = True
    def help_go_back(self): print ("Move arm in 0 point")

    def do_go(self, args):
        x, y = map(int,args.split())
        if 0<=x<=8 and 0<=y<=2:
            arm = self.program.arm
            arm.pos = self.get_coords(x,y)
            print("goto %d %d " %(arm.pos))
            arm.offset_time()
            arm.goto_start()
        else:
            print("%d %d -> out of matrix" %(x,y))

    def do_go_id(self, args):
        arm = self.program.arm
        arm.pos = self.get_coords(4,0)
        arm.offset_time()
        arm.goto_start()

    def do_get_id(self, arg):
        arm = self.program.arm
        arm.pos = self.get_coords(4,0)
        arm.offset_time()
        arm.goto_start()
        self.do_wait_arm()
        arm.release = True
        self.do_wait_arm()
        ft = self.program.arm.ft
        image_final = None
        while image_final is None:
            try:
                ft.startCameraOnline()
                sleep(2.5)
                frame = ft.getCameraFrame()
                sleep(1)
                with open("frame.jpg", "wb") as photo:
                    photo.write(bytearray(frame))
                sleep(1)
                pphoto = Image.open("frame.jpg")
                image_final = pytesseract.image_to_string(pphoto, config='outputbase digits')
                ft.stopCameraOnline()
                print(image_final)
                self.program.table = self.program.data.get_table(int(image_final))
            except Exception as e:
                print("azione fallita")
                image_final = None
                ft.stopCameraOnline()
                sleep(1)
        self.do_wait_arm()
        arm.goto_back = True


    def do_row_bool(self,args):
        print(self.program.table.row_bool(int(args)))

    def do_call_num(self, args):
        pos = self.program.table.call_num(int(args))
        if pos:
            self.do_catch('')
            arm = self.program.arm
            self.do_wait_arm()
            arm.pos = self.get_coords(*pos)
            arm.offset_time()
            arm.goto_start()
            self.do_wait_arm()
            arm.release = True
            self.do_wait_arm()
            arm.goto_back = True

    def do_catch(self, args):
        self.program.arm.catch = True

    def do_release(self, args):
        self.program.arm.release = True

    def do_server(self, args):
        print("\nApertura server\n")
        server = Server(self.program)
        t_server = Thread(target=server.run)
        t_server.start()
        print("\nServer aperto\n")





    def run(self):
        self.cmdloop()
