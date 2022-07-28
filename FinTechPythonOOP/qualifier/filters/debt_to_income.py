"""Debt to Income Filter"""

# This script filters the bank list by the applicant's maximum debt-to-income ratio.

# Filters the bank list by the maximum debt-to-income ratio allowed by the bank:

    # monthly_debt_ratio (float) = The applicant's monthly debt ratio.
    # bank_list (list of lists = The available bank loans.
        
# Function returns a a list of qualifying bank loans.

def filter_debt_to_income(monthly_debt_ratio, bank_list):

    debit_to_income_approval_list = []
    for bank in bank_list:
        if monthly_debt_ratio <= float(bank[3]):
            debit_to_income_approval_list.append(bank)
    return debit_to_income_approval_list
