from django.shortcuts import render, redirect
import requests
from .forms import StockTickerForm
from datetime import datetime
from collections import OrderedDict
import json
from decouple import config


# Create your views here.

# get the api_key from .env file
api_key = config('api_key')

# the landing page of the website
def homeView(request):
    return render(request, "home.html")

# Getting Started page - A dropdown list is displayed, and user can choose any stock ticker.
def select_stock_ticker(request):
    if request.method == 'POST':
        form = StockTickerForm(request.POST)
        if form.is_valid():
            selected_ticker = form.cleaned_data['ticker']
            # Redirect to the details page with the selected ticker
            return redirect('stock_details', ticker = selected_ticker)
    else:
        form = StockTickerForm()

    return render(request, 'form.html', {'form': form})

# displays the stock details for the selected stock ticker
def stock_details(request, ticker):
    
    # api_key = 'demo'  
    url_stock_data = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}'
    
    # Make a request to the API to fetch company information
    response = requests.get(url_stock_data)
        
    if response.status_code == 200:
        stock_data = response.json()
                
        # formatting some values
        market_cap = currency_format(stock_data["MarketCapitalization"])
        ebitda = currency_format(stock_data["EBITDA"])
        QuarterlyEarningsGrowthYOY = decimal_to_percentage(stock_data["QuarterlyEarningsGrowthYOY"])
        QuarterlyRevenueGrowthYOY = decimal_to_percentage(stock_data["QuarterlyRevenueGrowthYOY"])
        ProfitMargin = decimal_to_percentage(stock_data["ProfitMargin"])
        OperatingMarginTTM = decimal_to_percentage(stock_data["OperatingMarginTTM"])
        ReturnOnEquityTTM = decimal_to_percentage(stock_data["ReturnOnEquityTTM"])
        
    else:
        stock_data = {'error': 'Unable to fetch data.'}

    context = {
        'stock_data': stock_data,
        'market_cap': market_cap,
        'ebitda': ebitda,
        'QuarterlyEarningsGrowthYOY': QuarterlyEarningsGrowthYOY,
        'QuarterlyRevenueGrowthYOY': QuarterlyRevenueGrowthYOY,
        'ProfitMargin': ProfitMargin,
        'OperatingMarginTTM': OperatingMarginTTM,
        'ReturnOnEquityTTM': ReturnOnEquityTTM,
        
    }
    return render(request, 'stock-details.html', context)

