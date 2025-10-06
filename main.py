from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.core.window import Window

class ControlScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        # Light control
        self.light_label = Label(text='Light: OFF', font_size=24)
        self.light_switch = Switch(active=False)
        self.light_switch.bind(active=self.on_light_toggle)
        self.add_widget(self.light_label)
        self.add_widget(self.light_switch)

        # Fan control
        self.fan_label = Label(text='Fan: OFF', font_size=24)
        self.fan_switch = Switch(active=False)
        self.fan_switch.bind(active=self.on_fan_toggle)
        self.add_widget(self.fan_label)
        self.add_widget(self.fan_switch)

        # Appliance control
        self.appliance_label = Label(text='Appliance: OFF', font_size=24)
        self.appliance_switch = Switch(active=False)
        self.appliance_switch.bind(active=self.on_appliance_toggle)
        self.add_widget(self.appliance_label)
        self.add_widget(self.appliance_switch)

    def on_light_toggle(self, instance, value):
        self.light_label.text = f'Light: {"ON" if value else "OFF"}'

    def on_fan_toggle(self, instance, value):
        self.fan_label.text = f'Fan: {"ON" if value else "OFF"}'

    def on_appliance_toggle(self, instance, value):
        self.appliance_label.text = f'Appliance: {"ON" if value else "OFF"}'

class SmartHomeAutomationApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background
        Window.size = (400, 700)  # Mobile size for testing
        return ControlScreen()

if __name__ == '__main__':
    SmartHomeAutomationApp().run()
