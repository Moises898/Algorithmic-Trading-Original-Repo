import customtkinter
from Classes.components import *
from Classes.MT5 import MT5
from Classes.live_trading import on_tick
from backtest_gui import *
import threading
import requests
import tkinter as tk
from tkinter import messagebox

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("assets/themes/red.json")
#customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
from dotenv import load_dotenv
from os import environ
load_dotenv()

class ATLAS(customtkinter.CTk):
    admin = "Moises"
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("ATLAS")
        self.geometry(f"{680}x{600}")

        # Configure grid layout (2x2)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Display Side Bar in the App
        side_bar(self)        
        set_up_main_frame(self)           
        help_screen(self)
        
        self.sidebar_button_2.configure(state="disabled")    
        self.authentication = False   
        self.stop_thread_flag = threading.Event()
        # Connect the closing event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    # Close window button
    def on_closing(self):          
        if not self.stop_thread_flag.is_set() and "active_connection" in globals():
            self.stop_session()
        else:
            self.stop_thread_flag.set()
        # Destroy the window
        self.destroy()           
    # API Request
    def validate_active_license(self):
        # Simulate response from API    
        # url = 'http://127.0.0.1:8000/api/'
        # try:
        #     response = requests.get(url)
        #     if response.status_code == 200:
        #         data = response.json()         
        #     else:
        #         tk.messagebox.showerror("Error", "Failed to retrieve data")
        # except requests.exceptions.RequestException as e:
        #     tk.messagebox.showerror("Error", f"Request failed: {e}")
           
        # if self.main_frame.user_input.get() == self.admin and self.main_frame.password.get() == "1234":
        #     self.main_frame.grid_forget()
        print("Login Sucess")
        connection_mt5_screen(self)
        self.authentication = True
        # else:
        #     print("Auntenthication failed")           
    
    # Stop Startegy thread
    def stop_session(self): 
        if not self.connection.get_positions(0).empty:
            self.close_postions_flag.set()
            tk.messagebox.showinfo("Information","Active trades will be closed before end the session!")
            sleep(2)                                       
        self.stop_thread_flag.set()
        try:
            self.main_frame.profit_or_loss.grid_forget()
            self.main_frame.stop_thread.grid_forget()    
            self.main_frame.close_trades.grid_forget()  
            # Return button
            self.sidebar_button_2.configure(state="enabled")
            self.main_frame.stop_thread = customtkinter.CTkButton(self.main_frame, text="Return Strategy Screen",command= self.start_connection)
            self.main_frame.stop_thread.grid(row=4, column=0,columnspan=2, padx=40, pady=0,sticky="ew")            
        except:
            pass
    # Close trades manually
    def close_entry(self):
        if not self.connection.get_positions(0,symbol=self.symbol).empty:
            self.close_postions_flag.set()
        else:
            tk.messagebox.showinfo("Information","There's no active trades :(")
    # Show/Hide button
    def display_buttons(self):
        self.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")                 
        # Position Open
        if not self.connection.get_positions(0,symbol=self.symbol).empty:
            self.main_frame.close_position = customtkinter.CTkButton(self.main_frame, text="Close Position",command= self.start_connection)
            self.main_frame.close_position.grid(row=4, column=1,pady=10)                 
    # Screen Triggers
    def sidebar_button_login_event(self):
        self.sidebar_button_1.configure(state="disabled")
        set_up_main_frame(self)        
        self.main_frame.grid_forget()     
        if not self.authentication:   
            login_for_license_screen(self) 
        else:
            connection_mt5_screen(self)
        self.sidebar_button_2.configure(state="enabled")       

    def back_main_screen_event(self):
        self.main_frame.grid_forget()
        self.sidebar_button_1.configure(state="enabled")
        help_screen(self)
        self.sidebar_button_2.configure(state="disabled")
        
    def sidebar_button_event(self):
        self.sidebar_button_2.configure(state="disabled")
        help_screen(self)
        self.sidebar_button_1.configure(state="enabled")
        
    # MT5 Triggers
    def start_connection(self):
        if "active_connection" in globals():
            start_strategy_mt5_screen(self)            
        else:
            # Uncomment once you deploy
            # self.user_mt5 = int(self.main_frame.account_number.get())
            # self.password_mt5 = self.main_frame.password_mt5.get()
            
            # self.server_mt5 = self.main_frame.server.get()
            self.user_mt5 = int(environ.get("USER_DEMO"))
            self.password_mt5 = environ.get("PASSWORD_DEMO")
            self.server_mt5 = environ.get("SERVER_DEMO")
            try:
                self.connection = MT5(user=self.user_mt5,password=self.password_mt5,server=self.server_mt5)
                if self.connection.connection_state: 
                    global active_connection
                    active_connection = True      
                    self.initial_balance = self.connection.account_details().balance
                    start_strategy_mt5_screen(self)                               
                    #start_strategy_in_backtest_screen(self)
                    
            except Exception as e:
                # Display screen error with a message
                set_up_main_frame(self)
                error_screen(self,
                            title="Connection Failed",
                            message_1="Please verify next things before trying to connect again:",
                            message_2=f"-Make sure you have installed MT5 in your computer.\n-Valid credentials from a MT5 account.\n-Internet connection.\n-If your problem persist please contact us for assistance.\n{e}",
                            command_to_trigger=self.back_main_screen_event)            
        
    def start_strategy(self):                           
        # Dynamic Values
        self.symbol = self.main_frame.symbols_options.get()
        self.profit = float(str(self.main_frame.gain_entry.get()).replace("%","")) / 100
        self.risk = float(str(self.main_frame.risk_entry.get()).replace("%","")) / 100        
        self.max_trades = int(self.main_frame.max_trades_entry.get())
        self.entries_per_trade = int(self.main_frame.positions_entry.get())            
        self.lots = float(self.main_frame.lots_entry.get())  
        # Harcoded Values
        self.strategy = "multiple"             
        self.depth = 30           
        self.reverse = True
        # Strategy Parameters
        self.strategy_parameters = {
            "profit": self.initial_balance * self.profit,
            "loss": self.initial_balance * self.risk,
            "max_trades": self.max_trades,
            "dynamic_points":True,
            "timeFrame":"M1",
            "entries_per_trade":3,
            "lots": self.lots,
            "trailling_stop":True,
            "partial_close":True,
            "depth": self.depth,
            "reverse":self.reverse,
            "min_points":100            
        }        
        
        if self.stop_thread_flag.is_set():
            self.stop_thread_flag.clear()
        self.close_postions_flag = threading.Event()                          
        # Create new thread with the strategy, one single trade
        self.strategy_thread = threading.Thread(target=on_tick,
                                                args=(self.connection,
                                                      self.symbol,
                                                      self.strategy,
                                                      self.strategy_parameters                                                  
                                                      ),
                                                kwargs={
                                                    "gui": self,                                                    
                                                    }
                                                )                    
                        
        strategy_running_screen(self)       
                    
        
if __name__ == "__main__":
    app = ATLAS()    
    app.mainloop()