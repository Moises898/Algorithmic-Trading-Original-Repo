import customtkinter
import tkinter as tk
from Classes.Strategies import *
from PIL import Image

def validate_numeric_input(action, value_if_allowed):
    # Validation function to allow only numeric characters
    if action == '1':  # insert
        return all(char.isdigit() or char == '.' or char == "%" for char in value_if_allowed)
    return True

def set_up_main_frame(frame):
    """
        Reset the layout and grid for the main Frame of the root window
    """
    frame.main_frame = customtkinter.CTkFrame(frame,width=500, corner_radius=10)  
    frame.main_frame.grid_rowconfigure(0, weight=1)
    frame.main_frame.grid_columnconfigure(0, weight=1)
    frame.main_frame.grid(row=0,column=1, sticky="nsew",padx=(15, 15), pady=(20, 20))    
    
def side_bar(frame):
    """
        Display the sidebar with the available options mapped to their event in the main file
    """
    frame.sidebar_frame = customtkinter.CTkFrame(frame, width=100, corner_radius=10)
    frame.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(15, 0), pady=(20, 20))
    frame.sidebar_frame.grid_rowconfigure(4, weight=1)
    my_image = customtkinter.CTkImage(light_image=Image.open(r"assets\images\icon.png"), size=(100, 100))
    
    frame.logo_label = customtkinter.CTkLabel(frame.sidebar_frame,image=my_image, text="", font=customtkinter.CTkFont(family="Open Sans",size=22, weight="bold"))
    frame.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
    image_label = customtkinter.CTkLabel(frame.sidebar_frame, text="ATLAS", font=customtkinter.CTkFont(size=20, weight="bold"))
    image_label.grid(row=1, column=0, padx=20, pady=(5, 10))
    
    frame.sidebar_button_1 = customtkinter.CTkButton(frame.sidebar_frame, command=frame.sidebar_button_login_event,text="Start")
    frame.sidebar_button_1.grid(row=2, column=0, padx=20, pady=(280,10))
    
    frame.sidebar_button_2 = customtkinter.CTkButton(frame.sidebar_frame, command=frame.sidebar_button_event,text="Disclaimer")
    frame.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)          

def login_for_license_screen(frame):
    """
        Display the screen to validate if the user has an active license
    """
    set_up_main_frame(frame)                   
    frame.main_frame.grid_rowconfigure(0,weight=0)
    
    frame.main_frame.message = customtkinter.CTkLabel(frame.main_frame, text="Welcome", font=customtkinter.CTkFont(size=25, weight="bold"))
    frame.main_frame.message.grid(row=0, column=0, padx=(20,20), pady=(30,5))
    frame.main_frame.message_2 = customtkinter.CTkLabel(frame.main_frame, text="Please authenticate before start", font=customtkinter.CTkFont(size=15, weight="normal"))
    frame.main_frame.message_2.grid(row=1, column=0, padx=(20,20), pady=(0,20))
    
    frame.main_frame.user_input = customtkinter.CTkEntry(frame.main_frame, placeholder_text="User Name")
    frame.main_frame.user_input.grid(row=2, column=0, padx=(20, 20), pady=10, sticky="ew")
    
    frame.main_frame.password = customtkinter.CTkEntry(frame.main_frame, placeholder_text="Password",show="*")
    frame.main_frame.password.grid(row=3, column=0, padx=(20, 20), pady=10, sticky="ew")
    
    frame.main_frame.send_data = customtkinter.CTkButton(frame.main_frame, text="LOG IN", command=frame.validate_active_license)
    frame.main_frame.send_data.grid(row=4, column=0,pady=10)    
    
