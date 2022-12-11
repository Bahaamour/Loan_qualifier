# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import csv
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio import load_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = "./data/daily_rate_sheet.csv"
    # csvpath = "./data/daily_rate_sheet.csv"
    csvpath = Path(csvpath)
    if not csvpath.exists():
        csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = int(questionary.text("What's your credit score?").ask())
    debt = float(questionary.text("What's your current amount of monthly debt?").ask())
    income = float(questionary.text("What's your total monthly income?").ask())
    loan_amount = float(questionary.text("What's your desired loan amount?").ask())
    home_value = float(questionary.text("What's your home value?").ask())

    

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """ We want to determine which loans the user qualifies for based on:
    - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)
        
        Then we are returning a list of the banks that are willing to underwrite the loan.
    """
    
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


def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    #here, i'm saving the loan qualifiers

    header = "Financial Institution", "Max Loan Amount", "Max Loan To Value", "Max Debt to Income Ratio", "Minumum Credit Score","APR Offered"

    if len(qualifying_loans) >= 1:

        save_file = questionary.confirm("Would you like to save the file to csv?").ask()

        # here i'm asking the user if the want to save the file to csv

        if save_file:
            # I am using a while statement in case the user saved the file in any format other than csv, it would give him an error
            while True:
                file_location= questionary.text("Where would you like to save the file?").ask()
                if file_location [-3:] != "csv":
                    print("ERROR! file should be in CSV format.")
                
                else:
                    csvpath =Path(file_location)
                    print("Saving qualifing loan as csv file...")
                    break
            

            with open(csvpath,"w",newline= "") as csvfile:
                csvwriter= csv.writer(csvfile,delimiter =",")
                csvwriter.writerow(header)


                for row in qualifying_loans:
                    csvwriter.writerow(row)
# If the user chooses not to save file.
        else:
            sys.exit("Thank you for using the loan qualifier application.")

    else:
        sys.exit("You have no qualifing loans.")





def run():
    """The main function for running the script."""

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
