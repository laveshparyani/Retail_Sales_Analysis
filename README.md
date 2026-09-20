# Retail Sales Analysis Dashboard

A comprehensive retail sales analytics platform built with Python and Dash. This dashboard provides real-time insights into sales performance, customer behavior, and product trends through interactive visualizations and data analysis tools.

## 🌐 Live Demo

**https://retail-sales-analysis-6ii2.onrender.com**

> Hosted on Render's free tier, so the first request after a period of inactivity can take up to ~50 seconds to wake the instance. It is fast after that.

## 🚀 Features

- 📊 **Interactive Visualizations**: Real-time charts and graphs for sales analysis
- 🔍 **Advanced Filtering**: Filter data by date ranges, categories, and product types
- 📈 **Performance Metrics**: Track key performance indicators (KPIs) and trends
- 🎨 **Modern UI**: Clean, responsive interface built with Dash Bootstrap Components
- 🔄 **Live Reload**: Data refreshes from a bundled sample dataset (CSV + Excel)
- 🛡️ **Data Validation**: Robust error handling and data validation
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Git (for version control)

## 📦 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/laveshparyani/Retail_Sales_Analysis.git
cd Retail_Sales_Analysis
```

2. **Create and activate virtual environment**:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python src/app.py
```

The dashboard will be available at `http://localhost:8050`. No database setup is needed - the app reads the sample data in the `data/` folder.

## 🏗️ Project Structure

```
Retail_Sales_Analysis/
├── data/                 # Sample dataset
│   ├── customers.csv     # Reference customers
│   ├── products.csv      # Reference products (category, price)
│   └── sales_data.xlsx   # Sales records
├── src/
│   ├── app.py            # Main Dash application
│   └── static/css/       # Custom styles
├── .github/              # Community health files + CI/CodeQL workflows
├── requirements.txt      # Python dependencies
├── render.yaml           # Render deployment config
└── README.md             # Project documentation
```

## 💻 Technology Stack

### Backend
- **Python**: Core programming language
- **Dash**: Web framework for building analytical applications
- **Pandas**: Data manipulation and analysis

### Frontend
- **Dash Bootstrap Components**: UI components and styling
- **Plotly**: Interactive data visualization
- **CSS**: Custom styling and responsive design

### Data
- **CSV + Excel**: Bundled sample dataset in the `data/` folder
- **Pandas + OpenPyXL**: Data loading and analysis

## 📚 How to Use

1. **Data Analysis**:
   - Use the date range picker to select your analysis period
   - Apply filters to focus on specific products or categories
   - View real-time updates of sales metrics

2. **Visualizations**:
   - Interact with charts by hovering over data points
   - Zoom in/out of graphs for detailed analysis
   - Export visualizations as images or PDFs

3. **Performance Metrics**:
   - Monitor key performance indicators in real-time
   - Compare metrics across different time periods
   - Track sales trends and patterns

## 🔧 Development

### Running in Development Mode
```bash
python src/app.py
```

### Debugging
- Use the Dash debug mode for detailed error messages
- Check the browser console for frontend errors
- Monitor the Python console for backend errors

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Licensed under the [MIT License](LICENSE).

## 👤 Author

**Lavesh Paryani** - [@laveshparyani](https://github.com/laveshparyani)

## 🙏 Acknowledgments

- Dash community for the framework
- Plotly for the visualization tools
