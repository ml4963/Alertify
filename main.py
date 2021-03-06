import urllib.request, requests
from bs4 import BeautifulSoup
import os

from twilio.rest import TwilioRestClient
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.button import Button

Contact_Book = []

def get_data():
    if os.path.exists("app_data.csv") == False:
        return
    else:
        with open("app_data.csv") as data_file:
            for line in data_file:
                # [name, phonenum, address, longitude, latitude]
                data_list = line.strip().split(",")
                Contact_Book.append(data_list)
        data_file.close()

def store_data():
    if os.path.exists("app_data.csv") == False:
        return
    else:
        file = open("app_data.csv", "a")
        file.write("\nsample, sample, sample, sample, sample")
        file.close()

Builder.load_string("""
<HomeScreen>:
	BoxLayout:
		orientation: "vertical"
		Image:
			size_hint_y: None
			height: root.height/2
			width: root.width/2
			source: "logo.png"
		Button:
			text: "View Contact"
			color: 0,0,0,1
			font_size:35
			pos_hint: {"x":.2, "y":.2}
			size_hint: .6 , .5
			background_color: 250,245,0,0.7
			on_press: root.manager.current = 'contacts'
		Button:
			text: "Alert"
			color: 0,0,0,1
			font_size: 35
			pos_hint: {"x":.2, "y":.2}
			size_hint: .6 , .5
			background_color: 250,245,0,0.7
			on_press: root.send_Alert()
		Button:
			text: "Setting"
			color: 0,0,0,1
			font_size: 35
			pos_hint: {"x":.2, "y":.2}
			size_hint: .6 , .5
			background_color: 250,245,0,0.7
			
			on_press: root.manager.current = 'setting'
	
<ContactScreen>:
	on_pre_enter: root.display_contacts()
	BoxLayout:
		orientation: "vertical"
		Image:
			size_hint_y: None
			height: root.height/4
			width: root.width/4
			source: "logo.png"
		Label:
			id: contact_info
			text: root.contacts
			font_size:15
			pos_hint: {"x":.2, "y":.2}
			size_hint: .6 , .5
			background_color: 250,245,0,0.7
		Button:
			text: "Add Contact"
			color: 0,0,0,1
			font_size: 15
			pos_hint: {"x":.2, "y":.1}
			size_hint: .6 , .03
			background_color: 255,0,0,0.8
		Button:
			text: "Back"
			color: 0,0,0,1
			font_size: 15
			pos_hint: {"x":.2, "y":.1}
			size_hint: .6 , .02
			background_color: 255,0,0,0.8
			
			on_press: root.manager.current = 'home'
	    
			
<SettingScreen>:
	BoxLayout:
		size_hint_y: None
		height: 250
		Label:
			text: "Set Radius"
		TextInput:
			id: tmp_radius
			text: root.curr_radius
		
	BoxLayout:
		orientation: "vertical"
		size_hint_y: None
		height: 50
		Button:
			background_color: (1.0, 0.0, 0.0, 1.0)
			text: "Save Changes"
			on_press: root.update_radius()
		Button:
			background_color: (1.0, 0.0, 0.0, 1.0)
			text: "Back"
			on_press: root.manager.current = 'home'
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
        client.messages.create(to="+xxxxxxxxxx", from_="+16464193165",
                                         body="Hello Ryan~!")
        return

class ContactScreen(Screen):
    contacts = ""
    def display_contacts(self, *args):
        text = ""
        for contact in Contact_Book:
            text += str(contact) + "\n"
        self.contacts= text
        self.ids.contact_info.text= self.contacts
        

class SettingScreen(Screen):
    curr_radius = "0"
    def update_radius(self, *args):
        self.curr_radius = self.ids.tmp_radius.text

# Add the screens
sm = ScreenManager()
sm.add_widget(HomeScreen(name = "home"))
sm.add_widget(ContactScreen(name = "contacts"))
sm.add_widget(SettingScreen(name = "setting"))

    # Getting location of user
def location_lookup():
    site = urllib.request.Request('https://geoiptool.com/', \
                              headers = {'User-Agent': 'Mozilla/5.0'})
    html_content = urllib.request.urlopen(site).read().decode('utf-8')
    site = BeautifulSoup(html_content, 'html.parser')

    longNum = str(longitude(site)) # makes string so it's sliceable 
    if '-' in longNum:
        longNum = longNum[6:14]
    else:
        longNum = longNum[6:13]
    
    latNum = str(latitude(site))
    if '-' in latNum:
        latNum = latNum[6:14]
    else:
        latNum = latNum[6:13]

    coordinate = [longNum, latNum]
    
    #20 is longitude
    #17 is latitude
    
    return(coordinate)
       
def longitude(site):
    i = 0
    for div_class in site.findAll('div', {'class':'data-item'}):
        for part in div_class.findAll('span'):
            i += 1
            if i == 20:
                return(part)

def latitude(site):
    i = 0
    for div_class in site.findAll('div', {'class':'data-item'}):
        for part in div_class.findAll('span'):
            i += 1
            if i == 18:
                return(part)

class AlertifyApp(App):

    def build(self):
        get_data()
        user_coordinate = location_lookup()       
        return sm

    coordinate = location_lookup()

AlertifyApp().run()
