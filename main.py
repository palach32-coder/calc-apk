from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle

Window.clearcolor = (0.05, 0.05, 0.05, 1)

class VaderCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.sound = SoundLoader.load('vader_breath.mp3')
        
        # Попытка программного ограничения громкости через системный API Android
        try:
            from jnius import autoclass
            Context = autoclass('android.content.Context')
            AudioManager = autoclass('android.media.AudioManager')
            # Получаем контекст активности для управления звуком
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            audio_manager = activity.getSystemService(Context.AUDIO_SERVICE)
            # Устанавливаем громкость на 30% от максимума (вместо 100%)
            max_vol = audio_manager.getStreamMaxVolume(AudioManager.STREAM_MUSIC)
            audio_manager.setStreamVolume(AudioManager.STREAM_MUSIC, int(max_vol * 0.3), 0)
        except:
            # Если не сработало (например, на других ОС), продолжаем работу
            if self.sound: self.sound.volume = 0.3
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(source='i.jpg', pos=self.pos, size=Window.size)
        
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.display = Label(
            text="0", font_size='60sp', size_hint_y=0.6, 
            halign='right', valign='top',
            text_size=(Window.width * 0.9, None)
        )
        self.add_widget(self.display)

        self.keyboard_box = BoxLayout(orientation='vertical', size_hint_y=0.4, padding=[10, 5, 10, 5], spacing=5)
        
        self.extended_grid = GridLayout(cols=3, size_hint_y=0.25, spacing=4)
        for f in ['^', '(', ')']:
            btn = Button(text=f, font_size='20sp', background_color=(0.3, 0.1, 0.1, 1))
            btn.bind(on_press=self.on_btn_press)
            self.extended_grid.add_widget(btn)

        self.main_grid = GridLayout(cols=4, spacing=5, size_hint_y=0.75)
        btns = ['AC', 'DEL', '%', '/', '7', '8', '9', '×', '4', '5', '6', '-', '1', '2', '3', '+', 'INV', '0', ',', '=']
        
        for text in btns:
            color = (0.6, 0.1, 0.15, 1) if text in ['/', '×', '-', '+', '='] else (0.2, 0.2, 0.2, 0.8)
            btn = Button(text=text, font_size='20sp', background_normal='', background_color=color)
            btn.bind(on_press=self.on_btn_press)
            self.main_grid.add_widget(btn)

        self.keyboard_box.add_widget(self.main_grid)
        self.add_widget(self.keyboard_box)

    def _update_bg(self, *args):
        self.bg.pos = (0, 0)
        self.bg.size = Window.size

    def adjust_font(self):
        txt = self.display.text
        if len(txt) > 20: self.display.font_size = '20sp'
        elif len(txt) > 12: self.display.font_size = '35sp'
        else: self.display.font_size = '60sp'

    def on_btn_press(self, instance):
        txt = instance.text
        if txt == 'INV':
            if self.extended_grid.parent is None: self.keyboard_box.add_widget(self.extended_grid, index=1)
            else: self.keyboard_box.remove_widget(self.extended_grid)
        elif txt == '=':
            current_text = self.display.text
            if any(op in current_text for op in ['+', '-', '×', '/', '^', '(', ')']):
                try:
                    expr = current_text.replace('×', '*').replace(',', '.').replace('^', '**')
                    if expr[-1] in ('+', '-', '*', '/', '.'): expr = expr[:-1]
                    res_val = eval(expr)
                    
                    if isinstance(res_val, float) and not res_val.is_integer():
                        res = "{:.4f}".format(res_val).rstrip('0').rstrip('.')
                    else:
                        res = str(int(res_val))
                    
                    if res != current_text:
                        self.display.text = res
                        if self.sound:
                            self.sound.stop()
                            self.sound.play()
                except Exception: self.display.text = "Error"
        elif txt == 'AC': self.display.text = '0'
        elif txt == 'DEL': self.display.text = self.display.text[:-1] if len(self.display.text) > 1 else '0'
        else:
            if self.display.text == '0' or self.display.text == "Error": self.display.text = txt
            else: self.display.text += txt
        self.adjust_font()

class VaderCalcApp(App):
    def build(self):
        return VaderCalculator()

if __name__ == '__main__':
    VaderCalcApp().run()
