import pickle
import pandas as pd
from datetime import date
from sklearn.ensemble import RandomForestClassifier,VotingClassifier
from sklearn.model_selection import GridSearchCV,cross_val_score
import glob
# Load the model to reverse
with open("Classes/Models/random_forest_59_historical_data.pkl", 'rb') as file:
    base_model = pickle.load(file)
# Load the model to detect the entry
with open("Classes/Models/random_forest_model-2024-07-16-predict_emtries.pkl", 'rb') as file:
    predict_entries_model = pickle.load(file)
def clean_order_column(value): 
    """
        Internal function encode data
    """   
    if value == 'BUY':
        return 1
    elif value == 'SELL':
        return 0
    else:
        return value
    
def get_original_signal(row):
    """
        Get original signal if the entry was reversed
    """
    if row['reverse']:
        if row['order'] == 1:
            return 0
        else:
            return 1
    else:
        return row['order']

def convert_to_seconds(value):
    """
        Convert time to ms to the model input
    """
    new_value = pd.to_datetime(value)
    return (new_value.hour * 60) + new_value.minute

def format_data_to_train_model(operations,operations_analyzed,symbol):
    """
        Prepare the data to train the model with the operations received from the backtesting period.
        The function will return 2 arrays:
            - Candles -> Array with encoded values from the strategy
            - Target -> Expeceted value from the model
    """    
    date_for_df = str(date.today())
    dfs = []
    points_for_id = 0
    for i,key in enumerate(operations.keys()):
        df = operations[key]["df_strategy"].drop(columns={"Sell","Buy","SL","TP","SL1",	"TP1"})
        if key in operations_analyzed.keys():
            df["result"] = operations_analyzed[key]["result"]
            df["reverse"] = operations[key]["reversed"]
            df["points"] = operations[key]["points"]
            df["symbol"] = symbol
            df["order"] = operations[key]["type"]            
            points_for_id = operations[key]["points"]
            df["ID"] = symbol+"-"+date_for_df+"-"+str(points_for_id)+"backtest"+"-"+str(i)
            dfs.append(df)
    # Combine all the entries and format to split the data
    df = pd.concat(dfs).reset_index()    
    df["order"] = df["order"].apply(clean_order_column)    
    symbols_encoding = {"XAUUSD": 1, "EURUSD": 0}
    df["symbol"] = df["symbol"].apply(lambda x: symbols_encoding[x])
    df["signal"] = df.apply(get_original_signal, axis=1)    
    df["time"] = df["time"].apply(lambda x: convert_to_seconds(x))
    # Reduce by IDS and generate the arrays
    IDS = set(df["ID"])
    arrays = []
    targets = []
    ids = []
    columns = ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread','real_volume', 'points', 'symbol', "signal"]
    for id in IDS:        
        shape = df[df["ID"] == id].shape  
        if shape[0] != 100:
            print(shape)  
            print(id)
        reverse = df[df["ID"] == id]["reverse"].iloc[0] 
        result = df[df["ID"] == id]["result"].iloc[0] == "WIN"         
        ids.append(id)
        arrays.append(df[df["ID"] == id][columns].to_numpy())         
        if result:
            targets.append(reverse)
        else:
            targets.append(not reverse)        
    # Create the DataFrame with IDs grouped   
    df_for_ml = pd.DataFrame({"ID":ids,"Array":arrays,"Target":targets}) 
    # Split into arrays to train the model
    target = df_for_ml["Target"].values
    candles = [array.flatten() for array in df_for_ml["Array"].values]  
    return candles, target    

def train_random_forest(candles, target):   
    # Entrenar el modelo
    model = RandomForestClassifier(n_estimators=100, random_state=24,max_depth=10)
    model.fit(candles, target)    
    return model

def inputs_for_random_forest(df,order,symbol,points):
    """
        Add the features to the DataFrame and converts to a numpy array to use as input for the model
    """
    symbols_encoding = {"XAUUSD": 1, "EURUSD": 0}
    new_df = df.reset_index()
    # Add features to the DataFrame
    new_df["signal"] = order
    new_df["symbol"] = symbols_encoding[symbol]
    new_df["points"] = points
    columns = ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread','real_volume', 'points', 'symbol', "signal"]    
    # Convert time to seconds   
    new_df["time"] = new_df["time"].apply(lambda x: (pd.to_datetime(x).hour * 60) + pd.to_datetime(x).minute)    
    return new_df[columns].to_numpy()

def inputs_for_random_forest_v2(df,symbol,points):
    """
        Add the features to the DataFrame and converts to a numpy array to use as input for the model
    """
    symbols_encoding = {"XAUUSD": 1, "EURUSD": 0}
    new_df = df.reset_index()
    # Add features to the DataFrame    
    new_df["symbol"] = symbols_encoding[symbol]
    new_df["points"] = points
    columns = ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread','real_volume', 'points', 'symbol']    
    # Convert time to seconds   
    new_df["time"] = new_df["time"].apply(lambda x: (pd.to_datetime(x).hour * 60) + pd.to_datetime(x).minute)    
    return new_df[columns].to_numpy()

def get_prediction(input_model,model=base_model):    
    """
        use the pre loaded model to predict the entry
    """ 
    if model == "predict_entries_model":
        model = predict_entries_model
    return model.predict(input_model.reshape(1,-1))[0]

def ensemble_models(recent_model,inputs,target):
    """
        Combine predictions of the base model trained with historical data and recent model to improve the accuracy
    """    
    params = {        
        'weights': [(1,1),(1,2),(1,3),(1,4),(4,1),(3,1),(2,1)]
    }
    models_path = [model for model in glob.glob("Classes/Models/*.pkl")]
    models = []
    for i in range(len(models_path)):
        with open(models_path[i],'rb') as file:
            current = pickle.load(file)
            models.append(current)
        name = models_path[i].split("_")[3:]
        print(f'Acurracy {name}: {cross_val_score(current,inputs,target,cv=3).mean()}')           
    print(f'Acurracy current model: {cross_val_score(recent_model,inputs,target,cv=3).mean()}')    
    # Input for the voting_classifier
    models_for_voting_classifier = [(f"model {idx}",model) for idx,model in enumerate(models)] + [('recent',recent_model)]
    
    models_combined = VotingClassifier(models_for_voting_classifier,voting='soft',weights=(1,1,1,3))
    # # perfom GridSearch
    # grid = GridSearchCV(models_combined,params,cv=3,n_jobs=-1,verbose=2)
    # grid.fit(inputs,target)
    # best_params = grid.best_params_    
    # print(best_params)
    # models_combined.set_params(weights=best_params["weights"])    
    print(f'Acurracy combined model: {cross_val_score(models_combined,inputs,target,cv=3).mean()}')
    return models_combined