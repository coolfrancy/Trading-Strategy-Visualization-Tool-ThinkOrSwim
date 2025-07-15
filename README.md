# Trading Strategy Visualization Tool (ThinkOrSwim)

A web-based visualization platform for analyzing back-tested trading strategy data from ThinkOrSwim

## Overview

This tool transforms raw ThinkOrSwim back-testing data into interactive visual charts and dashboards, allowing traders to easily analyze performance metrics, identify patterns, and optimize their trading strategies. The core functionality is the ability to combine and visualize strategies across multiple stocks, providing a comprehensive view of how a single strategy performs across different securities or how multiple strategies compare across the same set of stocks.

## Features

- **Multi-Stock Strategy Analysis**: Analyze how a single trading strategy performs across multiple stocks simultaneously
- **Strategy Aggregation**: View combined performance metrics across a portfolio of stocks
- **Data Import**: Seamlessly import back-tested data from ThinkOrSwim
- **Interactive Visualizations**: Dynamic charts showing performance metrics, drawdowns, win/loss ratios, etc.
- **Strategy Comparison**: Compare multiple trading strategies side by side
- **Performance Metrics**: Calculate key statistics including Sharpe ratio, max drawdown, win rate, etc.
- **Responsive Design**: Fully functional across desktop and mobile devices

## Technology Stack

- **Backend**: Python with Flask and Django
- **Data Processing**: pandas for data manipulation and analysis
- **Frontend**: HTML, CSS
- **Charts**: Matplotlib / Plotly / Bokeh

## Installation

```bash
# Clone the repository
git clone https://github.com/coolfrancy/Trading-Strategy-Visualization-Tool-ThinkOrSwim.git

# Navigate to project directory
cd Trading-Strategy-Visualization-Tool-ThinkOrSwim

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

## Usage

1. Export your back-testing data from ThinkOrSwim
2. Upload the data file through the web interface
3. Analyze the results through the interactive dashboard

## Future Enhancements

- Export reports as PDF/CSV
- Custom indicator overlay options
- Real-time data integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Francy Romelus - francyromelus@gmail.com

Project Link: https://github.com/coolfrancy/Trading-Strategy-Visualization-Tool-ThinkOrSwim.git