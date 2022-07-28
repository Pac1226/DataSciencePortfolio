"""Max Loan Size Filter"""

# This script filters the bank list by comparing the user's loan value against the bank's maximum loan size.

# Filters the bank list by the maximum allowed loan amount:

    # loan_amount (int) = the requested loan amount
    # bank_list (list of lists) = the available bank loans
        
# Function returns a list of qualifying bank loans.


def filter_max_loan_size(loan_amount, bank_list):

    loan_size_approval_list = []

    for bank in bank_list:
        if loan_amount <= int(bank[1]):
            loan_size_approval_list.append(bank)
    return loan_size_approval_list
