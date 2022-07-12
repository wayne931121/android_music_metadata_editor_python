## <Wayne_931121_Inna>
## com.wayne931121.inna.music_metadata_editor
## This is a app for android.
# References:
# https://youtu.be/eR95woqouuc
# https://python-for-android.readthedocs.io/en/latest/apis/
# https://docs.python.org/zh-tw/3/library/re.html#re-syntax
# https://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement
# https://stackoverflow.com/questions/59006289/loading-images-from-internal-storage-kivy-python
# https://stackoverflow.com/questions/66219501/typeerror-kivy-weakproxy-weakproxy-object-is-not-callable
# https://stackoverflow.com/questions/56148252/how-to-use-windows-default-file-browser-in-kivy-app
# https://gist.github.com/rnixx/c60a744576866a7f1a42
# Refresh Android Media Store:
# https://stackoverflow.com/questions/72586638/downloaded-files-not-appearing-in-the-downloads-application-in-android-kivy
# https://developer.android.com/reference/android/content/Intent
# https://pyjnius.readthedocs.io/en/stable/android.html
# https://stackoverflow.com/questions/3572463/what-is-context-on-android
# https://developer.android.com/reference/android/content/Context
# https://developer.android.com/reference/android/content/package-summary
# https://stackoverflow.com/questions/4646913/android-how-to-use-mediascannerconnection-scanfile
# https://codertw.com/android-%E9%96%8B%E7%99%BC/331396/
# https://segmentfault.com/a/1190000014593444
# https://stackoverflow.com/questions/69054442/kivy-python-android-app-why-downloaded-video-from-any-website-are-not-showing-in
# https://stackoverflow.com/questions/54442336/using-mediastore-in-kivy-with-pyjnius
# https://developer.android.com/reference/android/provider/MediaStore
# https://stackoverflow.com/questions/3300137/how-can-i-refresh-mediastore-on-android
# https://stackoverflow.com/questions/60203353/action-media-scanner-scan-filestring-is-deprecated/63413716
# https://www.google.com/search?q=Android+Media+Storage
# https://www.google.com/search?q=Android%20rescan%20media
import os
import re
import sys
import time
import eyed3
import random
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
if platform=="win":
    Window.size = (1080*0.45, 2004*0.45)
from kivy.core.clipboard import Clipboard
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import *

# kivy v2.1.0
# Python v3.9.12

Builder.load_string("""
<Debug>
    TextInput:
        height: self.minimum_height
        size_hint: 1, None
        text: root.error
""")
path = os.getcwd()
delay = 0.01
error = ""
debug = True
AndroidPath = ""
font = "assets/kaiu.ttf"
Bt1Font = "assets/msgothic.ttc"
none = "assets/none.png"
hidden = {"right":-1}
Textinputs = {}

# # https://stackoverflow.com/questions/43666381/wrapping-the-text-of-a-kivy-label
# https://kivy.org/doc/stable/api-kivy.properties.html

# In kv file can't use this class, only in python can use.(P)
class P(FloatLayout):
    def __init__(self, flag=1, **kargs):
        super().__init__(**kargs) # kargs input by kv file
        if flag:
            self.l = self.ids.l 

# In kv file can use this class(P1)
class P1(P):
    def __init__(self, **kargs):
        super().__init__(flag=0, **kargs) # kargs input by kv file

class FCB(FloatLayout):
    def __init__(self, label_text, button_color, on_click, **kargs):
        self.label_text = label_text
        self.display_text = "　"+label_text # 解決中文對齊問題
        self.button_color = button_color
        self.on_click = on_click
        super().__init__(**kargs) # kargs input by kv file
        self.b = self.ids.b
        self.l = self.ids.l
        self.background_normal = self.b.background_normal
        self.background_down = self.b.background_down
    def reset(self, label_text, button_color, on_click):
        self.label_text = label_text
        self.display_text = "　"+label_text
        self.button_color = button_color
        self.b.ttext = label_text
        self.b.background_color = button_color
        self.b.background_normal = self.background_normal
        self.b.background_down = self.background_down
        self.l.text = self.display_text
        self.on_click = on_click
        self.size_hint = (1, 0.07)
    def hidden(self):
        self.size_hint = (0, 0)
        self.b.background_normal = service.none
        self.b.background_down = service.none

