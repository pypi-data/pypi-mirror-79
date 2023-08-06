import sys
import threading as th
from _tkinter import TclError
from io import StringIO
from tkinter import Tk, Canvas, Button, Entry, Label
from tkinter import END, WORD, INSERT, NW
from tkinter.scrolledtext import ScrolledText

import modi
from modi.modi import MODI
from modi.util.msgutil import parse_message
import time


class Debugger(MODI):
    def __init__(self, *args, **kwargs):
        self._buffer = StringIO()
        sys.stdout = self._buffer
        super().__init__(verbose=True, *args, **kwargs)
        _DebuggerWindow(self, self._buffer).start()


class _DebuggerWindow(th.Thread):
    def __init__(self, bundle: MODI, buffer: StringIO):
        super().__init__(daemon=True)
        self._buffer = buffer
        self.bundle = bundle
        self.__input_box = None
        self._modules = []
        self.__log = None
        self.__spec = None
        self.__curr_module = None
        self.__curr_cmd = None
        self.__tell = 0
        self.__query = None
        self.__sid, self.__did, self.__cmd, self.__data = \
            None, None, None, None

    def run(self) -> None:
        width, height = 900, 750
        window = Tk()
        window.title(f"PyMODI v{modi.__version__}")
        window.geometry(f"{width}x{height}")
        window.resizable(False, False)
        canvas = Canvas(window, width=width, height=height)
        canvas.create_rectangle(10, 60, 400, 340, outline='black')
        canvas.pack()

        Label(window, text='c:').place(x=10, y=5)
        self.__cmd = Entry(window)
        self.__cmd.place(x=25, y=5, width=40)

        Label(window, text='s:').place(x=80, y=5)
        self.__sid = Entry(window)
        self.__sid.place(x=95, y=5, width=40)
        Label(window, text='d:').place(x=150, y=5)
        self.__did = Entry(window)
        self.__did.place(x=165, y=5, width=40)
        Label(window, text='b:').place(x=220, y=5)
        self.__data = Entry(window)
        self.__data.place(x=235, y=5, width=500)
        Button(window, text="Generate", command=self.__parse).place(x=750, y=5)

        self.__input_box = Entry(window)
        self.__input_box.place(x=10, y=30, width=340)

        send_button = Button(window, text="Send", command=self.send)
        send_button.place(x=360, y=30)

        Label(window, text='command query: ').place(x=420, y=30)
        self.__query = Entry(window)
        self.__query.place(x=525, y=32, width=25)
        Button(window, text="Select", command=self.__change_query).place(
            x=555, y=30
        )

        self.__log = ScrolledText(window, wrap=WORD, font=('Helvetica', 12))
        self.__log.place(x=420, y=60, width=470, height=680)

        self.__spec = Label(window, text=f"PyMODI v{modi.__version__}",
                            bg='white', anchor=NW, justify='left',
                            font=('Helvetica', 10))
        self.__spec.place(x=10, y=350, width=400, height=390)

        for module in self.bundle._modules:
            self.__create_module_button(module, window)

        while True:
            try:
                window.update()
                self.__append_log()
                if self.__curr_module:
                    self.__change_spec(self.__curr_module)
            except TclError:
                break
            time.sleep(0.1)

    def __parse(self):
        try:
            cmd = eval(self.__cmd.get())
            sid = eval(self.__sid.get())
            did = eval(self.__did.get())
            data = eval(self.__data.get())
            msg = parse_message(cmd, sid, did, data)
            self.__input_box.delete(0, END)
            self.__input_box.insert(0, msg)
        except Exception:
            self.__input_box.delete(0, END)
            self.__input_box.insert(0, "Invalid Arguments")

    def __query_log(self, line: str) -> bool:
        if 'recv' not in line and 'send' not in line:
            return False
        if self.__curr_module \
                and str(self.__curr_module.id) not in line \
                and self.__curr_module.module_type != 'Network':
            return False
        if self.__curr_cmd and f'"c":{self.__curr_cmd},' not in line:
            return False
        return True

    def __change_query(self):
        self.__curr_cmd = self.__query.get()
        self.__update_log()

    def __update_log(self):
        self.__log.delete('0.0', END)
        log_text = self._buffer.getvalue()
        for line in log_text.split('\n'):
            if self.__query_log(line):
                self.__log.insert(INSERT, line + '\n')

    def __append_log(self):
        log_text = self._buffer.getvalue()
        new_text = log_text[self.__tell:]
        for line in new_text.split('\n'):
            if self.__query_log(line):
                self.__log.insert(INSERT, line + '\n')
            if line and 'send' not in line and 'recv' not in line:
                sys.__stdout__.write(line + '\n')
        self.__tell += len(new_text)
        self.__log.see(INSERT)

    def send(self):
        self.bundle.send(self.__input_box.get())

    def __change_spec(self, module):
        text = '\n'.join([f"Module Type: {module.module_type}",
                          f"Id: {module.id}",
                          f"UUID: {module.uuid}",
                          f"Version: {module.version}",
                          f"User Code: {module.has_user_code}",
                          f"Connected: {module.is_connected}"])
        text += '\n[Properties]\n'
        for prop in module._properties:
            text += f"{self.get_prop_name(prop, module)}: " \
                    f"{module._properties[prop].value} " \
                    f"last updated: " \
                    f"{module._properties[prop].last_update_time}\n"
        self.__spec.configure(text=text)

    @staticmethod
    def get_prop_name(prop, module):
        module_props = module.__class__.__dict__
        for prop_key in module_props:
            if prop == module_props[prop_key]:
                return prop_key
        return prop

    def __create_module_button(self, module, window):
        module_button = Button(window,
                               text=f"{module.module_type}\n({module.id})")
        module_type = str(module.__class__)
        if 'output' in module_type:
            color = '#fb973f'
        elif 'input' in module_type:
            color = '#9672f9'
        else:
            color = '#f3c029'
        module_button.configure(bg=color,
                                command=lambda: self.__change_module(module))
        module_button.place(x=170 + 60 * module.position[0],
                            y=180 - 40 * module.position[1],
                            width=60, height=40)
        self._modules.append(module_button)

    def __change_module(self, module):
        self.__curr_module = module
        self.__update_log()
