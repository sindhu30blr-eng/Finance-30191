CREATE TABLE IF NOT EXISTS assets (
    asset_id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    asset_class VARCHAR(50) NOT NULL,
    purchase_date DATE NOT NULL,
    shares NUMERIC(15, 8) NOT NULL,
    cost_basis NUMERIC(15, 2) NOT NULL,
    current_price NUMERIC(15, 2) NOT NULL,
    gain_loss NUMERIC(15, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(asset_id),
    transaction_type VARCHAR(20) NOT NULL, -- e.g., 'BUY', 'SELL', 'DIVIDEND'
    transaction_date DATE NOT NULL,
    amount NUMERIC(15, 2) NOT NULL
);
INSERT INTO assets (ticker, asset_class, purchase_date, shares, cost_basis, current_price, gain_loss) VALUES
('MSFT', 'Equities', '2023-01-15', 50.00, 15000.00, 17500.00, 2500.00),
('GOOGL', 'Equities', '2023-02-20', 20.50, 25000.00, 24000.00, -1000.00),
('US_BOND_10Y', 'Fixed Income', '2022-11-01', 100.00, 10000.00, 10150.00, 150.00),
('BTC', 'Crypto', '2023-03-10', 0.50, 12000.00, 14500.00, 2500.00);
-- Transaction for MSFT (asset_id = 1)
INSERT INTO transactions (asset_id, transaction_type, transaction_date, amount) VALUES
(1, 'BUY', '2023-01-15', 15000.00);

-- Transaction for GOOGL (asset_id = 2)
INSERT INTO transactions (asset_id, transaction_type, transaction_date, amount) VALUES
(2, 'BUY', '2023-02-20', 25000.00);

-- Transaction for US_BOND_10Y (asset_id = 3)
INSERT INTO transactions (asset_id, transaction_type, transaction_date, amount) VALUES
(3, 'BUY', '2022-11-01', 10000.00);

-- Transaction for BTC (asset_id = 4)
INSERT INTO transactions (asset_id, transaction_type, transaction_date, amount) VALUES
(4, 'BUY', '2023-03-10', 12000.00);

-- Example dividend transaction for MSFT
INSERT INTO transactions (asset_id, transaction_type, transaction_date, amount) VALUES
(1, 'DIVIDEND', '2023-05-20', 15.75);

-- Example sale transaction for GOOGL
INSERT INTO transactions (asset_id, transaction_type, transaction_date, amount) VALUES
(2, 'SELL', '2023-06-10', 500.00);