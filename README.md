# Budget Tracker - Web Application

A modern, browser-based personal finance management tool built with Streamlit.

## 🌟 Features

### 💰 **Transaction Management**
- Add income and expense transactions
- Multi-currency support (USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, INR, BRL, PKR)
- Automatic currency conversion to USD
- Real-time balance calculations

### 📊 **Data Visualization**
- **Balance Trend Chart**: Interactive line chart showing balance over time
- **Expense Breakdown**: Pie chart by category
- **Income vs Expenses**: Comparative bar chart
- Real-time chart updates as you add transactions

### 💾 **Data Management**
- **CSV Import/Export**: Load and save transaction data
- **Transaction History**: View, filter, and sort all transactions
- **Data Persistence**: Maintain data across sessions

### 🎨 **Modern Interface**
- Clean, responsive web design
- Mobile-friendly layout
- Interactive charts with Plotly
- Streamlit-powered interface

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd budget-tracker-cli
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

## 📖 Usage

### Adding Transactions
1. Use the sidebar form to add income or expense transactions
2. Select the transaction type (Income/Expense)
3. Enter the amount and description
4. Choose the currency
5. Click "Add Transaction"

### Viewing Data
- **Summary**: View total income, expenses, and balance at the top
- **Charts**: Interactive visualizations update automatically
- **Transaction History**: See all transactions in the main table
- **Filtering**: Use the transaction type filter to view specific categories

### Data Management
- **Export**: Download your data as CSV using the "Export to CSV" button
- **Import**: Upload a CSV file using the "Upload CSV" file uploader

## 🏗️ Project Structure

```
budget-tracker-cli/
├── streamlit_app.py         # Main Streamlit web application
├── requirements.txt         # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── .gitignore              # Git ignore file
├── README.md               # This file
└── src/                    # Backend logic
    ├── main.py            # CLI interface
    ├── models/            # Data models
    │   ├── __init__.py
    │   ├── budget_tracker.py  # Core business logic
    │   └── budget.py
    ├── commands/          # CLI commands
    │   ├── __init__.py
    │   └── cli.py
    └── utils/             # Utility functions
        ├── __init__.py
        └── file_handler.py
```

## 🌐 Deployment

### Streamlit Community Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy your repository
5. Share the public URL with others

### Local Network
The app automatically provides network URLs for sharing on your local network:
- **Local URL**: `http://localhost:8501`
- **Network URL**: `http://[your-ip]:8501`

## 🛠️ Technical Details

### Backend
- **BudgetTracker Class**: Core business logic for transaction management
- **Multi-currency Support**: Automatic conversion to USD using exchange rates
- **CSV Handling**: Import/export functionality for data persistence
- **Data Validation**: Input validation and error handling

### Frontend
- **Streamlit Framework**: Modern web interface
- **Plotly Charts**: Interactive data visualizations
- **Pandas Integration**: Efficient data handling and display
- **Responsive Design**: Works on desktop and mobile devices

### Dependencies
- `streamlit>=1.28.0` - Web application framework
- `pandas>=1.5.0` - Data manipulation and analysis
- `plotly>=5.15.0` - Interactive charts and visualizations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:
1. Check the [Issues](../../issues) section for existing problems
2. Create a new issue with a detailed description
3. Include your Python version and operating system information

---

**Happy budgeting! 💰📈**
  - Responsive layout with proper padding

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (included with most Python installations)

### Dependencies
Install required packages for charts and visualizations:
```bash
pip install matplotlib numpy
```

### Setup
1. Clone or download the project
2. Navigate to the project directory:
   ```bash
   cd budget-tracker-cli
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Mode (Default)
Launch the graphical interface:
```bash
python src/main.py
# or
python src/main.py --gui
```

### CLI Mode
Use the command-line interface:
```bash
python src/main.py --cli

# Then use subcommands:
python src/commands/cli.py add 50.00 "Food" --type Expense
python src/commands/cli.py add 1000.00 "Salary" --type Income
python src/commands/cli.py view
python src/commands/cli.py summary
python src/commands/cli.py clear
```

### GUI Usage Instructions
1. **Adding Transactions**:
   - Enter amount (numeric only)
   - Select or type category
   - Choose Income or Expense
   - Click "Add Transaction" or press Enter

2. **Viewing Data**:
   - Summary section shows real-time totals
   - Transaction list displays recent entries
   - Color coding: Green for income, Red for expenses

3. **Input Validation**:
   - Empty fields trigger error messages
   - Non-numeric amounts are rejected
   - Successful additions show confirmation

## Project Structure

```
python src/main.py
```

Follow the on-screen instructions to manage your budget.

## Directory Structure
```
budget-tracker-cli
├── src
│   ├── main.py          # Entry point of the application
│   ├── models           # Contains budget-related models
│   │   ├── __init__.py
│   │   └── budget.py    # Budget class for managing expenses
## Project Structure

```
budget-tracker-cli/
├── src/
│   ├── main.py                 # Main application entry point
│   ├── gui_app.py             # Tkinter GUI application
│   ├── models/
│   │   ├── __init__.py
│   │   ├── budget.py          # Legacy budget model
│   │   └── budget_tracker.py  # Enhanced Phase 1 model
│   ├── commands/
│   │   ├── __init__.py
│   │   └── cli.py             # CLI interface
│   └── utils/
│       ├── __init__.py
│       └── file_handler.py    # File operations (future use)
├── .vscode/
│   └── settings.json          # VS Code configuration
├── requirements.txt           # Project dependencies
├── setup.py                  # Package configuration
├── pyproject.toml            # Modern Python packaging
├── demo.py                   # Demonstration script
└── README.md                 # This file
```

## Technical Details

### Architecture
- **Model**: `BudgetTracker` class handles all business logic
- **View**: Tkinter GUI (`gui_app.py`) and CLI (`cli.py`)
- **Controller**: Main application (`main.py`) coordinates components

### Data Structure
Transactions are stored as dictionaries with the following structure:
```python
{
    'id': int,           # Unique transaction ID
    'amount': float,     # Transaction amount
    'category': str,     # Transaction category
    'type': str,         # 'Income' or 'Expense'
    'date': str          # ISO format datetime string
}
```

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Document functions with docstrings

## Future Enhancements (Phase 3+)
- Data persistence (JSON/CSV export/import)
- Advanced filtering and search capabilities
- Budget goals and spending alerts
- Enhanced chart types (spending trends, category comparisons)
- Monthly/yearly financial reports
- Data export for external analysis
- User authentication and profiles
- Mobile-responsive web interface

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the MIT License.

## Support
For questions or issues, please create an issue in the project repository.

---

**Budget Tracker App - Phase 2 Complete**  
*Advanced financial tracking with interactive charts and multi-currency support*

### 🎉 What's New in Phase 2:
✅ **Interactive Charts**: Pie, Bar, and Line charts with real-time updates  
✅ **Multi-Currency Support**: 10 major currencies with proper symbols  
✅ **Enhanced UI**: Professional layout with tabbed chart interface  
✅ **Visual Analytics**: Comprehensive expense analysis and trends  

Ready for Phase 3 enhancements!#   B u d g e t - T r a c k e t - P r o  
 