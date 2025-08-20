import streamlit as st
import pandas as pd
from datetime import date
from backend import DatabaseManager

st.set_page_config(layout="wide")

# Initialize database manager
db = DatabaseManager()

# ------------------ Main Application Layout ------------------
st.title("Financial Portfolio Tracker-sindhu G bhat")
st.markdown("---")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Manage Assets", "Transactions", "Business Insights"])

# ------------------ Dashboard Tab (Read) ------------------
with tab1:
    st.header("Portfolio Overview")
    assets = db.get_all_assets()
    if assets:
        # Get portfolio summary and display
        summary = db.get_portfolio_summary()
        total_value = summary[0] if summary[0] else 0
        total_gain_loss = summary[1] if summary[1] else 0

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Portfolio Value", f"${total_value:,.2f}")
        with col2:
            st.metric("Total Gain/Loss", f"${total_gain_loss:,.2f}", delta=f"${total_gain_loss:,.2f}")

        # Display assets in a dataframe
        assets_df = pd.DataFrame(assets, columns=["ID", "Ticker", "Class", "Purchase Date", "Shares", "Cost Basis", "Current Price", "Gain/Loss"])
        st.subheader("Asset Holdings")
        st.dataframe(assets_df, use_container_width=True)

        # Breakdown by asset class
        breakdown = db.get_asset_class_breakdown()
        if breakdown:
            breakdown_df = pd.DataFrame(breakdown, columns=["Asset Class", "Total Value"])
            st.subheader("Breakdown by Asset Class")
            st.bar_chart(breakdown_df.set_index("Asset Class"))
    else:
        st.info("No assets found. Add an asset in the 'Manage Assets' section.")

# ------------------ Manage Assets Tab (Create, Update, Delete) ------------------
with tab2:
    st.header("Manage Assets")
    st.subheader("Add New Asset")
    with st.form("add_asset_form", clear_on_submit=True):
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            ticker = st.text_input("Ticker Symbol (e.g., AAPL)")
            asset_class = st.selectbox("Asset Class", ["Equities", "Fixed Income", "Crypto", "Other"])
            purchase_date = st.date_input("Purchase Date", date.today())
        with col_form2:
            shares = st.number_input("Number of Shares", min_value=0.01, format="%.2f")
            cost_basis = st.number_input("Cost Basis ($)", min_value=0.01, format="%.2f")
            current_price = st.number_input("Current Price ($)", min_value=0.01, format="%.2f")

        submitted = st.form_submit_button("Add Asset")
        if submitted and ticker and shares and cost_basis and current_price:
            gain_loss = (current_price * shares) - cost_basis
            st.success(db.add_asset(ticker.upper(), asset_class, purchase_date, shares, cost_basis, current_price, gain_loss))

    st.markdown("---")
    st.subheader("Update or Delete an Asset")
    current_assets = db.get_all_assets()
    if current_assets:
        asset_options = {f"{a[1]} (ID: {a[0]})": a[0] for a in current_assets}
        selected_asset = st.selectbox("Select Asset to Update/Delete", list(asset_options.keys()))
        if selected_asset:
            asset_id_to_manage = asset_options[selected_asset]

            col_manage1, col_manage2 = st.columns(2)
            with col_manage1:
                new_price = st.number_input("New Current Price ($)", min_value=0.01, format="%.2f")
            with col_manage2:
                st.write("") # Spacer
                if st.button("Update Price"):
                    asset_info = db.get_asset_by_id(asset_id_to_manage)
                    if asset_info and new_price:
                        shares = asset_info[4]
                        cost_basis = asset_info[5]
                        new_gain_loss = (new_price * shares) - cost_basis
                        st.success(db.update_asset(asset_id_to_manage, new_price, new_gain_loss))

            if st.button("Delete Asset", type="primary"):
                if st.warning("Are you sure you want to delete this asset and all its transactions? This action is permanent."):
                    st.success(db.delete_asset(asset_id_to_manage))
                    st.experimental_rerun()
    else:
        st.info("No assets to manage.")

# ------------------ Transactions Tab (Create, Read) ------------------
with tab3:
    st.header("Log & View Transactions")

    st.subheader("Log a New Transaction")
    assets_tickers = db.get_asset_tickers()
    if assets_tickers:
        asset_id_map = {f"{t[1]} (ID: {t[0]})": t[0] for t in assets_tickers}
        selected_asset = st.selectbox("Select Asset", list(asset_id_map.keys()))

        with st.form("add_transaction_form", clear_on_submit=True):
            col_trans1, col_trans2 = st.columns(2)
            with col_trans1:
                transaction_type = st.selectbox("Transaction Type", ["BUY", "SELL", "DIVIDEND"])
            with col_trans2:
                transaction_date = st.date_input("Transaction Date", date.today())
            amount = st.number_input("Amount ($)", format="%.2f")

            if st.form_submit_button("Log Transaction"):
                if selected_asset and amount:
                    asset_id = asset_id_map[selected_asset]
                    st.success(db.add_transaction(asset_id, transaction_type, transaction_date, amount))
    else:
        st.warning("Please add an asset first to log a transaction.")

    st.markdown("---")
    st.subheader("Transaction History")
    transactions = db.get_all_transactions()
    if transactions:
        transactions_df = pd.DataFrame(transactions, columns=["ID", "Asset ID", "Type", "Date", "Amount", "Ticker"])
        st.dataframe(transactions_df, use_container_width=True)
    else:
        st.info("No transactions logged yet.")

# ------------------ Business Insights Tab (Read) ------------------
with tab4:
    st.header("Business Insights")
    insights = db.get_business_insights()
    if insights['total_assets'] is not None and insights['total_assets'] > 0:
        st.subheader("Portfolio Metrics")

        # Display insights using metric cards
        col_ins1, col_ins2, col_ins3 = st.columns(3)
        with col_ins1:
            st.metric("Total Assets", insights['total_assets'])
        with col_ins2:
            st.metric("Total Cost Basis", f"${insights['total_cost_basis']:,.2f}")
        with col_ins3:
            avg_cost = insights['avg_cost_per_share'] if insights['avg_cost_per_share'] is not None else 0
            st.metric("Avg. Cost per Share", f"${avg_cost:,.2f}")

        col_ins4, col_ins5 = st.columns(2)
        with col_ins4:
            max_gain = insights['max_gain_loss'] if insights['max_gain_loss'] is not None else 0
            st.metric("Maximum Gain/Loss", f"${max_gain:,.2f}", delta_color="normal")
        with col_ins5:
            min_gain = insights['min_gain_loss'] if insights['min_gain_loss'] is not None else 0
            st.metric("Minimum Gain/Loss", f"${min_gain:,.2f}", delta_color="inverse")

    else:
        st.info("No data available for business insights. Please add assets to your portfolio.")