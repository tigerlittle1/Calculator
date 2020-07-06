from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import  Window
from kivy.uix.gridlayout import GridLayout

class main_layout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.input_label = Label(text = "",text_size=(None,None),size_hint = (1,0.2),halign = 'right',markup= True)
        self.add_widget(self.input_label)

        self.button_layout = GridLayout(size_hint = (1,0.6))
        self.button_layout.cols = 4
        self.button_text = ["7","8","9","+","4","5","6","-","1","2","3","*","0",".","=","/","(",")"]
        self.button_list = []
        self.clear_button = Button(text = "C")
        self.back_button = Button(text="backspace")

        self.caculate_list = []
        self.temp = ""
        self.statue = "start"

        for i in range(18):
            self.button_list.append(Button(text =  self.button_text[i]))
            self.button_layout.add_widget(self.button_list[i])
            self.button_list[i].bind(on_press = self.button_call)

        self.button_layout.add_widget(self.clear_button)
        self.button_layout.add_widget(self.back_button)
        self.add_widget(self.button_layout)

        self.clear_button.bind(on_press = self.clear)
        self.back_button.bind(on_press=self.back_space)

    def button_call(self,instance):
        if self.statue == "start":
            self.input_label.text = ""
            self.statue = "ing"
        if instance.text == "=":
            if self.temp != "":
                self.caculate_list.append(self.temp)
                self.temp = ""
            self.input_label.text = str(self.caculate())
            self.caculate_list.clear()
            self.statue = "start"
        else:
            self.input_label.text += instance.text
            self.save_opt(instance.text)

    def clear(self,instance):
        self.input_label.text = ""
        self.caculate_list = []
        self.temp = ""

    def back_space(self,instance):
        self.input_label.text = self.input_label.text[:len(self.input_label.text)-1]
        if self.temp != "":
            self.temp = self.temp[:len(self.temp)-1]
        else:
            self.temp = self.caculate_list.pop()
            self.temp = self.temp[:len(self.temp) - 1]

    def save_opt(self, opt):
        print(opt)
        if len(self.input_label.text) == 1 and opt == "-":
            self.temp += opt
        elif opt == "+" or opt == "-" or opt == "*" or opt == "/" or opt == "(" or opt == ")":
            if self.temp != "":
                self.caculate_list.append(self.temp)
            self.caculate_list.append(opt)
            self.temp = ""
        else:
            self.temp += opt

    def caculate(self):
        print(self.caculate_list)
        output = self.procedure_postfix()
        ans_stack = []
        op_list = ["+","-","*","/"]
        for val in output:
            if val in op_list:
                b = ans_stack.pop()
                a = ans_stack.pop()
                if val == "+":
                    c = a + b
                    ans_stack.append(c)
                elif val == "-":
                    c = a - b
                    ans_stack.append(c)
                elif val == "*":
                    c = a * b
                    ans_stack.append(c)
                else:
                    c = a / b
                    ans_stack.append(c)
            else:
                ans_stack.append(float(val))

        return ans_stack[0]

    def procedure_postfix(self):
        op_stack = []
        output = []
        op_Priority = {"+": 1, "-": 1, "*": 2, "/": 2, "(": 0, ")": 3}

        for val in self.caculate_list:
            if op_Priority.get(val) == None:
                output.append(val)
            elif len(op_stack) != 0:
                if val == ")":
                    while True:
                        temp = op_stack.pop()
                        if temp != "(":
                            output.append(temp)
                        else:
                            break
                elif val == "(":
                    op_stack.append(val)
                else:
                    while op_Priority.get(val) <= op_Priority.get(op_stack[len(op_stack) - 1]):
                        temp = op_stack.pop()
                        if temp != "(":
                            output.append(temp)
                        if len(op_stack) == 0:
                            break
                    op_stack.append(val)
            else:
                op_stack.append(val)

        while len(op_stack) > 0:
            output.append(op_stack.pop())
        print(output)
        return output

class c(App):
    def build(self):
        return main_layout()

c().run()

