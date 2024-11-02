from django.shortcuts import render, redirect
from .forms import OptionParametersForm
from .models import OptionParameters, SimulationResults
import numpy as np
from datetime import datetime
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
import os
from .utils import get_stock_tickers

def heston_monte_carlo(S0, K, T, r, sigma, N=10):
    dt = T / 1000  # time step
    num_steps = int(T / dt)
    theta = 0.04 

    S = np.zeros((N, num_steps + 1))
    V = np.zeros((N, num_steps + 1))

    S[:, 0] = S0
    V[:, 0] = sigma ** 2  # Volatility squared

    for i in range(N):
        for j in range(1, num_steps + 1):
            Z1 = np.random.normal(0, 1)
            Z2 = np.random.normal(0, 1)
            V[i, j] = np.abs(V[i, j-1] + (theta - V[i, j-1]) * dt + np.sqrt(V[i, j-1]) * np.sqrt(dt) * Z2)
            S[i, j] = S[i, j-1] * np.exp((r - 0.5 * V[i, j-1]) * dt + np.sqrt(V[i, j-1]) * np.sqrt(dt) * Z1)

    payoffs = np.maximum(S[:, -1] - K, 0)
    option_price = np.exp(-r * T) * np.mean(payoffs)
    print(option_price)
    return option_price

def home(request):
    if request.method == 'POST':
        form = OptionParametersForm(request.POST)

        print(form.is_valid())
        if form.is_valid():
            option_parameters = form.save()
            print(option_parameters)
            # Run Monte Carlo simulation
            S0 = 100  # Initial stock price for simulation
            expiry_date = option_parameters.expiry_date
            T = (expiry_date - datetime.today().date()).days / 365.0  # Convert to years
            option_price = heston_monte_carlo(S0, float(option_parameters.strike_price), T, float(option_parameters.risk_free_rate), float(option_parameters.volatility))

            # Store the result
            SimulationResults.objects.create(option=option_parameters, option_price=option_price)
            stock_data = yf.download(option_parameters.ticker, start="2022-01-01", end=datetime.now().strftime('%Y-%m-%d'))

            # Create a plot
            plt.figure(figsize=(10, 5))
            plt.plot(stock_data['Close'], label='Close Price')
            plt.title(f'Historical Close Prices for {option_parameters.ticker}')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()
            
            # Save the plot to a file
            plots_dir = os.path.join('static', 'plots')
            if not os.path.exists(plots_dir):
                os.makedirs(plots_dir)
            plot_path = os.path.join('static', 'plots', f'{option_parameters.ticker}_historical_data.png')
            plt.savefig(plot_path)
            plt.close()  # Close the plot to free up memory
            return render(request, 'pricing/success.html', {
            'ticker': option_parameters.ticker,
            'expiry_date': option_parameters.expiry_date,
            'risk_free_rate': option_parameters.risk_free_rate,
            'volatility': option_parameters.volatility,
            'option_price' : option_price
        })
        else:
            print("Errors are ",form.errors)

    else:

        form = OptionParametersForm()

    return render(request, 'pricing/index.html', {'form': form})

def success(request):
    return render(request, 'pricing/success.html')
