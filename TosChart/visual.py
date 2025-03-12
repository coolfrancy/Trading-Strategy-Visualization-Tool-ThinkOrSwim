def data(cleaned_data_path):
    import pandas as pd
    import os
    import traceback
    import matplotlib.pyplot as plt

    #refactor the who code to the new database


    #this will give you a list of stocks from the folder
    stocks=os.listdir(cleaned_data_path)

    lists=[]
    ####
    ##cleans all the strategy file so they match the same format
    ###
    for stock in stocks:
        try:
            dt=pd.read_csv(cleaned_data_path+'/'+stock)
            dt.drop(columns=['Price','Amount','Position','P/L', 'Unnamed: 9','Side'], inplace=True)

            symb=dt.columns[0]
            date=dt.columns[2]

            ####
            for ind,num in enumerate(dt[date]):
                if ind%2!=0:
                    if ind>0:
                        dt.loc[ind-1, date]+='-'+num

                #trying somethin

            dt['Trade P/L']=dt['Trade P/L'].shift(periods=-1)

            for i,id in enumerate(dt[symb]):
                if int(id)%2==0:
                    dt.drop(i, inplace=True)

            dt.dropna(inplace=True)
            hold=[]

            #creating holding period because i want to know how long i held the stock
            for index,date in enumerate(dt[date]):
                open, close=date.split('-')
                hold.append(pd.to_datetime(close)-pd.to_datetime(open))
            dt['Holding Time']=hold

            g=dt.columns[0].split()
            dt['Id']=g[1]
            dt.drop(columns=symb, inplace=True)
            lists.append(dt)
        except Exception as e:
            print(e)
            continue

    #added part for graphing stuff
    comb=pd.concat(lists)
    comb['Trade P/L'] = comb['Trade P/L'].str.replace(r'[\$,]', '', regex=True).replace(r'\((\d+(\.\d+)?)\)', r'-\1', regex=True)
    comb['Trade P/L']=pd.to_numeric(comb['Trade P/L'])

    comb['Trade P/L'].describe()
    sell=[]
    for num in comb['Date/Time']:
        b, s=num.split('-')
        sell.append(s)
    comb['Date']=sell
    df=comb

    # Ensure 'Date' is in datetime format and sort by date
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Calculate cumulative P/L
    df['Trade P/L'] = df['Trade P/L'].cumsum()

    # Plot the line graph
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Trade P/L'], marker='o', label='Cumulative P/L', color='blue')
    plt.axhline(0, color='red', linestyle='--', label='Break-Even Line')
    plt.title('Cumulative Profit/Loss Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Profit/Loss')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig('/workspaces/TosChartWeb/web/static/graph.png')





if __name__=='__main__':
    data('/workspaces/TosChartWeb/TosChart/cleaned_data')





