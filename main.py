import customtkinter as ctk
from settings import *
from tkinter import PhotoImage


def format_text(text: float, unit: str = ""):
    return f"{text:1>0.2f}{unit}"


class Frame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, fg_color=WHITE)


class Btn(ctk.CTkButton):
    def __init__(self, master=None, row=0, column=0, type='outer', **kwargs):
        px = 15 if type == 'outer' else 0
        py = 15 if type == 'outer' else 25
        super().__init__(master, **kwargs, fg_color=LIGHT_GRAY,
                         text_color=BLACK, hover_color=GRAY)
        self.grid(row=row, column=column, sticky='ns', pady=py, padx=px)


class Label(ctk.CTkLabel):
    def __init__(self, master, font_size=12, text="label", bold=False, **kwargs):
        font_style = ctk.CTkFont(FONT, font_size, 'bold' if bold else 'normal')
        super().__init__(master, font=font_style, text=text, **kwargs)

# weight input


class WeightFrame(Frame):
    def __init__(self, window, variable, system, **kwargs):
        super().__init__(window, **kwargs)
        self.grid(row=1, column=0, sticky='nsew', padx=13, pady=7)

        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 4), weight=2, uniform='b')
        self.columnconfigure((1, 3), weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')

        def _update_variable(dx):
            variable.set(max(variable.get()+dx, 1))
            _update_text()

        Btn(self, text='-', column=0, command=lambda: _update_variable(-1.0))
        Btn(self, text='-', column=1, type='inner',
            command=lambda: _update_variable(-0.1))

        display = Label(self, text="weight",
                        font_size=INPUT_TEXT_SIZE, text_color=BLACK)
        display.grid(row=0, column=2, sticky='nwes')

        Btn(self, text='+', column=3, type='inner',
            command=lambda: _update_variable(0.1))
        Btn(self, text='+', column=4, command=lambda: _update_variable(1.0))

        def _update_text(*_):
            _unit = 'Kg'
            if system.get() == 'Imperial':
                _unit = 'lb'
            display.configure(
                text=f"{format_text(variable.get())[:-1]}{_unit}")
        _update_text()

        def _convert_var(*_):
            multiplier = {'Imperial': 0.454, 'Metric': 2.203}
            variable.set(variable.get()*multiplier[system.get()])
            _update_text()

        system.trace_add('write', _convert_var)
# height input


class HeightFrame(Frame):
    def __init__(self, window, variable, system, **kwargs):
        super().__init__(window, **kwargs)
        self.grid(row=2, column=0, sticky='nsew', padx=13, pady=20)

        slider = ctk.CTkSlider(self, from_=100, to=300,
                               variable=variable, height=16, progress_color=(DARK_GREEN, DARK_GREEN), fg_color=(WHITE, WHITE))
        slider.place(relx=.05, rely=.4, relwidth=.6)

        display = Label(self, text="height",
                        font_size=SWITCH_TEXT_SIZE, text_color=BLACK)
        display.place(relx=.7, rely=.16, relwidth=.25)

        def _update_slider(*_):
            ranges = {'Imperial': (39, 120, 0.4),
                      'Metric': (100, 300, 2.5)}
            _f, _t, _c = ranges[system.get()]
            slider.configure(from_=_f)
            slider.configure(to=_t)
            variable.set(variable.get()*_c)

        def _update_text(*_):
            _divisor = 100
            _unit = 'm'
            if system.get() == 'Imperial':
                _divisor = 12
                _unit = 'ft'
            display.configure(text=format_text(variable.get()/_divisor, _unit))
        _update_text()

        variable.trace_add('write', _update_text)
        system.trace_add('write', lambda *_: _update_slider())

# window


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=GREEN)
        self.title('BMI Calculator')
        self.geometry('600x600')
        self.resizable(width=False, height=False)

        # icon
        self.iconphoto(False, PhotoImage(file='product_icon.png'))

        self.rowconfigure((1, 2), weight=1, uniform='a')
        self.rowconfigure(0, weight=3, uniform='a')
        self.columnconfigure(0, weight=1)

        # data and data_configuration
        self.mode = ctk.StringVar(value='Metric')
        self._weight = ctk.DoubleVar(value=60.0)
        self._height = ctk.IntVar(value=170)
        self._bmi = ctk.StringVar()
        self._update_bmi()
        self._weight.trace_add('write', self._update_bmi)
        self._height.trace_add('write', self._update_bmi)

        # widgets
        Label(self, MAIN_TEXT_SIZE, textvariable=self._bmi, text_color=(WHITE, WHITE)).grid(
            row=0, column=0, sticky='nsew')

        WeightFrame(self, self._weight, self.mode)
        HeightFrame(self, self._height, self.mode)

        def _change_mode(*_):
            self.mode.set('Imperial'if self.mode.get()
                          == 'Metric' else 'Metric')

        ctk.CTkButton(self, fg_color='transparent', hover_color=GREEN, text_color=DARK_GREEN, font=ctk.CTkFont(FONT, None),
                      textvariable=self.mode, command=_change_mode).place(rely=.04, relx=.8, relwidth=.2)

        self.mainloop()

    def _update_bmi(self, *args):
        _temp = format_text(self._weight.get()/(self._height.get()/100)**2)
        self._bmi.set(_temp)


App()