def help_screen(frame):
    set_up_main_frame(frame)  
    
    frame.main_frame.grid_rowconfigure(1, weight=1)   
    
    frame.main_frame.message = customtkinter.CTkLabel(frame.main_frame,
                                                      text="DISCLAIMER",
                                                      font=customtkinter.CTkFont(size=25, weight="bold"),
                                                        wraplength=400,
                                                        justify="left",
                                                        anchor="center")
    frame.main_frame.message.grid(row=0, column=0, padx=(20, 20), pady=(10), sticky="ew")
    
    disclaimer_text = (
        "This software is a trading tool designed to assist users in their trading operations. "
        "By using this software, you acknowledge and agree that you are solely responsible for any trading losses incurred. "
        "This software does not guarantee profits or prevent losses in trading. Your use of this software is at your own risk. "
        "You should conduct your own research and consult with a financial advisor before making any trading decisions. "
        "This software may contain errors or technical limitations. "
        "Ensure compliance with all applicable laws and regulations governing trading activities. "        
    )
    frame.main_frame.message2 = customtkinter.CTkLabel(frame.main_frame,
                                                       text=disclaimer_text,
                                                       font=customtkinter.CTkFont(size=15),
                                                       wraplength=400,
                                                       justify="left",
                                                       anchor="center")
    frame.main_frame.message2.grid(row=1, column=0, padx=10, pady=0, sticky="ew")  
    
    my_image = customtkinter.CTkImage(light_image=Image.open(r"C:\Users\Moy\Documents\Python\Algorithmic Trading\HFT\assets\images\information.png"),size=(125, 125))
    image_label = customtkinter.CTkLabel(frame.main_frame, image=my_image, text="")  # display image with a CTkLabel
    image_label.grid(row=2,column=0, sticky="nsew",padx=(15, 15), pady=(0, 60))
                             
def connection_mt5_screen(frame):
    """
        Display the screen with the fields to connect to MT5
    """
    set_up_main_frame(frame)                   
    frame.main_frame.grid_rowconfigure(0, weight=0)
    frame.main_frame.grid_rowconfigure(1, weight=1)
    frame.main_frame.grid_rowconfigure(2, weight=0)
    frame.main_frame.grid_rowconfigure(3, weight=0)
    frame.main_frame.grid_rowconfigure(4, weight=0)
    frame.main_frame.grid_rowconfigure(5, weight=1)
    frame.main_frame.grid_rowconfigure(6, weight=2)
    
    frame.main_frame.message = customtkinter.CTkLabel(frame.main_frame, text="MT5 Connection", font=customtkinter.CTkFont(size=25, weight="bold"))
    frame.main_frame.message.grid(row=0, column=0, padx=(20,20), pady=(30,15))
    frame.main_frame.message_2 = customtkinter.CTkLabel(frame.main_frame, text="Please enter your credentials to connect to your account \ntrought MT5", font=customtkinter.CTkFont(size=15, weight="normal"))
    frame.main_frame.message_2.grid(row=1, column=0, padx=(20,20), pady=(0,20),sticky="ew")
    
    frame.main_frame.account_number = customtkinter.CTkEntry(frame.main_frame, placeholder_text="Account Number")
    frame.main_frame.account_number.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
    frame.main_frame.account_number.grid(row=2, column=0, padx=(20, 20), pady=10, sticky="ew")
    
    frame.main_frame.password_mt5 = customtkinter.CTkEntry(frame.main_frame, placeholder_text="Password",show="*")
    frame.main_frame.password_mt5.grid(row=3, column=0, padx=(20, 20), pady=10, sticky="ew")
    
    frame.main_frame.server = customtkinter.CTkEntry(frame.main_frame, placeholder_text="Server")
    frame.main_frame.server.grid(row=4, column=0, padx=(20, 20), pady=10, sticky="ew")
    
    frame.main_frame.connect = customtkinter.CTkButton(frame.main_frame, text="START",command=frame.start_connection)
    frame.main_frame.connect.grid(row=5, column=0,pady=10)    
    
    frame.main_frame.message_3 = customtkinter.CTkLabel(frame.main_frame, text="Data is only used to connect to MT5.", font=customtkinter.CTkFont(size=15, weight="normal",slant="italic"))
    frame.main_frame.message_3.grid(row=6, column=0, padx=(20,20), pady=(0,20),sticky="ew")
    
