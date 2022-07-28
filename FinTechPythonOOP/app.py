"""Loan Qualifier Application"""

# This is a modular command line application that matches applicants with qualifying loans with a total of 6 modules.

# The code calls a user submitted CSV file from one (1) function in " ./qualifier/utils/fileio.ipynb ".
# The code calls two (2) functions contained in " ./qualifier/utils/calculators.ipynb".

# The application checks data from the user loaded CSV file with our bank data in " ./data/daily_rate_sheet.csv ".

import csv
import sys
import fire
import questionary
from pathlib import Path
import pandas as pd


# The code below calls four (4) functions from " ./qualifier/filters " that filters data provided by the user.
# This is a cascading filter. It filters the user's data through the four functions in the order listed.

from qualifier.utils.fileio import load_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


# Function asks for the file path to the latest banking data and load the CSV file
# Function returns bank data from the " ./data/data_rate_sheet " CSV file.

def load_bank_data():

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


# Function prompts the applicant for the applicant's financial information in the command line
# Function returns the applicant's financial information

def get_applicant_info():
    
    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


# Function determines which loans the user qualifies for.
# Loan qualification criteria is based on:
    # - Credit Score
    # - Loan Size
    # - Debit to Income ratio (calculated)
    # - Loan to Value ratio (calculated)
# The data inputs are:
    # - bank_data (list): A list of bank data.
    # - credit_score (int): The applicant's current credit score.
    # - debt (float): The applicant's total monthly debt payments.
    # - income (float): The applicant's total monthly income.
    # - loan (float): The total loan amount applied for.
    # - home_value (float): The estimated home value.

# Function returns a list of the banks willing to underwrite the loan.
def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")
 
    return bank_data_filtered

 
# Function saves the qualifying loans to a CSV file for the user.
# qualifying_loans (list of lists) = The qualifying bank loans.
def save_qualifying_loans(bank_data_filtered):
    qualifying_loans = pd.DataFrame(bank_data_filtered)
    qualifying_loans.to_csv(r"qualifying_loans.csv")


# This is the main function that runs the entire script.
def run():
 
    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()
    
    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)
