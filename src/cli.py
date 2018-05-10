from threading import Thread
import cmd

from sock.server import Server


class Cli(cmd.Cmd):
    def __init__(self, program):
        cmd.Cmd.__init__(self)
        self.program = program
        self.get_coords = self.program.data.get_coords
        self.prompt = '>>> '

    def do_quit(self, args):
        print("\nArresto sistema in corso...\n")
        self.program.quit()
        return 1

    def do_state(self, args):
        print(self.program.arm)

    def do_showTable(self, args):
        print(self.program.table)

    def do_goBack(self, args):
        self.program.arm.goto_back = True

    def do_goto(self, args):
        x, y = map(int,args.split())
        arm = self.program.arm
        arm.pos = self.get_coords(x,y)
        print("goto %d %d " %(arm.pos))
        arm.offset_time()
        arm.goto_start()

    def do_newNumber(self, args):
        print(self.program.table.new_num(int(args)))

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
