def data(cleaned_data_path, phases_path=''):
    import pandas as pd
    import os
    import matplotlib.pyplot as plt
    from TosChart.summary import Summary
    from datetime import datetime

    chart_path = os.path.join(os.getcwd(), "web", "static", "graph.png")  

    # US Recession periods (NBER official dates)
    recession_periods = [
        ('2001-03-01', '2001-11-30'),  # Dot-com crash
        ('2007-12-01', '2009-06-30'),  # Great Recession
        ('2020-02-01', '2020-04-30'),  # COVID-19 recession
    ]

    #refactor the who code to the new database

    #this will give you a list of stocks from the folder
    stocks=os.listdir(cleaned_data_path)
    #include phases only if user wants to add
    if phases_path!='':
        phases=os.listdir(phases_path)

    def create_dataframe(stocks, data_path):
        lists=[]
        ####
        ##cleans all the strategy file so they match the same format
        ###
        for stock in stocks:
            try:
                dt=pd.read_csv(data_path+'/'+stock)
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
                
        df=pd.concat(lists)
        df['Trade P/L'] = df['Trade P/L'].str.replace(r'[\$,]', '', regex=True).replace(r'\((\d+(\.\d+)?)\)', r'-\1', regex=True)
        df['Trade P/L']=pd.to_numeric(df['Trade P/L'])

        sell=[]

        for num in df['Date/Time']:
            b, s=num.split('-')
            sell.append(s)
        df['Date']=sell

        # Ensure 'Date' is in datetime format and sort by date
        df = df.assign(Date=pd.to_datetime(df['Date'])).sort_values('Date')                

        return df

    def filter_trades_by_phases(main_df, phase_df):
        """
        Filter main trading data to only include trades that occurred during phase periods
        """
        if phase_df is None or phase_df.empty:
            return main_df
        
        # Extract phase periods from phase dataframe
        phase_periods = []
        for _, row in phase_df.iterrows():
            phase_start, phase_end = row['Date/Time'].split('-')
            phase_periods.append((pd.to_datetime(phase_start), pd.to_datetime(phase_end)))
        
        # Filter main dataframe trades that fall within any phase period
        filtered_trades = []
        
        for _, trade in main_df.iterrows():
            trade_start, trade_end = trade['Date/Time'].split('-')
            trade_start_date = pd.to_datetime(trade_start)
            trade_end_date = pd.to_datetime(trade_end)
            
            # Check if trade overlaps with any phase period
            for phase_start, phase_end in phase_periods:
                # Trade overlaps if it starts before phase ends and ends after phase starts
                if trade_start_date <= phase_end and trade_end_date >= phase_start:
                    filtered_trades.append(trade)
                    break  # Found overlap, no need to check other phases
        
        if filtered_trades:
            filtered_df = pd.DataFrame(filtered_trades).reset_index(drop=True)
            # Recalculate the Date column for the filtered data
            sell_dates = []
            for num in filtered_df['Date/Time']:
                b, s = num.split('-')
                sell_dates.append(s)
            filtered_df['Date'] = pd.to_datetime(sell_dates)
            filtered_df = filtered_df.sort_values('Date')
            return filtered_df
        else:
            # Return empty dataframe with same structure if no trades found
            return main_df.iloc[0:0].copy()


    # Create main dataframe
    df = create_dataframe(stocks, cleaned_data_path)

    # Create phase dataframe if phases_path is provided
    if phases_path != '':
        p_df = create_dataframe(phases, phases_path)
        # Filter main dataframe to only include trades during phase periods
        df = filter_trades_by_phases(df, p_df)
        plot_title = 'Cumulative P/L During Phase Periods with Recession Periods'
    else:
        p_df = None
        plot_title = 'Cumulative Profit/Loss Over Time with Recession Periods'

    # Check if we have any data after filtering
    if df.empty:
        print("No trades found during the specified phase periods.")
        return None

    # Calculate cumulative P/L
    df['Trade Sum'] = df['Trade P/L'].cumsum()
    
    ######
    #max drawdown calculation
    df['Running Max'] = df['Trade Sum'].cummax()
    df['Drawdown'] = df['Trade Sum'] - df['Running Max']
    max_drawdown = df['Drawdown'].min()  # Most negative value
    max_drawdown_pct = (max_drawdown / df['Running Max'].max()) * 100 if df['Running Max'].max() != 0 else 0
    ######

    # Plot and save the line graph
    plt.figure(figsize=(12, 8))
    
    # Plot the main line
    plt.plot(df['Date'], df['Trade Sum'], marker='o', label='Cumulative P/L', color='blue', linewidth=2, markersize=4)
    
    # Add recession periods as shaded areas
    for start_date, end_date in recession_periods:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        # Only shade if the recession period overlaps with our data
        if start <= df['Date'].max() and end >= df['Date'].min():
            plt.axvspan(start, end, alpha=0.3, color='red', label='Recession Period' if start_date == recession_periods[0][0] else "")
    
    # Add labels for recession periods
    recession_labels = {
        '2001-03-01': '2001 Crash',
        '2007-12-01': '2007 Crash', 
        '2020-02-01': '2020 Crash'
    }
    
    # Add text labels for recessions
    for start_date, end_date in recession_periods:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        # Only add labels if within our data range
        if start <= df['Date'].max() and end >= df['Date'].min():
            # Position label in the middle of the recession period
            mid_date = start + (end - start) / 2
            
            # Get y position for label (top of chart)
            y_pos = plt.ylim()[1] * 0.9
            
            # Add text label
            plt.text(mid_date, y_pos, recession_labels[start_date], 
                    rotation=0, ha='center', va='top', fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor='red'))

    # Add phase periods as shaded areas if phases are provided
    if phases_path != '' and p_df is not None and not p_df.empty:
        plt.plot([], [], color='green', alpha=0.2, linewidth=10, label='Phase Period')
        for _, phase_row in p_df.iterrows():
            phase_start_str, phase_end_str = phase_row['Date/Time'].split('-')
            phase_start = pd.to_datetime(phase_start_str)
            phase_end = pd.to_datetime(phase_end_str)
            
            # Only shade if the phase period overlaps with our filtered data
            if phase_start <= df['Date'].max() and phase_end >= df['Date'].min():
                plt.axvspan(phase_start, phase_end, alpha=0.2, color='green', 
                        label='Phase Period' if phase_row.name == p_df.index[0] else "")
    
    plt.axhline(0, color='red', linestyle='--', label='Break-Even Line')
    plt.title(plot_title, fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Profit/Loss', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)

    # Set the background color to light grey
    plt.gca().set_facecolor('lightgrey')  # Chart area background
    plt.gcf().patch.set_facecolor('lightgrey')  # Figure background

    # Format y-axis to show dollar signs
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')

    #calculates winners and losers
    wins = df[df['Trade P/L'] > 0]['Trade P/L']
    losses = df[df['Trade P/L'] < 0]['Trade P/L']

    count_win, count_loss = len(wins), len(losses)
    sum_win, sum_loss = wins.sum(), losses.sum()

    # Handle division by zero
    average_win = sum_win / count_win if count_win > 0 else 0
    average_loss = sum_loss / count_loss if count_loss > 0 else 0
    amount_ratio = round(average_win / abs(average_loss), 2) if average_loss != 0 else 0
    win_loss_percentage = round((count_win / (count_loss + count_win)) * 100, 2) if (count_loss + count_win) > 0 else 0

    #gives you information on data
    desc_dict = df['Trade P/L'].describe().to_dict()
    description = []
    for name, value in desc_dict.items():
        if '%' not in name:
            description.append(name + ' ' + str(value))
            
    summary = Summary(count_win, count_loss, win_loss_percentage, amount_ratio, max_drawdown_pct)

    return summary

if __name__ == '__main__':
    data('/workspaces/TosChartWeb/TosChart/cleaned_data')