def error_screen(frame,title,message_1,message_2,command_to_trigger):
    set_up_main_frame(frame) 
    messages = message_2.split("\n")                    
    frame.main_frame.grid_rowconfigure(0, weight=1)
    frame.main_frame.grid_rowconfigure(1, weight=0)
    frame.main_frame.grid_rowconfigure(2, weight=0)
    frame.main_frame.grid_rowconfigure(2+len(messages), weight=2)         
                    
    frame.main_frame.title = customtkinter.CTkLabel(frame.main_frame, text=title, font=customtkinter.CTkFont(size=25, weight="bold"))
    frame.main_frame.title.grid(row=0, column=0, padx=(20,20), pady=(20,20))
    
    frame.main_frame.message_1 = customtkinter.CTkLabel(frame.main_frame, text=message_1, font=customtkinter.CTkFont(size=15, weight="normal"))
    frame.main_frame.message_1.grid(row=1, column=0, padx=(20,20), pady=(0,20),sticky="ew")
    
    for i in range(len(messages)):    
        message = customtkinter.CTkLabel(master=frame.main_frame, text=f"{messages[i]}",font=customtkinter.CTkFont(size=14, weight="normal"),anchor="w")
        message.grid(row=2+i, column=0, padx=20, pady=(0,5),sticky="ew")
        
    frame.main_frame.connect = customtkinter.CTkButton(frame.main_frame, text="Main Screen",command=command_to_trigger)
    frame.main_frame.connect.grid(row=len(messages) + 2, column=0,pady=10)
                
def strategy_running_screen(frame):
    """
        Display the screen with the fields to connect to MT5
    """   
    
    PADX = (0,40)
    PADY = 10    
    
    def update_profit(object):    
        if not object.stop_thread_flag.is_set():                       
            # Current Profit/Loss acumulated            
            current_profit = object.connection.account_details().equity - object.balance                            
            object.main_frame.profit_or_loss = customtkinter.CTkLabel(frame.main_frame,                                                    
                                                  text=f"PnL Session: {round(current_profit,2):,}",
                                                  font=customtkinter.CTkFont(size=15, weight="normal"))
            object.main_frame.profit_or_loss.grid(row=6, column=0,columnspan=2, padx=PADX, pady=2, sticky="ew")    
            if not object.stop_thread_flag.is_set():                       
                frame.main_frame.after(1000,lambda: update_profit(object))
    frame.sidebar_button_2.configure(state="disabled")    
    # Define Tkinter variables to update the GUI and parameters introduced by the user   
    initial_balance = tk.StringVar(value=f"{frame.balance:,}") 
    frame.profit = tk.StringVar(value="0.0")
    parameters_to_display = [
                             f"Dynamic SL = {frame.dynamic_sl}".strip(),
                             f"Partial Close = {frame.partial_close}".strip(),
                             f"Lots = {frame.lots}".strip(),
                             f"Points = {frame.points}".strip(),
                             f"Initial Balance: {initial_balance.get()}".strip(),
                             f"PnL Session: {frame.profit.get()}".strip()]
    set_up_main_frame(frame)    
    frame.main_frame.grid_rowconfigure((0,len(parameters_to_display)+1), weight=2)    
    #frame.main_frame.grid_rowconfigure((1,len(parameters_to_display)), weight=1)                
    frame.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")        
    
    # Initialize Strategy Title
    frame.main_frame.message = customtkinter.CTkLabel(frame.main_frame,
                                                                        text=f"Strategy Running in {frame.symbol}",
                                                                        font=customtkinter.CTkFont(size=24, weight="bold"))
    frame.main_frame.message.grid(row=0, column=0, columnspan=2, padx=20, pady=0, sticky="ew")

    # Display parameters used and symbol
    for index, param in enumerate(parameters_to_display, start=1):
        label = customtkinter.CTkLabel(frame.main_frame, text=param, font=customtkinter.CTkFont(size=15))
        label.grid(row=index, column=0, columnspan=2, padx=10, pady=0, sticky="ew")
    
    # Button Close Session
    frame.main_frame.stop_thread = customtkinter.CTkButton(frame.main_frame, text="Stop Session",command= frame.stop_session)
    frame.main_frame.stop_thread.grid(row=len(parameters_to_display)+1, column=0, padx=(40,5), pady=PADY,sticky="ew")      
    # Button Close Positions    
    frame.main_frame.close_trades = customtkinter.CTkButton(frame.main_frame, text="Close Trades",command= frame.close_entry)
    frame.main_frame.close_trades.grid(row=len(parameters_to_display)+1, column=1, padx=(5,40), pady=PADY,sticky="ew")               
    
    # Start threads after display the GUI 
    frame.strategy_thread.start()    
    # Update the PL
    update_profit(frame)    
    
