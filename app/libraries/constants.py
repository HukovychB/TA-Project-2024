#Used in web.py
styles_option_menu = {
    "container": {
        "padding": "0!important",  
        "background-color": "#3f3b3b",  
    },
    "nav-link": {
        "font-size": "24px",  
        "text-align": "center", 
        "margin": "0px",  
        "color": "#f2e1e1",  
        "font-family": "serif", 
        "padding": "10px 20px", 
        "--hover-color": "#FF5500",
    },
    "nav-link-selected": {
        "background-color": "#FF5500",  
        "color": "white",  
    },
    "icon": {
        "color": "#f2e1e1", 
        "font-size": "20px"
    },
} 

#Used in main.py
styles_statistics_df = {
    'Total Return': lambda x: f'{x*100:.2f}%', 'Ann. Mean Return': lambda x: f'{x*100:.2f}%', 
    'St. Dev.': lambda x: f'{x*100:.2f}%', 'Max Drawdown': lambda x: f'{x*100:.2f}%',
    'Pct. Win. Trades': lambda x: f'{x*100:.2f}%', 'Pct. Losing Trades': lambda x: f'{x*100:.2f}%',
    'Num. Trades': '{:.0f}', 'Win. Trades': '{:.0f}', 'Losing Trades': '{:.0f}', 'Avg. Trade Duration': '{:.1f}',
    'Sharpe': '{:.2f}', 'Sortino': '{:.2f}', 'Win/Loss Ratio': '{:.2f}'
}
