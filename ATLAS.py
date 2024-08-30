import customtkinter
from Classes.components import *
from Classes.MT5 import MT5
from Classes.Strategies import main_loop
from charts import *
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

class App(customtkinter.CTk):
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
    
    def on_closing(self):
        # This function will be called when the user tries to close the window    
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
        if positions_open(self.connection):
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
            self.main_frame.stop_thread.grid(row=7, column=0,columnspan=2, padx=40, pady=0,sticky="ew")            
        except:
            pass
    # Close trades manually
    def close_entry(self):
        if positions_open(self.connection,self.symbol):
            self.close_postions_flag.set()
        else:
            tk.messagebox.showinfo("Information","There's no active trades :(")
    # Show/Hide button
    def display_buttons(self):
        self.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")                 
        # Position Open
        if positions_open(self.connection,self.symbol):
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
        self.symbol = self.main_frame.symbols_options.get()
        self.risk = float(str(self.main_frame.risk_entry.get()).replace("%","")) / 100
        self.profit = float(str(self.main_frame.gain_entry.get()).replace("%","")) / 100
        self.max_trades = int(self.main_frame.max_trades_entry.get())
        self.partial_close = self.main_frame.partial_close_options.get() == "Enable"
        self.dynamic_sl = self.main_frame.dynamic_SL_menu.get() == "Enable"        
        self.positions_entry = int(self.main_frame.positions_entry.get())    
        self.points = round(int(self.main_frame.points_entry.get()),2)        
        self.lots = float(self.main_frame.lots_entry.get())  
        self.fibonacci = self.main_frame.fibonacci_options.get() == "Enable"
        if self.stop_thread_flag.is_set():
            self.stop_thread_flag.clear()
        self.close_postions_flag = threading.Event()             
        periods = 500 
        # Code below is the implementation of a backtest before run the strategy to train a new random forest and combine with
        # base model to get better entries (takes lonher to start due the backtest and trainning)                                  
        # while True:
        #     if self.symbol == "XAUUSD":
        #         operations,_ = backtest_strategy(self.connection,periods,self.symbol,False,self.points,fibonacci=self.fibonacci,model=False)            
        #     else:
        #         operations,_ = backtest_strategy(self.connection,periods,self.symbol,False,45,fibonacci=False,model=False)            
        #     _,trades = analyze_results(operations)
        #     if len(trades) > 10:
        #         self.X, self.y = format_data_to_train_model(operations,trades,self.symbol)
        #         recent = train_random_forest(self.X,self.y)
        #         self.models_combined = ensemble_models(recent,self.X,self.y)
        #         self.models_combined.fit(self.X,self.y)
        #         break
        #     else:
        #         print("Duplicating")
        #         periods = periods * 2 
        # Create new thread with the strategy        
        self.strategy_thread = threading.Thread(target=main_loop,
                                                args=(self,
                                                      self.connection,
                                                      self.symbol,
                                                      self.partial_close,
                                                      self.risk,self.profit,
                                                      self.positions_entry,
                                                      self.max_trades,
                                                      "M1",
                                                      self.stop_thread_flag,
                                                      self.close_postions_flag,
                                                      self.points,
                                                      self.lots,
                                                      True,
                                                      self.dynamic_sl,
                                                      True,
                                                      self.fibonacci
                                                      #self.models_combined
                                                      ))             
                
        strategy_running_screen(self)       
                 
    def start_backtest(self):        
        self.symbol = self.main_frame.symbols_options.get()        
        # Default value
        self.reverse = True       
        self.points = round(int(self.main_frame.points_entry.get()),2)             
        self.fibonacci = self.main_frame.fibonacci_options.get() == "Enable"
        self.periods = self.main_frame.periods_entry.get()        
        
        # Start backtest to get the trades
        trades, win_rate = execute_backtest(connection=self.connection,
                                            symbol=self.symbol,
                                            n_periods=int(self.periods),
                                            points=self.points,
                                            automatic_points=self.fibonacci,
                                            use_random_forest=True,
                                            volume_filter=False,
                                            reverse_entries=False
                                            )    
        # Initialize window    
        chart = Chart(inner_width=.8,maximize=True,on_top=True,title="ATLAS - Backtesting")        
        chart.layout(background_color='#090008', text_color='#FFFFFF', font_size=16,
                    font_family='Helvetica')    
        chart.watermark('XAUUSD', color='rgba(180, 180, 240, 0.5)')

        chart.crosshair(mode='normal', vert_color='#FFFFFF', vert_style='dotted',
                        horz_color='#FFFFFF', horz_style='dotted')
        chart.legend(visible=True, font_size=14)           
                                    
        table,table_result = generate_tables_of_trades()       
        
        chart.show(block=True)   
        
if __name__ == "__main__":
    app = App()    
    app.mainloop()