class Filechooser(Screen):
    def __init__(self, **kargs):   # kv language will give some arg to here, so you must use **kargs.
        super().__init__(**kargs)  # If you don't use,it will cause this error: got an unexpected keyword argument '__no_builder'
        self.root_path = AndroidPath if platform=="android" else os.getcwd() #"C://" if platform=="win" else os.getcwd()
        self.root_path = self.root_path.replace("\\", "/")
        self.FontSize = Window.width*0.055
        self.fifters = ["mp3"]
        self.selection = ""
        self.buttons = []
        for k in self.ids.keys():
            exec("self.{0} = self.ids.{0}".format(k))
        for k in self.ControlBar.ids.keys():
            exec("self.{0} = self.ControlBar.ids.{0}".format(k))
        self.select_bar.canvas.before.children[0].rgba = (0,0,0,0.3)
        self.fc_open.pos_hint = hidden
        self.vpath = P()
        self.t2b.add_widget(self.vpath)
        self.ControlBar.remove_widget(self.select_bar)
        if platform!="android":
            self.service = Clock.schedule_interval(self.on_hover, 0.01)
        self.set_files(self.root_path)
    def on_hover(self, *args):
        result = self.ids.FC.to_local(*service.mouse_pos())
        for i in self.buttons: 
            if i.b.collide_point(*result):
                i.b.background_color = (1,1,1,1)
            else:
                i.b.background_color = i.button_color
    def back(self, *args):
        path = "/".join(self.path.split("/")[:-1])
        if path=="C:/": path=self.root_path
        self.enter_path()
        self.set_files(path)
    def enter(self, *args):
        opath = self.path
        path = os.path.join(self.path, args[0].ttext).replace("\\", "/")
        try: #防止進入受保護資料夾權限不足而出錯
            self.enter_path()
            self.set_files(path)
        except:
            self.set_files(opath)
    def enter_path(self):
        self.vpath.canvas.after.children[0].rgba = (0,0,0,0)
        self.fc_open.pos_hint = hidden
        try:
            self.ControlBar.remove_widget(self.select_bar)
        except:
            pass
    def selected(self, *args):
        self.vpath.canvas.after.children[0].rgba = (0,0,0,1)
        self.selection = os.path.join(self.path, args[0].ttext).replace("\\", "/")
        self.select_bar.ids.l.text = self.selection
        self.fc_open.pos_hint = self.fc_open.fpos_hint
        try:
            self.ControlBar.add_widget(self.select_bar)
        except:
            pass
    # https://www.runoob.com/python/python-os-path.html
    def sort_by_date(self, file):
        return os.path.getmtime(os.path.join(self.path, file))
    def set_files(self, path):
        tpath = path
        self.path = path
        for w in list(range(len(self.buttons)))[::-1]: self.t2b.remove_widget(self.buttons.pop(w))
        if not(path==self.root_path):
            tpath = path.replace("\\", "/").split("/")
            if tpath[-2]=="": tpath[-2]=self.root_path
            tpath = tpath[-2]+" > "+tpath[-1]
            self.append("..", (1,1,1,0.9), self.back)
        self.vpath.ids.l.text = tpath
        path, folders, files = next(os.walk(path))
        folders.sort(key=self.sort_by_date)
        files.sort(key=self.sort_by_date)
        for e in folders[::-1]:
            if e[0:1]!=".":
                self.append(e, (1,1,1,0.9), self.enter)
        for e in files[::-1]:
            if (e.split(".")[-1] in self.fifters) and e[0:1]!=".":
                self.append(e, (1,1,1,0.7), self.selected)
    def append(self, *args):
        button = FCB(*args)
        self.buttons.append(button)
        self.t2b.add_widget(button)
    def Open(self):
        service.sm.switch_to(service.Edit, direction='left')
        service.Edit.ids.scroll.scroll_y = 1
        service.Edit.load()

class Imagechooser(Filechooser):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.fifters = ["jpg", "jpeg", "png"]
        self.set_files(self.root_path)
        # https://stackoverflow.com/questions/17501122/how-to-unbind-a-property-automatically-binded-in-kivy-language
        self.ControlBar.remove_widget(self.fc_back)
        self.ControlBar.fc_back_run = lambda:Clock.schedule_once(lambda *args:service.sm.switch_to(service.screens[2], direction='left'))
        self.ControlBar.add_widget(self.fc_back)
    def Open(self):
        service.sm.switch_to(service.screens[2], direction='left')
        service.screens[2].fn = self.selection
        service.screens[2].rm = False
        service.screens[2].ids.img.source = service.screens[2].fn

class Ap(Screen):
    def __init__(self, **kargs):
        self.text = AndroidPath
        self.FontSize = Window.width*0.055
        self.w = Window.width
        self.h = Window.height
        super(Ap, self).__init__(**kargs)
        return

