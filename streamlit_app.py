"""
Budget Tracker - Streamlit Web Application
A modern, browser-based personal finance management tool
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import sys
import os
from typing import Dict, List, Optional
import io
import base64

# Add the src directory to the Python path for backend imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import backend logic
try:
    from models.budget_tracker import BudgetTracker
except ImportError:
    st.error("Backend modules not found. Please ensure the src/models directory exists.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Budget Tracker Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .success-metric {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
    }
    .danger-metric {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
    }
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitBudgetTracker:
    """Streamlit wrapper for the Budget Tracker application"""
    
    def __init__(self):
        # Initialize session state
        self.init_session_state()
        
        # Load or create budget tracker instance
        self.load_tracker()
    
    def init_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'budget_tracker' not in st.session_state:
            st.session_state.budget_tracker = BudgetTracker()
        
        if 'base_currency' not in st.session_state:
            st.session_state.base_currency = "USD"
        
        if 'filter_type' not in st.session_state:
            st.session_state.filter_type = "All"
        
        if 'filter_category' not in st.session_state:
            st.session_state.filter_category = "All"
    
    def load_tracker(self):
        """Load the budget tracker from session state"""
        self.tracker = st.session_state.budget_tracker
    
    def save_tracker(self):
        """Save the budget tracker to session state"""
        st.session_state.budget_tracker = self.tracker

    def render_header(self):
        """Render the application header"""
        st.markdown('<h1 class="main-header">💰 Budget Tracker Pro</h1>', unsafe_allow_html=True)
        st.markdown("---")

    def render_sidebar(self):
        """Render the sidebar with settings and controls"""
        st.sidebar.title("⚙️ Settings & Controls")
        
        # Base currency selection
        st.sidebar.subheader("💱 Base Currency")
        currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "BRL", "PKR"]
        st.session_state.base_currency = st.sidebar.selectbox(
            "Select base currency for conversions:",
            currencies,
            index=currencies.index(st.session_state.base_currency)
        )
        
        # Data management
        st.sidebar.subheader("📁 Data Management")
        
        # Export data
        if st.sidebar.button("📥 Export Data to CSV"):
            self.export_data()
        
        # Import data
        st.sidebar.subheader("📤 Import Data")
        uploaded_file = st.sidebar.file_uploader(
            "Choose a CSV file to import:",
            type=['csv'],
            help="Upload a CSV file with transaction data"
        )
        
        if uploaded_file is not None:
            self.import_data(uploaded_file)
        
        # Clear all data
        st.sidebar.subheader("🗑️ Reset Data")
        if st.sidebar.button("Clear All Transactions", type="secondary"):
            if st.sidebar.checkbox("I understand this will delete all data"):
                self.tracker.transactions = []
                self.save_tracker()
                st.rerun()
        
        # Statistics
        st.sidebar.subheader("📊 Quick Stats")
        total_transactions = len(self.tracker.get_transactions())
        st.sidebar.metric("Total Transactions", total_transactions)
        
        if total_transactions > 0:
            summary = self.tracker.get_summary()
            st.sidebar.metric(
                "Net Balance", 
                f"${summary['net_balance']:,.2f}",
                delta=f"${summary['net_balance']:,.2f}" if summary['net_balance'] >= 0 else None
            )

    def render_transaction_input(self):
        """Render the transaction input section"""
        st.subheader("➕ Add New Transaction")
        
        with st.form("transaction_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                amount = st.number_input(
                    "Amount",
                    min_value=0.01,
                    value=0.01,
                    step=0.01,
                    format="%.2f",
                    help="Enter the transaction amount"
                )
                
                transaction_type = st.selectbox(
                    "Type",
                    ["Income", "Expense"],
                    help="Select transaction type"
                )
            
            with col2:
                # Get categories based on transaction type
                categories = self.tracker.get_categories(transaction_type)
                if categories:
                    category = st.selectbox(
                        "Category",
                        [""] + categories,
                        help="Select or enter a category"
                    )
                    if category == "":
                        category = st.text_input("Custom Category", placeholder="Enter new category")
                else:
                    category = st.text_input("Category", placeholder="Enter category name")
                
                currency = st.selectbox(
                    "Currency",
                    ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "BRL", "PKR"],
                    help="Select transaction currency"
                )
            
            with col3:
                transaction_date = st.date_input(
                    "Date",
                    value=date.today(),
                    help="Select transaction date"
                )
                
                st.write("")  # Spacing
                st.write("")  # Spacing
                submit_button = st.form_submit_button(
                    "Add Transaction",
                    type="primary",
                    use_container_width=True
                )
            
            # Process form submission
            if submit_button:
                if amount > 0 and category.strip():
                    success = self.tracker.add_transaction(
                        amount=amount,
                        category=category.strip(),
                        transaction_type=transaction_type,
                        currency=currency,
                        transaction_date=transaction_date.strftime("%Y-%m-%d")
                    )
                    
                    if success:
                        self.save_tracker()
                        st.success(f"✅ Added {transaction_type.lower()}: {category} - {currency} {amount:,.2f}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add transaction. Please check your inputs.")
                else:
                    st.error("❌ Please enter a valid amount and category.")

    def render_summary_metrics(self):
        """Render the financial summary using metrics"""
        st.subheader("📊 Financial Summary")
        
        summary = self.tracker.get_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Total Income",
                value=f"${summary['total_income']:,.2f}",
                delta=f"+${summary['total_income']:,.2f}" if summary['total_income'] > 0 else None
            )
        
        with col2:
            st.metric(
                label="💸 Total Expenses",
                value=f"${summary['total_expenses']:,.2f}",
                delta=f"-${summary['total_expenses']:,.2f}" if summary['total_expenses'] > 0 else None
            )
        
        with col3:
            balance = summary['net_balance']
            st.metric(
                label="💵 Net Balance",
                value=f"${balance:,.2f}",
                delta=f"${balance:,.2f}",
                delta_color="normal" if balance >= 0 else "inverse"
            )
        
        with col4:
            # Calculate savings rate
            if summary['total_income'] > 0:
                savings_rate = (balance / summary['total_income']) * 100
                st.metric(
                    label="📈 Savings Rate",
                    value=f"{savings_rate:.1f}%",
                    delta=f"{savings_rate:.1f}%" if savings_rate >= 0 else None
                )
            else:
                st.metric(
                    label="📈 Savings Rate",
                    value="0.0%"
                )

    def render_transaction_history(self):
        """Render the transaction history table with filtering"""
        st.subheader("📋 Transaction History")
        
        transactions = self.tracker.get_transactions()
        
        if not transactions:
            st.info("No transactions found. Add your first transaction above!")
            return
        
        # Create DataFrame
        df_data = []
        for t in transactions:
            # Convert to base currency for comparison
            usd_amount = self.tracker.convert_to_usd(t['amount'], t.get('currency', 'USD'))
            
            df_data.append({
                'Date': t['date'][:10] if 'date' in t else 'N/A',
                'Type': t['type'],
                'Category': t['category'],
                'Amount': f"{t.get('currency', 'USD')} {t['amount']:,.2f}",
                'USD Equivalent': f"${usd_amount:.2f}",
                'Currency': t.get('currency', 'USD')
            })
        
        df = pd.DataFrame(df_data)
        
        # Filtering options
        col1, col2 = st.columns(2)
        with col1:
            type_filter = st.selectbox(
                "Filter by Type:",
                ["All", "Income", "Expense"],
                key="type_filter"
            )
        
        with col2:
            categories = ["All"] + list(set(t['category'] for t in transactions))
            category_filter = st.selectbox(
                "Filter by Category:",
                categories,
                key="category_filter"
            )
        
        # Apply filters
        filtered_df = df.copy()
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['Type'] == type_filter]
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['Category'] == category_filter]
        
        # Display table
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Summary of filtered data
        if len(filtered_df) != len(df):
            st.info(f"Showing {len(filtered_df)} of {len(df)} transactions")

    def render_charts(self):
        """Render charts and visualizations"""
        st.subheader("📈 Financial Analytics")
        
        transactions = self.tracker.get_transactions()
        
        if not transactions:
            st.info("Add some transactions to see charts and analytics!")
            return
        
        # Create tabs for different charts
        tab1, tab2, tab3 = st.tabs(["💸 Expenses Breakdown", "📊 Income vs Expenses", "📈 Balance Trend"])
        
        with tab1:
            self.render_expenses_pie_chart(transactions)
        
        with tab2:
            self.render_income_expense_bar_chart(transactions)
        
        with tab3:
            self.render_balance_trend_chart(transactions)

    def render_expenses_pie_chart(self, transactions):
        """Render expenses breakdown pie chart"""
        expenses = [t for t in transactions if t['type'] == 'Expense']
        
        if not expenses:
            st.info("No expense transactions to display.")
            return
        
        # Group by category and convert to USD
        expense_by_category = {}
        for expense in expenses:
            category = expense['category']
            usd_amount = self.tracker.convert_to_usd(expense['amount'], expense.get('currency', 'USD'))
            expense_by_category[category] = expense_by_category.get(category, 0) + usd_amount
        
        # Create pie chart
        fig = px.pie(
            values=list(expense_by_category.values()),
            names=list(expense_by_category.keys()),
            title="Expenses by Category (USD)",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        
        st.plotly_chart(fig, use_container_width=True)

    def render_income_expense_bar_chart(self, transactions):
        """Render income vs expenses bar chart"""
        # Group by type and convert to USD
        income_total = sum(
            self.tracker.convert_to_usd(t['amount'], t.get('currency', 'USD'))
            for t in transactions if t['type'] == 'Income'
        )
        
        expense_total = sum(
            self.tracker.convert_to_usd(t['amount'], t.get('currency', 'USD'))
            for t in transactions if t['type'] == 'Expense'
        )
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                name='Income',
                x=['Financial Overview'],
                y=[income_total],
                marker_color='lightgreen'
            ),
            go.Bar(
                name='Expenses',
                x=['Financial Overview'],
                y=[expense_total],
                marker_color='lightcoral'
            )
        ])
        
        fig.update_layout(
            title="Income vs Expenses (USD)",
            barmode='group',
            height=500,
            yaxis_title="Amount (USD)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add summary below chart
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Income", f"${income_total:,.2f}")
        with col2:
            st.metric("Total Expenses", f"${expense_total:,.2f}")

    def render_balance_trend_chart(self, transactions):
        """Render balance trend over time"""
        if len(transactions) < 2:
            st.info("Add more transactions to see balance trend over time.")
            return
        
        # Sort transactions by date
        sorted_transactions = sorted(transactions, key=lambda x: x.get('date', ''))
        
        # Calculate running balance
        running_balance = 0
        dates = []
        balances = []
        
        for t in sorted_transactions:
            usd_amount = self.tracker.convert_to_usd(t['amount'], t.get('currency', 'USD'))
            if t['type'] == 'Income':
                running_balance += usd_amount
            else:
                running_balance -= usd_amount
            
            dates.append(t.get('date', ''))
            balances.append(running_balance)
        
        # Create line chart
        df_chart = pd.DataFrame({'Date': dates, 'Balance': balances})
        fig = px.line(
            df_chart,
            x='Date',
            y='Balance',
            title="Balance Trend Over Time (USD)"
        )
        
        fig.update_traces(line_color='#1f77b4', line_width=3)
        fig.update_layout(height=500)
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Balance (USD)")
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        
        st.plotly_chart(fig, use_container_width=True)

    def export_data(self):
        """Export transaction data to CSV"""
        transactions = self.tracker.get_transactions()
        
        if not transactions:
            st.warning("No transactions to export.")
            return
        
        # Create DataFrame for export
        df_data = []
        for t in transactions:
            df_data.append({
                'Date': t.get('date', ''),
                'Type': t['type'],
                'Category': t['category'],
                'Amount': t['amount'],
                'Currency': t.get('currency', 'USD'),
                'USD_Equivalent': self.tracker.convert_to_usd(t['amount'], t.get('currency', 'USD'))
            })
        
        df = pd.DataFrame(df_data)
        
        # Convert to CSV
        csv = df.to_csv(index=False)
        
        # Create download button
        st.sidebar.download_button(
            label="💾 Download CSV",
            data=csv,
            file_name=f"budget_tracker_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.sidebar.success("✅ Export ready! Click the download button above.")

    def import_data(self, uploaded_file):
        """Import transaction data from CSV"""
        try:
            # Read the uploaded file
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_columns = ['Type', 'Category', 'Amount']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.sidebar.error(f"Missing required columns: {', '.join(missing_columns)}")
                return
            
            # Import transactions
            imported_count = 0
            for _, row in df.iterrows():
                try:
                    success = self.tracker.add_transaction(
                        amount=float(row['Amount']),
                        category=str(row['Category']),
                        transaction_type=str(row['Type']),
                        currency=row.get('Currency', 'USD'),
                        transaction_date=row.get('Date', datetime.now().strftime('%Y-%m-%d'))
                    )
                    if success:
                        imported_count += 1
                except Exception as e:
                    st.sidebar.warning(f"Failed to import row: {e}")
            
            if imported_count > 0:
                self.save_tracker()
                st.sidebar.success(f"✅ Imported {imported_count} transactions successfully!")
                st.rerun()
            else:
                st.sidebar.error("❌ No transactions were imported.")
                
        except Exception as e:
            st.sidebar.error(f"❌ Failed to import data: {str(e)}")

    def run(self):
        """Main application runner"""
        # Render header
        self.render_header()
        
        # Render sidebar
        self.render_sidebar()
        
        # Main content area
        self.render_transaction_input()
        st.markdown("---")
        
        self.render_summary_metrics()
        st.markdown("---")
        
        self.render_transaction_history()
        st.markdown("---")
        
        self.render_charts()
        
        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #666; margin-top: 2rem;'>
                💰 Budget Tracker Pro - Built with ❤️ using Streamlit
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
    """Main function to run the Streamlit app"""
    app = StreamlitBudgetTracker()
    app.run()

if __name__ == "__main__":
    main()
