bank_config = [

    {
        "institution": "Chase bank",
        "file_dir": "examples",
        "file_pattern": "Chase_checking*csv",
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
        "institution": "Chase Card",
        "file_dir": "examples",
        "file_pattern": "Chase_card*csv",
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
        "institution": "Fidelity",
        "file_dir": "examples",
        "file_pattern": "Fidelity*csv",
        "column_map": {
            "symbol": "Symbol",
            "quantity": "Quantity",
            "cost": "Cost Basis",
        },
        "datetime_format": "%m/%d/%Y",
        "filename_date_regex": r"\S{3}-\d{2}-\d{4}"
    }
]