class Done(Screen):
    pass

class Edit(Screen):
    def __init__(self, **kargs):
        self.none = f("assets/none.png")
        self.fn = self.none #Audio Image
        self.rm = False
        super().__init__(**kargs)
        self.target = "" #Audio Name
        Textinputs["Date:"].hint_text = "YYYY-MM-DD/HH:MM:SS"
        return
    def load(self):
        global f
        self.target = service.FC.selection
        self.target = self.target.replace("\\", "/")
        mp3 = eyed3.load(self.target)
        images = list(mp3.tag.images)
        self.image = 0
        self.images = images
        self.cache = self.none
        for e in images:
            if e.picture_type==3:
                self.cache = f("assets/%s.%s"%(time.time(),e.mime_type.split("\\")[-1].split("/")[-1])).replace("\\","/")
                self.image = e
                with open(self.cache, "wb") as f1:
                    f1.write(e.image_data)
                break
        if self.cache==self.none:
            for e in images:
                self.cache = f("assets/%s.%s"%(time.time(),e.mime_type.split("\\")[-1].split("/")[-1])).replace("\\","/")
                self.image = e
                with open(self.cache, "wb") as f1:
                    f1.write(e.image_data)
                break
        self.ids.img.source = self.cache
        if self.cache!= self.none:
            os.remove(self.cache)
        Textinputs["Album:"].text = "" if mp3.tag.album==None else mp3.tag.album
        Textinputs["Title:"].text = "" if mp3.tag.title==None else mp3.tag.title
        Textinputs["Artist:"].text = "" if mp3.tag.artist==None else mp3.tag.artist
        Textinputs["Album Artist:"].text = "" if mp3.tag.album_artist==None else mp3.tag.album_artist
        Textinputs["Track Number:"].text = "" if mp3.tag.track_num[0]==None else str(mp3.tag.track_num[0])
        Textinputs["Date:"].text = "" if mp3.tag._getDate(b"TIME")==None else mp3.tag._getDate(b"TIME").replace("T", "/")
    def download_image(self):
        if self.cache!=self.none and os.path.isfile(self.target):
            folder = "/".join(self.target.split("/")[:-1])
            for e in self.images:
                cache = os.path.join(folder, "Album Cover %s %s.%s"%(e.picture_type,
                                                                     time.time(),
                                                                     e.mime_type.split("\\")[-1].split("/")[-1])).replace("\\","/")
                with open(cache, "wb") as f1:
                     f1.write(e.image_data)
                service.android_rescan_MediaStore(cache)
    def remove_image(self):
        self.fn = self.none
        self.rm = True
        self.ids.img.source = self.fn
    def add_image(self):
        service.sm.switch_to(service.screens[3], direction='right')
    def save(self):
