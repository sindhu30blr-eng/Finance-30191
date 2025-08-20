import psycopg2

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = psycopg2.connect(
                dbname="nikhil",
                user="postgres",
                password="sindhubhat",
                host="localhost"
            )
            self.cursor = self.conn.cursor()
            print("Database connection successful.")
        except psycopg2.OperationalError as e:
            print(f"Error connecting to database: {e}")

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Database connection closed.")

    # ------------------ CRUD Operations ------------------
    # Create
    def add_asset(self, ticker, asset_class, purchase_date, shares, cost_basis, current_price, gain_loss):
        """Adds a new asset to the database."""
        try:
            self.cursor.execute(
                """
                INSERT INTO assets (ticker, asset_class, purchase_date, shares, cost_basis, current_price, gain_loss)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (ticker, asset_class, purchase_date, shares, cost_basis, current_price, gain_loss)
            )
            self.conn.commit()
            return "Asset added successfully."
        except Exception as e:
            self.conn.rollback()
            return f"Error adding asset: {e}"

    def add_transaction(self, asset_id, transaction_type, transaction_date, amount):
        """Adds a new transaction to the database."""
        try:
            self.cursor.execute(
                """
                INSERT INTO transactions (asset_id, transaction_type, transaction_date, amount)
                VALUES (%s, %s, %s, %s)
                """,
                (asset_id, transaction_type, transaction_date, amount)
            )
            self.conn.commit()
            return "Transaction added successfully."
        except Exception as e:
            self.conn.rollback()
            return f"Error adding transaction: {e}"

    # Read
    def get_all_assets(self):
        """Retrieves all assets from the database."""
        self.cursor.execute("SELECT * FROM assets ORDER BY ticker")
        return self.cursor.fetchall()

    def get_asset_by_id(self, asset_id):
        """Retrieves a single asset by its ID."""
        self.cursor.execute("SELECT * FROM assets WHERE asset_id = %s", (asset_id,))
        return self.cursor.fetchone()

    def get_all_transactions(self):
        """Retrieves all transactions with asset ticker information."""
        self.cursor.execute(
            """
            SELECT t.*, a.ticker
            FROM transactions t
            JOIN assets a ON t.asset_id = a.asset_id
            ORDER BY t.transaction_date DESC
            """
        )
        return self.cursor.fetchall()

    # Update
    def update_asset(self, asset_id, current_price, gain_loss):
        """Updates an asset's current price and gain/loss."""
        try:
            self.cursor.execute(
                """
                UPDATE assets
                SET current_price = %s, gain_loss = %s
                WHERE asset_id = %s
                """,
                (current_price, gain_loss, asset_id)
            )
            self.conn.commit()
            return "Asset updated successfully."
        except Exception as e:
            self.conn.rollback()
            return f"Error updating asset: {e}"

    # Delete
    def delete_asset(self, asset_id):
        """Deletes an asset and its related transactions from the database."""
        try:
            self.cursor.execute("DELETE FROM transactions WHERE asset_id = %s", (asset_id,))
            self.cursor.execute("DELETE FROM assets WHERE asset_id = %s", (asset_id,))
            self.conn.commit()
            return "Asset deleted successfully."
        except Exception as e:
            self.conn.rollback()
            return f"Error deleting asset: {e}"

    # ------------------ Business Insights ------------------
    def get_portfolio_summary(self):
        """Calculates total portfolio value and gain/loss."""
        self.cursor.execute("SELECT SUM(shares * current_price) as total_value, SUM(gain_loss) as total_gain_loss FROM assets")
        return self.cursor.fetchone()

    def get_asset_class_breakdown(self):
        """Breaks down portfolio value by asset class."""
        self.cursor.execute("SELECT asset_class, SUM(shares * current_price) FROM assets GROUP BY asset_class")
        return self.cursor.fetchall()

    def get_business_insights(self):
        """Provides various business insights using aggregate functions."""
        insights = {}
        # Count total assets
        self.cursor.execute("SELECT COUNT(*) FROM assets")
        insights['total_assets'] = self.cursor.fetchone()[0]

        # Sum total cost basis
        self.cursor.execute("SELECT SUM(cost_basis) FROM assets")
        insights['total_cost_basis'] = self.cursor.fetchone()[0]

        # Average cost basis per share
        self.cursor.execute("SELECT AVG(cost_basis / shares) FROM assets")
        insights['avg_cost_per_share'] = self.cursor.fetchone()[0]

        # Max gain/loss
        self.cursor.execute("SELECT MAX(gain_loss) FROM assets")
        insights['max_gain_loss'] = self.cursor.fetchone()[0]

        # Min gain/loss
        self.cursor.execute("SELECT MIN(gain_loss) FROM assets")
        insights['min_gain_loss'] = self.cursor.fetchone()[0]

        return insights

    # ------------------ Other helpers ------------------
    def get_asset_tickers(self):
        """Retrieves a list of asset tickers."""
        self.cursor.execute("SELECT asset_id, ticker FROM assets")
        return self.cursor.fetchall()