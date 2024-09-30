from Classes.MT5 import MT5
from Classes.data_operations import *
from Classes.Strategies import *
from Classes.backtest import *
from lightweight_charts import Chart

operation_line = None
id_mapping = {}


def format_table(row):
    ids_of_rows = [table.get(item[0]) for item in table.items()]             
    for id in ids_of_rows:
        for column in ('ID',"Result","TP","SL","Points"):
            id.background_color(column,color="#121417")
    for column in ('ID',"Result","TP","SL","Points"):        
        row.background_color(column=column, color="green")    

def clear_screen():
    global operation_line
    lines = chart.lines()    
    if len(lines) > 0:
        for line in lines:
            line.delete()      
    if operation_line is not None:
        operation_line.delete()
        operation_line = None        
    chart.clear_markers()
    
def plot_selected_trade(row):
    global id_mapping
    previous_data = trades[id_mapping[row["ID"]]]["df_strategy"]
    data_from_entry = trades[id_mapping[row["ID"]]]["df"]    
    entry =  trades[id_mapping[row["ID"]]]["type"]    
    SL = data_from_entry["SL"].iloc[0]
    TP = data_from_entry["TP"].iloc[0]
    end = -1
    for idx, (high, low) in enumerate(zip(data_from_entry["high"], data_from_entry["low"])):
        if entry == "BUY":
            if high >= TP or low <= SL:
                end = idx
                break
        else:
            if low <= TP or high >= SL:
                end = idx
                break            

    all_data = pd.concat([previous_data,data_from_entry.iloc[:end+30]]).reset_index()    
    all_data['time'] = pd.to_datetime(all_data['time'], unit='s',utc=True).dt.tz_convert('America/Mexico_City')    
    
    chart.set(all_data)     
    chart.marker(
            time=data_from_entry.reset_index()["time"].iloc[0],
            position='below' if entry == 'BUY' else 'above',
            shape='arrow_up' if entry == 'BUY' else 'arrow_down',
            color='red' if entry == 'SELL' else 'green',
            text=entry
        )
    if end != -1:
        chart.marker(
            time=data_from_entry.reset_index()["time"].iloc[end],
            position='below' if entry == 'SELL' else 'above',
            shape='arrow_up' if entry == 'SELL' else 'arrow_down',
            color='red' if entry == 'SELL' else 'green',
            text=f'{entry} Exit'
        )
       
    data_from_entry = data_from_entry.reset_index()
    data_from_entry['time'] = pd.to_datetime(data_from_entry['time'], unit='s')
    df_entry = pd.DataFrame({"time":data_from_entry["time"].values, "Entry Price":[id_mapping[row["ID"]] for _ in range(data_from_entry.shape[0])]})  
     
    return df_entry,data_from_entry,entry,end

def on_row_click(row): 
    global operation_line     
    clear_screen()
    format_table(row)                    
    df_entry,data_from_entry,entry,end = plot_selected_trade(row)    
           
        
    operation_line = chart.trend_line(
                            start_time=df_entry["time"].iloc[0],
                            start_value=df_entry["Entry Price"].iloc[0],
                            end_time=df_entry["time"].iloc[end],
                            end_value=data_from_entry["TP" if row["Result"] == "WIN" else "SL"].iloc[0],
                            color= "red" if entry == 'SELL' else "green",
                            style="sparse_dotted")      
    
    table.footer[1] = id_mapping[row["ID"]]
    
def execute_backtest(connection,symbol,n_periods,points=100,automatic_points=False,use_random_forest=False,volume_filter=False,reverse_entries=False):              
    # Execute with custom parameteres
    operations, _ = backtest_strategy(connection,n_periods,symbol,reverse_entries,points,volume_filter,fibonacci=automatic_points,model=use_random_forest)     
    counters,results = analyze_results(operations)
    try:
        win_rate = counters['tp_counter']  / sum(counters.values())
        drop_open_trades = []
        # Ask the user if want to display the open trades
        for trade in operations.keys():
            if trade in results.keys():
                operations[trade]["result"] = results[trade]["result"]
            else:
                drop_open_trades.append(trade)
                #operations[trade]["result"] = "OPEN"
        # Drop the keys
        for open_trade in drop_open_trades:
            del operations[open_trade]
        return operations,win_rate        
    except ZeroDivisionError:        
        return None,None   
    