def start_strategy_mt5_screen(frame):
    """
    Display the screen with the current symbols and parameters to start the strategy
    using a two-column layout.
    """
    
    def set_lots():
        if frame.main_frame.fibonacci_options.get() == "Disable":
            if frame.main_frame.symbol == "XAUUSD":
                frame.lots.set(str(round(lots_value / 3, 2)))                
            else:
                frame.lots.set(str(lots_value))
        else:
            if frame.main_frame.symbol == "XAUUSD":
                frame.lots.set(str(round(lots_value / 1.5, 2)))                
            else:
                frame.lots.set(str(lots_value * 2))
    
    def display_points(selection):
        if selection == "Enable":
            frame.main_frame.points_label.grid_forget()
            frame.main_frame.points_entry.grid_forget()              
        elif selection == "Disable":            
            # Point for TP/SL
            frame.main_frame.points_label = customtkinter.CTkLabel(frame.main_frame,
                                                                text="Points to TP/SL:", anchor="e")
            frame.main_frame.points_label.grid(row=11, column=0, padx=PADX, pady=PADY)
            frame.main_frame.points_entry = customtkinter.CTkEntry(frame.main_frame,
                                                                placeholder_text="Points TP/SL",
                                                                textvariable=frame.points)
            frame.main_frame.points_entry.grid(row=11, column=1, padx=PADX, pady=PADY, sticky="ew")        
            frame.main_frame.points_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
            frame.main_frame.message.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="ew")
            frame.main_frame.start_strategy.grid(row=13, column=0, columnspan=2, padx=150, pady=15, sticky="ew")        
        
    def symbol_adjustments(selection):
        if selection == "XAUUSD":
            frame.lots.set(str(round(lots_value / 3, 2)))            
            frame.points.set(str(points("XAUUSD")))
        else:
            frame.lots.set(str(lots_value))
            frame.points.set(str(points(".")))
        
    def format_percentage(value):
        try:
            value = float(value)
            return f"{value}%"
        except ValueError:
            return value
    
    def on_risk_change(event):
        current_value = frame.main_frame.risk_entry.get().replace("%", "")
        formatted_value = format_percentage(current_value)  
        frame.main_frame.risk_entry.delete(0, 'end')
        frame.main_frame.risk_entry.insert(0, formatted_value)
    
    def on_profit_change(event):
        current_value = frame.main_frame.gain_entry.get().replace("%", "")  
        formatted_value = format_percentage(current_value)  
        frame.main_frame.gain_entry.delete(0, 'end')
        frame.main_frame.gain_entry.insert(0, formatted_value)
        
    PADX = (0,40)
    PADY = 2.5
    connection = frame.connection    
    symbols = connection.display_symbols(["EURUSD", "XAUUSD"], 30)
    
    # Define Tkinter variables to update the GUI
    frame.risk = tk.StringVar(value="0.5%")
    frame.target_profit = tk.StringVar(value="0.5%")
    frame.max_trades = tk.StringVar(value="8")
    frame.balance = connection.account_details().balance   
    lots_value = 0.01 if frame.balance < 1000 else round((frame.balance / 10_000) * .10, 2)
    points = lambda x: TARGET_POINTS_XAUUSD if x == "XAUUSD" else TARGET_POINTS_EURUSD
    frame.points = tk.StringVar(value=str(points("."))) 
    frame.lots = tk.StringVar(value=str(lots_value))
    
    set_up_main_frame(frame)
    frame.main_frame.grid_rowconfigure(0, weight=1)
    frame.main_frame.grid_columnconfigure(0, weight=1)
    frame.main_frame.grid_rowconfigure(13, weight=2)
    
    if len(symbols) != 0:       
        
        # Configure grid for two columns
        frame.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")        
        # Initialize Strategy Title
        frame.main_frame.message = customtkinter.CTkLabel(frame.main_frame,
                                                                            text="Initialize Strategy",
                                                                            font=customtkinter.CTkFont(size=22, weight="bold"))
        frame.main_frame.message.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="ew")

        # Instructions Text
        frame.main_frame.message_2 = customtkinter.CTkLabel(frame.main_frame,
                                                                              text="Please enter your parameters to start the strategy",
                                                                              font=customtkinter.CTkFont(size=15, weight="normal"))
        frame.main_frame.message_2.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(0, 6), sticky="ew")
      
        # Symbol Selector
        frame.main_frame.symbol = customtkinter.CTkLabel(frame.main_frame, text="Symbol:", anchor="e")
        frame.main_frame.symbol.grid(row=3, column=0, padx=PADX, pady=PADY)

        frame.main_frame.symbols_options = customtkinter.CTkOptionMenu(frame.main_frame,
                                                                                        values=[symbol.name for symbol in symbols],
                                                                                        command=symbol_adjustments)
        frame.main_frame.symbols_options.grid(row=3, column=1, padx=PADX, pady=(10, 10), sticky="ew")
        # Risk 
        frame.main_frame.risk = customtkinter.CTkLabel(frame.main_frame, text="% Risk:",
                                                                        anchor="e")
        frame.main_frame.risk.grid(row=4, column=0, padx=PADX, pady=PADY)
        frame.main_frame.risk_entry = customtkinter.CTkEntry(frame.main_frame,
                                                                            placeholder_text="% Risk")
        frame.main_frame.risk_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
        frame.main_frame.risk_entry.grid(row=4, column=1, padx=PADX, pady=PADY, sticky="ew")  
        frame.main_frame.risk_entry.bind("<Return>", on_risk_change)      
        # Profit
        frame.main_frame.gain = customtkinter.CTkLabel(frame.main_frame, text="% Profit:",
                                                                        anchor="e")
        frame.main_frame.gain.grid(row=5, column=0, padx=PADX, pady=PADY)
        frame.main_frame.gain_entry = customtkinter.CTkEntry(frame.main_frame,
                                                                            placeholder_text="Expected Profit Percentage")
        frame.main_frame.gain_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
        frame.main_frame.gain_entry.grid(row=5, column=1, padx=PADX, pady=PADY, sticky="ew")  
        frame.main_frame.gain_entry.bind("<Return>", on_profit_change)         
        # Max entries
        frame.main_frame.max_trades = customtkinter.CTkLabel(frame.main_frame,
                                                                            text="Max Trades:", anchor="e")
        frame.main_frame.max_trades.grid(row=6, column=0, padx=PADX, pady=PADY)
        frame.main_frame.max_trades_entry = customtkinter.CTkEntry(frame.main_frame,
                                                                                    placeholder_text="Max Number of Trades allowed")
        frame.main_frame.max_trades_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
        frame.main_frame.max_trades_entry.grid(row=6, column=1, padx=PADX, pady=10, sticky="ew")        
        # Partial Close
        frame.main_frame.partial_close = customtkinter.CTkLabel(frame.main_frame,
                                                                            text="Enable Partial Close:", anchor="e")
        frame.main_frame.partial_close.grid(row=7, column=0, padx=PADX, pady=PADY)
        frame.main_frame.partial_close_options = customtkinter.CTkOptionMenu(frame.main_frame,
                                                                                            values=["Enable", "Disable"])        
        frame.main_frame.partial_close_options.grid(row=7, column=1, padx=PADX, pady=PADY, sticky="ew")               
        # Entries per Signal
        frame.main_frame.positions = customtkinter.CTkLabel(frame.main_frame,
                                                                            text="Positions per Entry:", anchor="e")
        frame.main_frame.positions.grid(row=8, column=0, padx=PADX, pady=PADY)
        frame.main_frame.positions_entry = customtkinter.CTkEntry(frame.main_frame,
                                                                                    placeholder_text="# Trades per signal")        
        frame.main_frame.positions_entry.grid(row=8, column=1, padx=PADX, pady=PADY, sticky="ew")
        frame.main_frame.positions_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
        # Lots per entry    
        frame.main_frame.lots_label = customtkinter.CTkLabel(frame.main_frame,
                                                            text="Lots per Entry:", anchor="e")
        frame.main_frame.lots_label.grid(row=9, column=0, padx=PADX, pady=PADY)
        frame.main_frame.lots_entry = customtkinter.CTkEntry(frame.main_frame,
                                                            placeholder_text="Lots per entry",
                                                            textvariable=frame.lots)        
        frame.main_frame.lots_entry.grid(row=9, column=1, padx=PADX, pady=PADY, sticky="ew")        
        frame.main_frame.lots_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
        # TP/SL based on Fibonacci Levels
        frame.main_frame.fibonacci_label = customtkinter.CTkLabel(frame.main_frame,
                                                            text="Automatic SL/TP:", anchor="e")
        frame.main_frame.fibonacci_label.grid(row=10, column=0, padx=PADX, pady=PADY)
        frame.main_frame.fibonacci_options = customtkinter.CTkOptionMenu(frame.main_frame,
                                                                                            values=["Enable", "Disable"],
                                                                                            command=display_points) 
        frame.main_frame.fibonacci_options.grid(row=10, column=1, padx=PADX, pady=PADY, sticky="ew")                                  
        # Point for TP/SL
        frame.main_frame.points_label = customtkinter.CTkLabel(frame.main_frame,
                                                            text="Points to TP/SL:", anchor="e")
        frame.main_frame.points_label.grid(row=11, column=0, padx=PADX, pady=PADY)
        frame.main_frame.points_entry = customtkinter.CTkEntry(frame.main_frame,
                                                            placeholder_text="Points TP/SL",
                                                            textvariable=frame.points)        
        frame.main_frame.points_entry.grid(row=11, column=1, padx=PADX, pady=PADY, sticky="ew")        
        frame.main_frame.points_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
        # Dynamic SL
        frame.main_frame.dynamic_SL_label = customtkinter.CTkLabel(frame.main_frame,
                                                                        text="Dynamic SL:", anchor="e")
        frame.main_frame.dynamic_SL_label.grid(row=12, column=0, padx=PADX, pady=PADY)
        frame.main_frame.dynamic_SL_menu = customtkinter.CTkOptionMenu(frame.main_frame,   
                                                                       values=["Enable", "Disable"])
        frame.main_frame.dynamic_SL_menu.grid(row=12, column=1, padx=PADX, pady=PADY,sticky="ew")
        # # Reverse entries
        # frame.main_frame.reverse_label = customtkinter.CTkLabel(frame.main_frame,
        #                                                                 text="Reverse entries:", anchor="e")
        # frame.main_frame.reverse_label.grid(row=13, column=0, padx=PADX, pady=PADY)
        # frame.main_frame.reverse_menu = customtkinter.CTkOptionMenu(frame.main_frame,   
        #                                                                values=["Enable", "Disable"])
        # frame.main_frame.reverse_menu.grid(row=13, column=1, padx=PADX,sticky="ew")
                                                    
        # START button 
        frame.main_frame.start_strategy = customtkinter.CTkButton(frame.main_frame, text="START", command=frame.start_strategy)
        frame.main_frame.start_strategy.grid(row=13, column=0, columnspan=2, padx=120, pady=10, sticky="ew")
        
        # Default values
        frame.main_frame.risk_entry.insert(0, frame.risk.get())  
        frame.main_frame.positions_entry.insert(0, "3")  
        frame.main_frame.gain_entry.insert(0, frame.target_profit.get())
        frame.main_frame.max_trades_entry.insert(0, frame.max_trades.get())
        frame.main_frame.partial_close_options.set("Enable")        
        #frame.main_frame.reverse_menu.set("Disable")
        frame.main_frame.dynamic_SL_menu.set("Enable")
        frame.main_frame.fibonacci_options.set("Disable")

    else:
        # If no symbols are available, display the error message
        frame.main_frame.message = customtkinter.CTkLabel(frame.main_frame,
                                                          text="Bad Market conditions",
                                                          font=customtkinter.CTkFont(size=25, weight="bold"))
        frame.main_frame.message.grid(row=0, column=0, padx=(20, 20), pady=(30, 15), sticky="ew")
        
        frame.main_frame.not_available = customtkinter.CTkLabel(frame.main_frame,
                                                                 text="Spread exceeds the minimum threshold! :( \nTry again later once the market has better conditions.",
                                                                 font=customtkinter.CTkFont(size=16, weight="normal"))
        frame.main_frame.not_available.grid(row=1, column=0, padx=0, pady=0)
        
        my_image = customtkinter.CTkImage(light_image=Image.open(r"assets\images\research.png"), size=(250, 250))
        image_label = customtkinter.CTkLabel(frame.main_frame, image=my_image, text="")
        image_label.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
   
