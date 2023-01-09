from kivy.app import App
from kivy.graphics import Line, Color
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from threading import Thread
from ploter import Ploter
from kivy.clock import Clock

class Screen(Widget):
    def __init__(self, ploter):
        super().__init__()

        self.ploter = ploter
        self.vector = (0, 0)
        self.new_vector = (0, 0)
        self.rgba = ploter.rgba

        Clock.schedule_interval(self.update, 0)

    def update(self, event):
        self.draw = ploter.draw
        self.rgba = ploter.rgba
        if self.draw:
            self.new_vector = (self.ploter.x, self.ploter.y)
            self.draw_line()

    def draw_line(self):
        with self.canvas:
            self.colo = Color()
            self.colo.rgba = self.rgba
            x = self.vector[0]/10
            y = self.vector[1]/10
            Line(points = [x, y, self.new_vector[0]/10, self.new_vector[1]/10])
            self.vector = self.new_vector

class MyApp(App):
    def build(self):
        self.screen = Screen(ploter)
        return self.screen

if __name__ == '__main__':
    ploter = Ploter('logo.gcode')
    thread = Thread(target = ploter.mainloop)
    thread.start()
    myapp = MyApp()
    myapp.run()