#         fn = self.target.split(".")
#         ftype = fn[-1]
#         filename = ".".join(fn[:-1])
#         prefix = "edited%05d"%int(random.random()*10000)
#         #You can't use shutil.copy in android, or caused some error.
#         with open(self.target, "rb") as old_audio:
#             old_audio_data = old_audio.read()
#         if re.match("edited\d{5}", filename.split("_")[-1])!=None: #如果這是經編輯器處理過的音樂
#             if os.path.isfile(self.target): #防刪錯檢查
#                 os.remove(self.target) #移除舊的，經編輯器處理過的音樂
#             filename = "_".join(filename.split("_")[:-1])
#         else:
#             os.rename(self.target, filename+"_original."+ftype)
#         filename = filename+"_%s."%prefix+ftype #更新檔名防止音樂檢視器未刷新檔案
#         with open(filename, "wb") as new_audio:
#             new_audio.write(old_audio_data)
#         mp3 = eyed3.load(filename)
        mp3 = eyed3.load(self.target)
        mp3.initTag(version=(2, 3, 0))
        mp3.tag.artist = Textinputs["Artist:"].text
        mp3.tag.album = Textinputs["Album:"].text
        mp3.tag.album_artist = Textinputs["Album Artist:"].text
        mp3.tag.title = Textinputs["Title:"].text
        file = self.fn 
        images = list(mp3.tag.images)
        image_type = 3
        if Textinputs["Track Number:"].text!="":
            mp3.tag.track_num = int(Textinputs["Track Number:"].text)
        if self.rm:
            pass
        elif self.fn!=self.none: #使用者已選取圖片
            mime_type = "image/jpeg" if file.split(".")[-1]=="jpg" or file.split(".")[-1]=="jpeg" else "image/png"
            for e in images:
                if e.picture_type==image_type:
                    mp3.tag.images.remove(e.description)
            with open(self.fn, "rb") as img:
                data = img.read()
            mp3.tag.images.set(image_type, data, mime_type=mime_type, description="Music Editor Edited")
        else:
            if self.image:
                for e in self.images:
                    mp3.tag.images.set(e.picture_type, e.image_data, mime_type=e.mime_type, description=e.description)
        date = Textinputs["Date:"].text
        date = date.replace("/", "T")
        final_time = ""
        TIME, TDAT, TYER = [""]*3
        if date!="":
            if re.match("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", date)!=None:
                TIME = re.match("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", date).group()
                TDAT = date.split("T")[0]
                TYER = date.split("-")[0]
            elif re.match("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", date)!=None:
                TIME = re.match("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", date).group()
                TDAT = date.split("T")[0]
                TYER = date.split("-")[0]
            elif re.match("\d{4}-\d{2}-\d{2}T\d{2}", date)!=None:
                TIME = re.match("\d{4}-\d{2}-\d{2}T\d{2}", date).group()
                TDAT = date.split("T")[0]
                TYER = date.split("-")[0]
            elif re.match("\d{4}-\d{2}-\d{2}", date)!=None:
                TDAT = re.match("\d{4}-\d{2}-\d{2}", date).group()
                TYER = date.split("-")[0]
            elif re.match("\d{4}", date)!=None:
                TYER = re.match("\d{4}", date).group()
            if TIME!="": mp3.tag._setDate(b"TIME", TIME)
            if TDAT!="": mp3.tag._setDate(b"TDAT", TDAT)
            if TYER!="": mp3.tag._setDate(b"TYER", TYER); mp3.tag.recording_date = TYER
            if TIME!="":
                final_time = TIME
            elif TDAT!="":
                final_time = TDAT
            elif TYER!="":
                final_time = TYER
            mp3.tag.release_date = final_time
        mp3.tag.save(encoding="utf-8")
        service.android_rescan_MediaStore(self.target)
        service.screens[4].ids.ML.text = "處理完成！"
    def run_save(self):
        service.sm.switch_to(service.screens[4], direction="left")
        #try:
        #    self.save()
        #except:
        #    service.screens[4].ids.ML.text = "處理失敗！"
        self.save()
        service.screens[1].set_files(service.screens[1].path)
    def stored(self):
        if self.target!="":
            Clock.schedule_once(lambda *args:self.run_save())

class Debug(StackLayout):
    def __init__(self, err):
        self.error=err
        super().__init__()

