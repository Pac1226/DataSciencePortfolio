"""A Collection of Financial Calculators"""

# This script contains a variety of financial calculator functions needed to determine loan qualifications.

# Function calculates the user's monthly debt-to-income ratio basedon input:

    # Monthly_debt_payment (int) =  The total monthly debt.
    # Monthly_income (int) = The total monthly income.
    
# Function returns the monthly debt ratio

def calculate_monthly_debt_ratio(monthly_debt_payment, monthly_income):

    monthly_debt_ratio = int(monthly_debt_payment) / int(monthly_income)
    
    return monthly_debt_ratio


# Function calculates the user's loan-to-value ratio based on inputs
    # loan_amount (int) = User's requested loan amount.
    # home_value (int) = User's home value.
# Function returns the user's loan-to-value ratio.

def calculate_loan_to_value_ratio(loan_amount, home_value):
    
    loan_to_value_ratio = int(loan_amount) / int(home_value)
    
    return loan_to_value_ratio
