import re
import pandas as pd

def preprocess(data):
    """
    Preprocess WhatsApp chat exported text into a DataFrame with columns:
    ['user', 'user_message', 'message', 'only_date', 'day_name', 'only_year', 'only_month', 'hour', 'minute']
    """

    # 1️⃣ Regex to match WhatsApp timestamp
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    # 2️⃣ Split messages and extract dates
    messages = re.split(pattern, data)[1:]  # first element is empty
    dates = re.findall(pattern, data)
    
    # 3️⃣ Create DataFrame
    df = pd.DataFrame({
        'user_message': messages,
        'date': pd.to_datetime(
            dates,
            format='%d/%m/%Y, %H:%M - ',
            errors='coerce'
        )
    })
    
    # 4️⃣ Split user and message
    def split_user_message(text):
        if ": " in text:
            user, message = text.split(": ", 1)
        else:
            user, message = "system_notification", text
        return pd.Series([user, message])
    
    df[['user', 'message']] = df['user_message'].apply(split_user_message)
    
    # 5️⃣ Add time-related columns
    df['only_date'] = df['date'].dt.date
    df["month_num"]= df['date'].dt.month
    df['month'] = df['date'].dt.strftime("%B")
    df['day_name'] = df['date'].dt.day_name()
    df['year'] = df['date'].dt.year
    df['only_month'] = df['date'].dt.month_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
   # df['year'] = df['date'].dt.year  
    
    # 6️⃣ Keep 'user_message' for backward compatibility
    # Drop only 'date' if you want
    df.drop(columns=['date'], inplace=True)
    
    return df
