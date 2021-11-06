bank_config = [
    {
        "institution": "bank_1",
        "file_dir": "test/statements",
        "file_pattern": "Chase1*csv",
        "column_map": {
            "date": "Posting Date",
            "merchant": "Description",
            "amount": "Amount",
            "balance": "Balance",
        },
        "datetime_format": "%m/%d/%Y",
        "filename_date_regex": r"\d{8}"
    },

    {
        "institution": "bank_2",
        "file_dir": "test/statements",
        "file_pattern": "Chase27*csv",
        "column_map": {
            "date": "Posting Date",
            "merchant": "Description",
            "amount": "Amount",
            "balance": "Balance",
        },
        "datetime_format": "%m/%d/%Y",
        "filename_date_regex": r"\d{8}"
    },
]


card_config = [
    {
        "institution": "card_1",
        "file_dir": "test/statements",
        "file_pattern": "Chase23*csv",
        "column_map": {
            "date": "Transaction Date",
            "merchant": "Description",
            "category": "Category",
            "type": "Type",
            "amount": "Amount",
        },
        "datetime_format": "%m/%d/%Y",
        "filename_date_regex": r"\d{8}"
    },
]


brokerage_config = [
    {
        "institution": "brokerage_1",
        "file_dir": "test/statements",
        "file_pattern": "Chase_S*csv",
        "column_map": {
            "date": "As of",
            "symbol": "Ticker",
            "quantity": "Quantity",
            "cost": "Cost"
        },
        "datetime_format": "%m/%d/%Y",
        "filename_date_regex": r"\d{4}-\d{2}-\d{2}"
    },

    {
        "institution": "brokerage_2",
        "file_dir": "test/statements",
        "file_pattern": "F*csv",
        "column_map": {
            "symbol": "Symbol",
            "quantity": "Quantity",
            "cost": "Cost Basis",
        },
        "datetime_format": "%m/%d/%Y",
        "filename_date_regex": r"\S{3}-\d{2}-\d{4}"
    }
]
