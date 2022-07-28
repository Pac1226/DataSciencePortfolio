"""Loan to Value Filter"""

# This script filters the bank list by the applicant's maximum home loan to home value ratio.

# Filters the bank list by the maximum debt-to-income ratio allowed by the bank:

    # loan_to_value_ratio (float) = The applicant's loan to value ratio.
    # bank_list (list of lists = The available bank loans.
        
# Function returns a list of qualifying bank loans.

def filter_loan_to_value(loan_to_value_ratio, bank_list):

    loan_to_value_approval_list = []

    for bank in bank_list:
        if loan_to_value_ratio <= float(bank[2]):
            loan_to_value_approval_list.append(bank)
    return loan_to_value_approval_list