# displays the stock analysis for the selected stock ticker
def analyze_stock(request, ticker = None):
    if ticker:
        # Analyze stock using the ticker
        # api_key = 'demo'
        
        # all the URLs needed for a request
        url_last_hour = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={api_key}"
        url_current_stock = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"
        url_last_one_week = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
        url_last_one_year = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={api_key}"

        
        # Make a request to the APIs
        response_last_hour = requests.get(url_last_hour)
        response_last_one_week = requests.get(url_last_one_week)
        response_last_one_year = requests.get(url_last_one_year)
        response_current_stock = requests.get(url_current_stock)
        
        ############# retrieves data for the last 1 hour ###################
                   
        stock_data_last_hour = response_last_hour.json()
        
        # Extract Time Series Data
        time_series_hour = stock_data_last_hour["Time Series (5min)"]

        # Sort the data by the timestamps to ensure it's in chronological order
        sorted_time_series = OrderedDict(sorted(time_series_hour.items(), reverse = True))

        # Get the last 12 data points (for the last 1 hour)
        last_hour_data = list(sorted_time_series.items())[:12]

        # Prepare the data for the chart
        timestamps_last_hour = []
        high_prices_last_hour = []
        
        for time, data in last_hour_data:
            timestamps_last_hour.append(time)
            high_prices_last_hour.append(data["2. high"]) 
             
        #################################################################
        
        ######### retrieves current stock high and low ##################
        
        current_stock = response_current_stock.json()["Global Quote"]
        high = current_stock['03. high']
        low = current_stock['04. low']   
        date = format_date(current_stock["07. latest trading day"])  
        
        #################################################################
        
        ######### retrieves data for the last 1 Week ####################
        
        stock_data_last_week = response_last_one_week.json()
        
        # Extract Time Series Data
        time_series_week = stock_data_last_week["Time Series (Daily)"]

        # Sort the data by the timestamps to ensure it's in chronological order
        sorted_time_series_week = OrderedDict(sorted(time_series_week.items(), reverse = True))

        # Get the last 12 data points (for the last 1 hour)
        last_week_data = list(sorted_time_series_week.items())[:7]

        # Prepare the data for the chart
        timestamps_last_week = []
        high_prices_last_week = []
        
        for time, data in last_week_data:
            timestamps_last_week.append(time)
            high_prices_last_week.append(data["2. high"])
            
        #################################################################
        
        ######### retrieves data for the last 1 Year ####################
        
        stock_data_last_year = response_last_one_year.json()
        
        # Extract Time Series Data
        time_series_year = stock_data_last_year["Monthly Time Series"]

        # Sort the data by the timestamps to ensure it's in chronological order
        sorted_time_series_year = OrderedDict(sorted(time_series_year.items(), reverse = True))

        # Get the last 12 data points (for the last 1 hour)
        last_year_data = list(sorted_time_series_year.items())[:12]

        # Prepare the data for the chart
        timestamps_last_year = []
        high_prices_last_year = []
        
        for time, data in last_year_data:
            timestamps_last_year.append(time)
            high_prices_last_year.append(data["2. high"])
            
        #################################################################
        
    
    symbol = stock_data_last_hour["Meta Data"]["2. Symbol"]
    latest_date = stock_data_last_hour["Meta Data"]["3. Last Refreshed"]
    time_zone = stock_data_last_hour["Meta Data"]["6. Time Zone"]
            
    context = {
            'timestamps_last_hour': json.dumps(timestamps_last_hour),
            'high_prices_last_hour': json.dumps(high_prices_last_hour),
            'timestamps_last_week': json.dumps(timestamps_last_week),
            'high_prices_last_week': json.dumps(high_prices_last_week),
            'timestamps_last_year': json.dumps(timestamps_last_year),
            'high_prices_last_year': json.dumps(high_prices_last_year),
            'symbol': symbol,
            'latest_date': format_date_and_time(latest_date),
            'time_zone': time_zone,
            'high': high,
            'low': low,
            'date': date,
        } 
    
    return render(request, 'analyze.html', context)

def top_stock_gainer_loser(request):
    
    # api_key = "demo"
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}"
    
    response = requests.get(url)
    
    top_stock_data = response.json()
    
    top_gainers = top_stock_data["top_gainers"][:9]
    top_losers = top_stock_data["top_losers"][:9]
    
    date_data = top_stock_data["last_updated"]   
    stripped_datetime = ' '.join(date_data.split()[:2])
    stripped_timezone = ''.join(date_data.split()[2])
    
    last_updated = format_date_and_time(stripped_datetime)
    time_zone = stripped_timezone
            
    context = {
        "top_gainers": top_gainers,
        "top_losers": top_losers,
        "last_updated": last_updated,
        "time_zone": time_zone,
    }
    return render(request, 'stock-gainer-loser.html', context)

def get_news(request):
    
    # api_key = 'demo'
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=financial_markets&apikey={api_key}'
    
    response = requests.get(url)
    
    news_data = response.json()
    
    news_feeds = news_data["feed"][:10]
        
        
    context = {
        'news_feeds': news_feeds,
    }
    
    return render(request, 'news.html', context)


################### formatting functions #########################################
def currency_format(value):
    
    formatted_value = "${:,.2f} billion".format(int(value) / 1_000_000_000)
    return str(formatted_value)

def decimal_to_percentage(decimal_value):
    
    percentage_value = float(decimal_value) * 100
    return f"{percentage_value:.{2}f}%"

def format_date(date_str):
    
    # Convert string to datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Format the date as desired
    formatted_date = date_obj.strftime("%B %-d, %Y")

    # Add suffix for the day
    day = date_obj.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    # Final formatted string
    formatted_date = f"{date_obj.strftime('%B')} {day}{suffix}, {date_obj.year}"

    return formatted_date

def format_date_and_time(date_str):
    
    # Convert the string into a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Format the datetime object into a more readable format
    formatted_date = date_obj.strftime("%B %d, %Y at %I:%M %p")

    return formatted_date