class MyApp(App):
    def __init__(self, error=""):
        self.error = error
        if self.error!="":
            self.reset()
            self.build = lambda: Debug(self.error)
        # 所有錯誤都會在這行後才會被顯示
        super().__init__()
    def build(self):
        global ttext, root
        self.android_init()
        self.font = f(font)
        self.Bt1Font = f(Bt1Font)
        self.none = f(none)
        self.kv = f("assets/App.kv")
        self.root = Builder.load_file(self.kv)
        if platform=="win":
            self.icon = f("assets/ic.png")
        self.title = "Mp3 Metadata Editor"
        self.height = Window.height
        self.width = Window.width
        self.Clock = Clock
        self.Globals = Globals
        self.mouse_pos = lambda:Window.mouse_pos
        self.FC = Filechooser(name='FC')
        self.IFC = Imagechooser(name='IFC')
        self.MAIN = Ap(name='Ap')
        self.Edit = Edit(name="Edit")
        self.Done = Done(name="Done")
        # 這裡self.screens會指向原物件，原物件改了它也會改。
        self.screens = [self.MAIN, self.FC, self.Edit, self.IFC, self.Done]
        self.sm = ScreenManager()
        self.sm.switch_to(self.screens[0])
        self.copy_paste_manager = copy_paste_manager()
        return self.sm
    def android_init(self):
        if platform=="android":
            global AndroidPath
            from jnius import autoclass, cast
            from android.storage import app_storage_path
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            #SERVICE_NAME = 'com.wayne931121.inna.music.ServiceWayne'
            #service = autoclass(SERVICE_NAME)
            #self.mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            #argument = ""
            #service.start(self.mActivity, argument)
            #self.service = service
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            AndroidActivityInfo = autoclass('android.content.pm.ActivityInfo')
            activity = PythonActivity.mActivity
            activity.setRequestedOrientation(AndroidActivityInfo.SCREEN_ORIENTATION_PORTRAIT)
            currentActivity = cast('android.app.Activity', activity)
            File = autoclass('java.io.File')
            Uri = autoclass('android.net.Uri')
            Intent = autoclass('android.content.Intent')
            currentApplication = currentActivity.getApplicationContext()
            Context = cast('android.content.Context', currentApplication)
            MediaStore = cast('android.provider.MediaStore', currentApplication)
            self.PythonActivity = PythonActivity
            self.activity = PythonActivity.mActivity
            self.currentActivity = currentActivity
            self.File = File
            self.Uri = Uri
            self.Intent = Intent
            self.Context = Context
            self.MediaStore = MediaStore
            self.MediaScannerConnection = autoclass('android.media.MediaScannerConnection')
            caf = 1
            while caf:
                try :
                    from android.storage import primary_external_storage_path
                    AndroidPath = primary_external_storage_path()
                    try:
                        os.listdir(AndroidPath)
                        caf = 0
                    except:
                        pass
                except :
                    AndroidPath = "Get Path Failed"
    def android_rescan_MediaStore(self, file):
        if platform=="android":
            #file = self.Uri.fromFile(self.File(file))
            #mediaScanIntent = self.Intent(self.Intent.ACTION_MEDIA_SCANNER_SCAN_FILE, file)
            #self.Context.sendBroadcast(mediaScanIntent)
            self.MediaScannerConnection.scanFile(self.Context, [file], None, None)
        return
    def reset(self):
        self.on_pause, self.on_start, self.on_resume = [lambda:1]*3
        self.on_stop = self.stop_debug
    def stop_debug(self):
        global debug; debug = False; return None;
    def stop_service(self):
        if platform == "android":
            pass #self.service.stop(self.mActivity);
        else:
            self.FC.service.cancel();
    def on_pause(self):
        for e in Textinputs.keys():
            Textinputs[e].focus = False
        return True
    def on_resume(self):
        pass
    def on_start(self):
        pass
    def on_stop(self):
        self.stop_debug()
        self.stop_service()
    def on_text(self, TextinputObject):
        if "\n" in TextinputObject.text:
            TextinputObject.text = TextinputObject.text.replace("\n", "")
    def register(self, Description, Object):
        global Textinputs
        if Description!="":
            Textinputs[Description] = Object

class copy_paste(FloatLayout):
    pass

class copy_paste_manager():
    def __init__(self):
        self.relative = service.Edit.ids.scroll #self relative layout to use to_local(*touch.pos)
        self.target = service.Edit.ids.fly #will add element in it
        self.widget = copy_paste()
        self.bubb = self.widget.ids.wg
        self.textinput = None
        self.added = False
        Window.bind(on_touch_down=self.on_touch_down)
        super().__init__()
    def remove(self):
        self.added = False
        self.target.remove_widget(self.widget)
    def event_pos_in_target_element(self, pos):
        for e in Textinputs.items():
            if e[1].collide_point(*pos):
                return e[1]
        return False
    def copy(self):
        Clock.schedule_once(lambda *args:self.inner_copy())
    def paste(self):
        Clock.schedule_once(lambda *args:self.inner_paste())
    def inner_copy(self):
        Textinput = self.textinput
        text = ""
        if Textinput.selection_text!="":
            text = Textinput.selection_text
        else:
            text = Textinput.text
        Clipboard.copy(text)
    def inner_paste(self):
        self.textinput.insert_text(Clipboard.paste())
    def on_touch_down(self, self1, touch):
        if service.sm.current=="Edit":
            pos = self.relative.to_local(*touch.pos)
            if not self.added: #如果元件尚未加進去
                if touch.is_double_tap: #如果是雙次點擊
                    result = self.event_pos_in_target_element(pos)
                    if result:
                        self.added = True
                        self.textinput = result
                        self.widget.pos_hint = {}
                        self.target.add_widget(self.widget)
                        self.widget.pos = pos
            elif self.bubb.collide_point(*pos): #如果正在點擊自身按鈕
                pass
            else: #如果元件已加進去
                if not touch.is_double_tap:
                    self.remove() 
                else:
                    result = self.event_pos_in_target_element(pos)
                    if result:
                        self.widget.pos = pos
                    else:
                        self.remove()


def Globals():
    return globals()

def f(file):
    global path
    print()
    print(os.path.join(path, file))
    print()
    return os.path.join(path, file)

if platform=="win":
    try:
        sys._MEIPASS
        path = sys._MEIPASS
    except:
        pass

if __name__ == '__main__':
    while debug:
        try:
            service = MyApp(error)
            service.run()
        except Exception as err:
            error += str(err)+"\n"
    if error!="": print(error)