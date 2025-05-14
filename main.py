from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
import subprocess
import re
import os

def scan_wifi(interface="wlan0"):
    try:
        output = subprocess.check_output(["su", "-c", f"iwlist {interface} scan"], stderr=subprocess.DEVNULL).decode()
    except Exception as e:
        return [f"Xatolik: {e}"]

    cells = output.split("Cell ")
    networks = []
    for cell in cells[1:]:
        ssid = re.search(r'ESSID:"(.*?)"', cell)
        bssid = re.search(r'Address: ([\dA-F:]+)', cell)
        signal = re.search(r"Signal level=(-?\d+) dBm", cell)
        channel = re.search(r"Channel:(\d+)", cell)

        info = f"SSID: {ssid.group(1) if ssid else 'Yashirin'}\n" \
               f"BSSID: {bssid.group(1) if bssid else 'Noma’lum'}\n" \
               f"Signal: {signal.group(1)} dBm\n" if signal else "" \
               f"Kanal: {channel.group(1) if channel else 'Noma’lum'}\n"

        networks.append(info)
    return networks

class WifiScanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.label = Label(text="Wi-Fi tarmoqlarini ko‘rish uchun tugmani bosing", size_hint_y=None, height=100)
        self.add_widget(self.label)

        self.button = Button(text="Scan Wi-Fi", size_hint_y=None, height=60)
        self.button.bind(on_press=self.start_scan)
        self.add_widget(self.button)

        self.result_area = ScrollView()
        self.result_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.result_box.bind(minimum_height=self.result_box.setter('height'))
        self.result_area.add_widget(self.result_box)
        self.add_widget(self.result_area)

    def start_scan(self, instance):
        self.result_box.clear_widgets()
        self.label.text = "Scanning..."
        result = scan_wifi()
        for net in result:
            self.result_box.add_widget(Label(text=net, size_hint_y=None, height=150))
        self.label.text = f"Topildi: {len(result)} ta tarmoq"

class WifiApp(App):
    def build(self):
        return WifiScanner()

if __name__ == "__main__":
    WifiApp().run()
