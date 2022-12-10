# Loan Qualifier Application

Loan qualifier application aims to update the existing Loan Qualifier Application to allow the user to save the qualified loans to a CSV file.

User Story:
> "As a user, I need the ability to save the qualifying loans to a CSV file so that I can share the results as a spreadsheet."

---

## Technologies

Python libraries that are required for this program:

`fire` (0.3.1)

`questionary` (1.5.2)

---

## Installation Guide

You can install Fire and Questionary from your Terminal (Mac User) or Gitbash (Windows User)by using the Python Package Index (PyPI).

Using the following code:

```python
pip install fire
```
```python
pip install questionary
```

---

## Usage

The app can be run by a simple python command on your terminal(Mac User) or gitbash (Windows User) `python app.py`.

The application wiull be pulling the input data from (daily_rate_sheet.csv) file which is located under (./data) folder. If the user saved the (daily_rate_sheet.csv) under a different location, the user will be promted to enter the file location.

Further, the application will ask the user to enter their details for the loan application such as, Credit Score, Debt, Income, Loan Value and property Value. Based on the input, the aplication wiull determine the eligible offers for the user. 

If the user has eligible offers in the market, the application will ask the user if he would like to save the offers that the application pulled for him. If the user decided to save the offers, the user will be prompted to save the file as a csv. 

```python
if len(qualifying_loans) >= 1:

        save_file = questionary.confirm("Would you like to save the file to csv?").ask()

        # here i'm asking the user if the want to save the file to csv

        if save_file:
            file_location= questionary.text("Where would you like to save the file? file should be in CSV format").ask()
            csvpath =Path(file_location)
            print("Saving qualifing loan as csv file...")
            

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

```

---

## Contributors

Baha Amour
---

## License

2022 edX Bootcamps.
