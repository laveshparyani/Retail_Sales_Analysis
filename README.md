# Retail Sales Analysis Dashboard

A comprehensive retail sales analytics platform built with Python and Dash. This dashboard provides real-time insights into sales performance, customer behavior, and product trends through interactive visualizations and data analysis tools.

## 🚀 Features

- 📊 **Interactive Visualizations**: Real-time charts and graphs for sales analysis
- 🔍 **Advanced Filtering**: Filter data by date ranges, categories, and product types
- 📈 **Performance Metrics**: Track key performance indicators (KPIs) and trends
- 🎨 **Modern UI**: Clean, responsive interface built with Dash Bootstrap Components
- 🔄 **Real-time Updates**: Live data updates from SQL Server database
- 🛡️ **Data Validation**: Robust error handling and data validation
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- SQL Server (for database)
- ODBC Driver for SQL Server
- Git (for version control)

## 📦 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/Retail_Sales_Analysis.git
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

4. **Set up environment variables**:
Create a `.env` file in the root directory with the following variables:
```env
DB_SERVER=your_server_name
DB_NAME=your_database_name
```

5. **Test database connection**:
```bash
python src/test_db_connection.py
```

6. **Run the application**:
```bash
python src/app.py
```

The dashboard will be available at `http://localhost:8050`

## 🏗️ Project Structure

```
Retail_Sales_Analysis/
├── data/                  # Data files and resources
├── src/
│   ├── app.py            # Main application file
│   ├── test_db_connection.py  # Database connection testing
│   ├── static/           # Static assets (CSS, JS, images)
│   └── __pycache__/      # Python bytecode cache
├── .venv/                # Virtual environment
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 💻 Technology Stack

### Backend
- **Python**: Core programming language
- **Dash**: Web framework for building analytical applications
- **Pandas**: Data manipulation and analysis
- **SQLAlchemy**: Database ORM and connection management
- **PyODBC**: SQL Server connectivity

### Frontend
- **Dash Bootstrap Components**: UI components and styling
- **Plotly**: Interactive data visualization
- **CSS**: Custom styling and responsive design

### Database
- **SQL Server**: Data storage and management
- **OpenPyXL**: Excel file handling

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

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dash community for the amazing framework
- Plotly for the visualization tools
- SQLAlchemy team for the database ORM 