def generate_tables_of_trades(chart,results):
    # Table displaying the results
    table_result = chart.create_table(width=0.2,height=.2,    
                  headings=('Metric','Result'),                  
                  position='right',
                  func= click)  
    # Table dispalying the trades
    table = chart.create_table(width=0.2, height=.78,
                  headings=('ID',"Result","TP","SL","Points"),
                  widths=(.20,.20,.20,.20,.20),
                  alignments=('center','center'),
                  position='right',                   
                  func=on_row_click)               
    table.footer(2)
    table.footer[0] = 'Entry Price:'       
    profit_points = 0 
    loss_points = 0 
    win_operations = 0
    loss_operations = 0
    # Add values for the selected trade
    for idx,key in enumerate(trades.keys()):
        id_mapping[idx] = key
        result = trades[key]["result"]
        if result == "WIN":
            profit_points += trades[key]["points"]
            win_operations += 1
            table.new_row(idx, result,round(trades[key]["df"]["TP"].iloc[0],2 if symbol == "XAUUSD" else 4),round(trades[key]["df"]["SL"].iloc[0],2 if symbol == "XAUUSD" else 4),trades[key]["points"])    
        else:
            loss_points += trades[key]["sl_points"]
            loss_operations += 1
            table.new_row(idx, result,round(trades[key]["df"]["TP"].iloc[0],2 if symbol == "XAUUSD" else 4),round(trades[key]["df"]["SL"].iloc[0],2 if symbol == "XAUUSD" else 4),trades[key]["sl_points"]) 
    # Display metrics from the backtest
    table_result.new_row("WIN RATE",round(win_rate,2))
    table_result.new_row("POINTS",profit_points-loss_points)  
    table_result.new_row("WIN TRADES",win_operations)  
    table_result.new_row("LOSS TRADES",loss_operations) 
    table_result.new_row("PnL",round(results["Profit"].astype(float).sum(),2)) 
    
    return table,table_result

def click(row):
    pass

if __name__ == '__main__':     
    
    # START CONNECTION
    user = 3000063681
    password = "821AZ!$p5x"
    server = "demoUK-mt5.darwinex.com"    
    conn = MT5(user, password, server)
    n_periods = 1000
    symbol = "XAUUSD"
    #best_settings = optimize_strategy(conn, n_periods, symbol)           
    # Start backtest to get the trades
    trades, win_rate = execute_backtest(connection=conn,
                                        symbol=symbol,
                                        n_periods=n_periods,
                                        points= 400,#best_settings['best_points'],
                                        automatic_points=True,#best_settings['fibonnaci_used'],
                                        use_random_forest=False,#best_settings['randomForest'],
                                        volume_filter=False,
                                        reverse_entries=False
                                        )   
    if trades is None:
        print("No entries") 
    else:
        # Initialize window    
        chart = Chart(inner_width=.8,maximize=True,title="ATLAS - Backtesting")        
        chart.layout(background_color='#090008', text_color='#FFFFFF', font_size=16,
                    font_family='Helvetica')    
        #chart.watermark('XAUUSD', color='rgba(180, 180, 240, 0.5)')

        chart.crosshair(mode='normal', vert_color='#FFFFFF', vert_style='dotted',
                        horz_color='#FFFFFF', horz_style='dotted')
        chart.legend(visible=True, font_size=14)           
        backtest_results = get_orders_from_backtesting(trades,symbol,lots=0.1)                              
        table,table_result = generate_tables_of_trades(chart,backtest_results)       
        chart.precision(2 if symbol == "XAUUSD" else 4)
        chart.show(block=True)   