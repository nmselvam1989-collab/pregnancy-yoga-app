# -*- coding: utf-8 -*-
"""
கர்ப்பகால யோகா - Pregnancy Yoga (Tamil)
A simple Kivy app: home screen lists safe pregnancy yoga poses,
detail screen shows Tamil instructions + a countdown timer.
"""

import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty

from data import EXERCISES, DISCLAIMER_TA

# ---------------------------------------------------------------------------
# Tamil font registration
# ---------------------------------------------------------------------------
# Android's default Kivy font does NOT render Tamil glyphs. You must supply a
# Tamil-capable TTF (e.g. "Noto Sans Tamil") at:
#     assets/fonts/NotoSansTamil-Regular.ttf
# Download it free from Google Fonts: https://fonts.google.com/noto/specimen/Noto+Sans+Tamil
FONT_PATH = os.path.join(os.path.dirname(__file__), "assets", "fonts", "NotoSansTamil-Regular.ttf")
FONT_NAME = "TamilFont"

if os.path.exists(FONT_PATH):
    LabelBase.register(name=FONT_NAME, fn_regular=FONT_PATH)
else:
    # Falls back to default font (Tamil text will show as boxes/blanks
    # until you add the .ttf file above).
    FONT_NAME = "Roboto"

Window.clearcolor = (0.98, 0.95, 0.97, 1)

PRIMARY = (0.55, 0.27, 0.55, 1)   # soft purple
ACCENT = (0.95, 0.65, 0.55, 1)    # soft coral
TEXT_DARK = (0.2, 0.15, 0.2, 1)


def tamil_label(text, font_size=18, bold=False, color=TEXT_DARK, **kwargs):
    return Label(
        text=text,
        font_name=FONT_NAME,
        font_size=dp(font_size),
        bold=bold,
        color=color,
        markup=True,
        **kwargs
    )


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))

        title = tamil_label(
            "கர்ப்பகால யோகா", font_size=26, bold=True,
            color=PRIMARY, size_hint_y=None, height=dp(50)
        )
        subtitle = tamil_label(
            "பாதுகாப்பான பயிற்சிகளைத் தேர்ந்தெடுக்கவும்",
            font_size=15, size_hint_y=None, height=dp(30)
        )
        root.add_widget(title)
        root.add_widget(subtitle)

        scroll = ScrollView()
        list_box = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        list_box.bind(minimum_height=list_box.setter("height"))

        for ex in EXERCISES:
            btn = Button(
                text=f"{ex['name_ta']}\n({ex['duration']} வி.)",
                font_name=FONT_NAME,
                font_size=dp(16),
                halign="left",
                size_hint_y=None,
                height=dp(64),
                background_color=ACCENT,
                background_normal="",
                color=(1, 1, 1, 1),
            )
            btn.bind(size=lambda w, *a: setattr(w, "text_size", (w.width - dp(20), None)))
            btn.bind(on_release=lambda inst, ex_id=ex["id"]: self.open_exercise(ex_id))
            list_box.add_widget(btn)

        scroll.add_widget(list_box)
        root.add_widget(scroll)

        info_btn = Button(
            text="எச்சரிக்கை குறிப்பு",
            font_name=FONT_NAME,
            size_hint_y=None,
            height=dp(44),
            background_color=PRIMARY,
            background_normal="",
        )
        info_btn.bind(on_release=self.show_disclaimer)
        root.add_widget(info_btn)

        self.add_widget(root)

    def open_exercise(self, ex_id):
        self.manager.get_screen("exercise").load_exercise(ex_id)
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "exercise"

    def show_disclaimer(self, *args):
        content = tamil_label(DISCLAIMER_TA, font_size=15)
        content.text_size = (dp(280), None)
        popup = Popup(title="குறிப்பு", content=content, size_hint=(0.85, 0.5))
        popup.open()


class ExerciseScreen(Screen):
    remaining = NumericProperty(0)
    timer_text = StringProperty("00:00")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.exercise = None
        self._event = None

        self.root_box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        self.add_widget(self.root_box)

    def load_exercise(self, ex_id):
        self.exercise = next(e for e in EXERCISES if e["id"] == ex_id)
        self.remaining = self.exercise["duration"]
        self._render()

    def _render(self):
        self.root_box.clear_widgets()

        back_btn = Button(
            text="< பட்டியலுக்குத் திரும்பு",
            font_name=FONT_NAME,
            size_hint_y=None,
            height=dp(40),
            background_color=PRIMARY,
            background_normal="",
        )
        back_btn.bind(on_release=self.go_back)
        self.root_box.add_widget(back_btn)

        name = tamil_label(
            self.exercise["name_ta"], font_size=22, bold=True,
            color=PRIMARY, size_hint_y=None, height=dp(60)
        )
        name.text_size = (Window.width - dp(24), None)
        self.root_box.add_widget(name)

        scroll = ScrollView()
        steps_box = BoxLayout(orientation="vertical", spacing=dp(6), size_hint_y=None)
        steps_box.bind(minimum_height=steps_box.setter("height"))

        for i, step in enumerate(self.exercise["steps_ta"], start=1):
            lbl = tamil_label(f"{i}. {step}", font_size=16, size_hint_y=None)
            lbl.bind(width=lambda w, *a: setattr(w, "text_size", (w.width, None)))
            lbl.bind(texture_size=lambda w, ts: setattr(w, "height", ts[1] + dp(10)))
            steps_box.add_widget(lbl)

        benefit = tamil_label(
            "நன்மை: " + self.exercise["benefit_ta"],
            font_size=15, size_hint_y=None
        )
        benefit.bind(width=lambda w, *a: setattr(w, "text_size", (w.width, None)))
        benefit.bind(texture_size=lambda w, ts: setattr(w, "height", ts[1] + dp(10)))
        steps_box.add_widget(benefit)

        scroll.add_widget(steps_box)
        self.root_box.add_widget(scroll)

        self.timer_label = tamil_label(
            self._format_time(self.remaining), font_size=36, bold=True,
            color=ACCENT, size_hint_y=None, height=dp(60)
        )
        self.root_box.add_widget(self.timer_label)

        controls = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        start_btn = Button(text="தொடங்கு", font_name=FONT_NAME,
                            background_color=PRIMARY, background_normal="")
        start_btn.bind(on_release=self.start_timer)
        reset_btn = Button(text="மீட்டமை", font_name=FONT_NAME,
                            background_color=ACCENT, background_normal="")
        reset_btn.bind(on_release=self.reset_timer)
        controls.add_widget(start_btn)
        controls.add_widget(reset_btn)
        self.root_box.add_widget(controls)

    @staticmethod
    def _format_time(seconds):
        m, s = divmod(max(0, int(seconds)), 60)
        return f"{m:02d}:{s:02d}"

    def start_timer(self, *args):
        if self._event:
            return
        self._event = Clock.schedule_interval(self._tick, 1)

    def _tick(self, dt):
        self.remaining -= 1
        self.timer_label.text = self._format_time(self.remaining)
        if self.remaining <= 0:
            self._event.cancel()
            self._event = None
            self.timer_label.text = "முடிந்தது!"

    def reset_timer(self, *args):
        if self._event:
            self._event.cancel()
            self._event = None
        self.remaining = self.exercise["duration"]
        self.timer_label.text = self._format_time(self.remaining)

    def go_back(self, *args):
        if self._event:
            self._event.cancel()
            self._event = None
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "home"


class PregnancyYogaApp(App):
    def build(self):
        self.title = "கர்ப்பகால யோகா"
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ExerciseScreen(name="exercise"))
        return sm


if __name__ == "__main__":
    PregnancyYogaApp().run()