def start_strategy_in_backtest_screen(frame):
    """
    Display the screen with the current symbols and parameters to start the strategy
    using a two-column layout.
    """
    def symbol_adjustments(selection):
        if selection == "XAUUSD":          
            frame.points.set(str(points("XAUUSD")))
        else:            
            frame.points.set(str(points(".")))
            
    def display_points(selection):
        if selection == "Enable":
            frame.main_frame.points_label.grid_forget()
            frame.main_frame.points_entry.grid_forget()              
        elif selection == "Disable":            
            # Point for TP/SL
            frame.main_frame.points_label = customtkinter.CTkLabel(frame.main_frame,
                                                                text="Points to TP/SL:", anchor="e")
            frame.main_frame.points_label.grid(row=11, column=0, padx=PADX, pady=PADY)
            frame.main_frame.points_entry = customtkinter.CTkEntry(frame.main_frame,
                                                                placeholder_text="Points TP/SL",
                                                                textvariable=frame.points)
            frame.main_frame.points_entry.grid(row=11, column=1, padx=PADX, pady=PADY, sticky="ew")        
            frame.main_frame.points_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
            frame.main_frame.message.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="ew")
            frame.main_frame.start_strategy.grid(row=13, column=0, columnspan=2, padx=150, pady=15, sticky="ew")         
        
        
    PADX = (0,40)
    PADY = 2.5
    connection = frame.connection    
    symbols = connection.display_symbols(["EURUSD", "XAUUSD"], 100)
    
    # Define Tkinter variables to update the GUI    
    points = lambda x: TARGET_POINTS_XAUUSD if x == "XAUUSD" else TARGET_POINTS_EURUSD
    frame.points = tk.StringVar(value=str(points(".")))     
    
    set_up_main_frame(frame)
    frame.main_frame.grid_rowconfigure(0, weight=1)
    frame.main_frame.grid_columnconfigure(0, weight=1)
    frame.main_frame.grid_rowconfigure(13, weight=2)
    
        
    # Configure grid for two columns
    frame.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")        
    # Initialize Strategy Title
    frame.main_frame.message = customtkinter.CTkLabel(frame.main_frame,
                                                                        text="Backtest Strategy",
                                                                        font=customtkinter.CTkFont(size=22, weight="bold"))
    frame.main_frame.message.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="ew")

    # Instructions Text
    frame.main_frame.message_2 = customtkinter.CTkLabel(frame.main_frame,
                                                                            text="Please enter your parameters to simulate the strategy",
                                                                            font=customtkinter.CTkFont(size=15, weight="normal"))
    frame.main_frame.message_2.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(0, 6), sticky="ew")
    
    # Symbol Selector
    frame.main_frame.symbol = customtkinter.CTkLabel(frame.main_frame, text="Symbol:", anchor="e")
    frame.main_frame.symbol.grid(row=3, column=0, padx=PADX, pady=PADY)

    frame.main_frame.symbols_options = customtkinter.CTkOptionMenu(frame.main_frame,
                                                                                    values=[symbol.name for symbol in symbols],
                                                                                    command=symbol_adjustments)
    frame.main_frame.symbols_options.grid(row=3, column=1, padx=PADX, pady=(10, 10), sticky="ew")
    
    # Number of peridos for backtest
    frame.main_frame.periods_label = customtkinter.CTkLabel(frame.main_frame,
                                                        text="Number of Periods:", anchor="e")
    frame.main_frame.periods_label.grid(row=4, column=0, padx=PADX, pady=PADY)
    frame.main_frame.periods_entry = customtkinter.CTkEntry(frame.main_frame,
                                                        placeholder_text="# of Periods")        
    frame.main_frame.periods_entry.grid(row=4, column=1, padx=PADX, pady=PADY,sticky="ew")
    frame.main_frame.periods_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))
    
    # TP/SL based on Fibonacci Levels
    frame.main_frame.fibonacci_label = customtkinter.CTkLabel(frame.main_frame,
                                                        text="Automatic SL/TP:", anchor="e")
    frame.main_frame.fibonacci_label.grid(row=10, column=0, padx=PADX, pady=PADY)
    frame.main_frame.fibonacci_options = customtkinter.CTkOptionMenu(frame.main_frame,
                                                                                        values=["Enable", "Disable"],
                                                                                        command=display_points) 
    frame.main_frame.fibonacci_options.grid(row=10, column=1, padx=PADX, pady=PADY, sticky="ew")                                  
    # Point for TP/SL
    frame.main_frame.points_label = customtkinter.CTkLabel(frame.main_frame,
                                                        text="Points to TP/SL:", anchor="e")
    frame.main_frame.points_label.grid(row=11, column=0, padx=PADX, pady=PADY)
    frame.main_frame.points_entry = customtkinter.CTkEntry(frame.main_frame,
                                                        placeholder_text="Points TP/SL",
                                                        textvariable=frame.points)        
    frame.main_frame.points_entry.grid(row=11, column=1, padx=PADX, pady=PADY, sticky="ew")        
    frame.main_frame.points_entry.configure(validate='key', validatecommand=(frame.register(validate_numeric_input), '%d', '%S'))   
                                                
    # START button 
    frame.main_frame.start_strategy = customtkinter.CTkButton(frame.main_frame, text="START", command=frame.start_backtest)
    frame.main_frame.start_strategy.grid(row=13, column=0, columnspan=2, padx=120, pady=10, sticky="ew")
    
    # Default values   
    frame.main_frame.fibonacci_options.set("Disable")