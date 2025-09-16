from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import json

# Data storage (in-memory for demo)
users = []
products = []
negotiations = []
transactions = []

# Mock data
govt_schemes = [
    {'name': 'PM-KISAN', 'description': 'Direct income support to farmers', 'link': 'https://pmkisan.gov.in/'},
    {'name': 'Pradhan Mantri Fasal Bima Yojana', 'description': 'Crop insurance scheme', 'link': 'https://pmfby.gov.in/'},
]
market_prices = {'wheat': 2000, 'rice': 1800, 'maize': 1500}

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        self.message = Label(text='')
        login_btn = Button(text='Login')
        login_btn.bind(on_press=self.login)
        register_btn = Button(text='Register')
        register_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'register'))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_btn)
        layout.add_widget(register_btn)
        layout.add_widget(self.message)
        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            self.manager.current = 'home'
            self.manager.get_screen('home').set_user(user)
        else:
            self.message.text = 'Invalid credentials'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        self.role_input = TextInput(hint_text='Role (farmer/buyer)', multiline=False)
        self.message = Label(text='')
        register_btn = Button(text='Register')
        register_btn.bind(on_press=self.register)
        back_btn = Button(text='Back to Login')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.role_input)
        layout.add_widget(register_btn)
        layout.add_widget(back_btn)
        layout.add_widget(self.message)
        self.add_widget(layout)

    def register(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        role = self.role_input.text.strip().lower()
        if role not in ['farmer', 'buyer']:
            self.message.text = 'Role must be farmer or buyer'
            return
        if any(u['username'] == username for u in users):
            self.message.text = 'Username already exists'
            return
        users.append({'username': username, 'password': password, 'role': role})
        self.message.text = 'Registration successful. Please login.'
        self.username_input.text = ''
        self.password_input.text = ''
        self.role_input.text = ''

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.welcome_label = Label(text='Welcome!')
        self.layout.add_widget(self.welcome_label)
        buttons_layout = GridLayout(cols=2, spacing=10)
        buttons_layout.add_widget(Button(text='Browse Produce', on_press=lambda x: setattr(self.manager, 'current', 'browse')))
        buttons_layout.add_widget(Button(text='Transactions', on_press=lambda x: setattr(self.manager, 'current', 'transactions')))
        buttons_layout.add_widget(Button(text='Weather', on_press=lambda x: setattr(self.manager, 'current', 'weather')))
        buttons_layout.add_widget(Button(text='Govt Schemes', on_press=lambda x: setattr(self.manager, 'current', 'schemes')))
        buttons_layout.add_widget(Button(text='Market Prices', on_press=lambda x: setattr(self.manager, 'current', 'prices')))
        if self.user and self.user['role'] == 'farmer':
            buttons_layout.add_widget(Button(text='List Produce', on_press=lambda x: setattr(self.manager, 'current', 'list_produce')))
        self.layout.add_widget(buttons_layout)
        self.logout_btn = Button(text='Logout')
        self.logout_btn.bind(on_press=self.logout)
        self.layout.add_widget(self.logout_btn)
        self.add_widget(self.layout)

    def set_user(self, user):
        self.user = user
        self.welcome_label.text = f"Welcome, {user['username']}! Role: {user['role']}"
        if user['role'] == 'farmer':
            self.layout.children[1].add_widget(Button(text='List Produce', on_press=lambda x: setattr(self.manager, 'current', 'list_produce')))

    def logout(self, instance):
        self.manager.current = 'login'

class ListProduceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.name_input = TextInput(hint_text='Product Name', multiline=False)
        self.quantity_input = TextInput(hint_text='Quantity (kg)', multiline=False)
        self.price_input = TextInput(hint_text='Price per kg', multiline=False)
        self.location_input = TextInput(hint_text='Location', multiline=False)
        self.message = Label(text='')
        list_btn = Button(text='List Product')
        list_btn.bind(on_press=self.list_product)
        back_btn = Button(text='Back')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(self.name_input)
        layout.add_widget(self.quantity_input)
        layout.add_widget(self.price_input)
        layout.add_widget(self.location_input)
        layout.add_widget(list_btn)
        layout.add_widget(back_btn)
        layout.add_widget(self.message)
        self.add_widget(layout)

    def list_product(self, instance):
        name = self.name_input.text.strip()
        try:
            quantity = int(self.quantity_input.text.strip())
            price = float(self.price_input.text.strip())
        except ValueError:
            self.message.text = 'Invalid quantity or price'
            return
        location = self.location_input.text.strip()
        farmer = self.manager.get_screen('home').user['username']
        products.append({'id': len(products) + 1, 'farmer': farmer, 'name': name, 'quantity': quantity, 'price': price, 'location': location})
        self.message.text = 'Product listed successfully'
        self.name_input.text = ''
        self.quantity_input.text = ''
        self.price_input.text = ''
        self.location_input.text = ''

class BrowseProduceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)
        back_btn = Button(text='Back', size_hint_y=None, height=50)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)
        self.add_widget(self.layout)

    def on_enter(self):
        self.grid.clear_widgets()
        for product in products:
            btn = Button(text=f"{product['name']} - {product['quantity']}kg @ ₹{product['price']}/kg in {product['location']} (Farmer: {product['farmer']})", size_hint_y=None, height=100)
            btn.bind(on_press=lambda x, p=product: self.negotiate(p))
            self.grid.add_widget(btn)

    def negotiate(self, product):
        self.manager.get_screen('negotiate').set_product(product)
        self.manager.current = 'negotiate'

class NegotiateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product = None
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.product_label = Label(text='')
        self.offers_label = Label(text='')
        self.offer_input = TextInput(hint_text='Your Offer (₹)', multiline=False)
        submit_btn = Button(text='Submit Offer')
        submit_btn.bind(on_press=self.submit_offer)
        back_btn = Button(text='Back')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'browse'))
        layout.add_widget(self.product_label)
        layout.add_widget(self.offers_label)
        layout.add_widget(self.offer_input)
        layout.add_widget(submit_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def set_product(self, product):
        self.product = product
        self.product_label.text = f"Product: {product['name']}\nQuantity: {product['quantity']}kg\nPrice: ₹{product['price']}/kg\nLocation: {product['location']}"
        neg = next((n for n in negotiations if n['product_id'] == product['id']), None)
        if neg:
            self.offers_label.text = 'Offers: ' + ', '.join(map(str, neg['offers']))
        else:
            self.offers_label.text = 'No offers yet'

    def submit_offer(self, instance):
        try:
            offer = float(self.offer_input.text.strip())
        except ValueError:
            return
        neg = next((n for n in negotiations if n['product_id'] == self.product['id']), None)
        if not neg:
            neg = {'product_id': self.product['id'], 'offers': []}
            negotiations.append(neg)
        neg['offers'].append(offer)
        self.offers_label.text = 'Offers: ' + ', '.join(map(str, neg['offers']))
        self.offer_input.text = ''

class TransactionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        layout.add_widget(self.scroll)
        back_btn = Button(text='Back')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def on_enter(self):
        self.grid.clear_widgets()
        user = self.manager.get_screen('home').user
        for t in transactions:
            if t['buyer'] == user['username'] or any(p['farmer'] == user['username'] for p in products if p['id'] == t['product_id']):
                self.grid.add_widget(Label(text=f"Product ID: {t['product_id']}, Buyer: {t['buyer']}, Amount: ₹{t['amount']}, Status: {t['status']}", size_hint_y=None, height=50))

class WeatherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.weather_label = Label(text='Weather: Sunny, 25°C\nPodcast: Listen to today\'s farming weather update')
        back_btn = Button(text='Back')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(self.weather_label)
        layout.add_widget(back_btn)
        self.add_widget(layout)

class GovtSchemesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        for scheme in govt_schemes:
            self.grid.add_widget(Label(text=f"{scheme['name']}: {scheme['description']}\nLink: {scheme['link']}", size_hint_y=None, height=100))
        self.scroll.add_widget(self.grid)
        layout.add_widget(self.scroll)
        back_btn = Button(text='Back')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

class MarketPricesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        for item, price in market_prices.items():
            self.grid.add_widget(Label(text=f"{item}: ₹{price}/quintal", size_hint_y=None, height=50))
        self.scroll.add_widget(self.grid)
        layout.add_widget(self.scroll)
        back_btn = Button(text='Back')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

class SmartFarmersApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ListProduceScreen(name='list_produce'))
        sm.add_widget(BrowseProduceScreen(name='browse'))
        sm.add_widget(NegotiateScreen(name='negotiate'))
        sm.add_widget(TransactionsScreen(name='transactions'))
        sm.add_widget(WeatherScreen(name='weather'))
        sm.add_widget(GovtSchemesScreen(name='schemes'))
        sm.add_widget(MarketPricesScreen(name='prices'))
        return sm

if __name__ == '__main__':
    SmartFarmersApp().run()
