from twilio.rest import TwilioRestClient
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.button import Button

Builder.load_string("""
<HomeScreen>:
	BoxLayout:
		orientation: "vertical"
		Label:
			text: "Alert!fy"
			font_size: 80
		Button:
			text: "View Contact"
			height: 80
			on_press: root.manager.current = 'contacts'
		Button:
			text: "Alert"
			on_press: root.send_Alert()
		Button:
			text: "Setting"
			on_press: root.manager.current = 'settings'
	
<ContactScreen>:
	BoxLayout:
		orientation: "vertical"
		Button:
		Button:
<SettingScreen>:
	BoxLayout:
		orientation: "vertical"
		Button:
		Button:
""")

# Set up the screens
class HomeScreen(Screen):
    '''
    (From the twilio program)
    function to send out alerts to the destination
    '''
    def send_Alert(self, *args):
        account_sid = "ACbb4b9650631364e99781ded800fa9699" 
        auth_token = "0a068601c149167e134887defd6fc2a9" 
        client = TwilioRestClient("ACbb4b9650631364e99781ded800fa9699", \
                              "0a068601c149167e134887defd6fc2a9")
        client.messages.create(to="+19176671977", from_="+16464193165",
                                         body="Hello Jia~!")
        return

class ContactScreen(Screen):
    pass

class SettingScreen(Screen):
    pass

# Add the screens
sm = ScreenManager()
sm.add_widget(HomeScreen(name = "home"))
sm.add_widget(ContactScreen(name = "contacts"))
sm.add_widget(SettingScreen(name = "setting"))

#The functions to switch screen to "contacts"
def view_Contacts(obj):
    #App proceeds to next page
    pass

# Function to switch screen to "functions"
def to_setting(obj):
    pass


class AlertifyApp(App):
    def build(self):
        return sm

AlertifyApp().run()
