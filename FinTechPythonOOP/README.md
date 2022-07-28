# Peter Lieberman | Challenge 2 | Loan Qualifier Application

The following document is a technical summary of a modular application built for "FinTech Lending Startup" that collects loan information from applicants to identify a list loans they qualify for.


## Technologies

```python
The program uses the Python libraries: sys, fire, questionary and pathlib. The application requires a csvfile with bank loan data as the data input. The output is a csvfile with an optimized list of loans that is given to the user. The frontend of the application runs through the command line.
```
---

## Installation Guide

The program requires Python 3.7 and Anaconda (or another means for activitating the Python libraries).

---

## User Story & Acceptance Criteria

As a user, I need the ability to save the qualifying loans to a CSV file so that I can share the results as a spreadsheet.

1) Given that I’m using the loan qualifier CLI, when I run the qualifier, then the tool should prompt the user to save the results as a CSV file.

2) Given that no qualifying loans exist, when prompting a user to save a file, then the program should notify the user and exit.

3) Given that I have a list of qualifying loans, when I’m prompted to save the results, then I should be able to opt out of saving the file.

4) Given that I have a list of qualifying loans, when I choose to save the loans, the tool should prompt for a file path to save the file.

5) Given that I’m using the loan qualifier CLI, when I choose to save the loans, then the tool should save the results as a CSV file.

## Usage

This is a modular command line application that matches applicants with qualifying loans by performing four (4) main actions:

1) Loads the bank data information from a CSV file. This is done prior to asking the user for info.
2) Grabs the applicant's information by asking five questions using Questionary.
3) Finds the qualifying loans by filtering the user's data (step 2) against our bank data (step 1).
4) Exports and saves the List of Qualifying Loans as a CSV File for the user.

The main program ("app.ipynb") utilizes six (6) modules that are contained in the directory. 

- The code calls a user submitted CSV file from one (1) module in the "FileIO" file from the "Utils" folder. The function is a CSV reader.

- The code calls two (2) modules in the "Calculators" file in the "Utils" folder to perform calculations. This script contains financial calculator functions needed to determine loan qualifications.

- The code calls four (4) modules contained in separate files that are in the "Filters" folder. These functions work together in a cascading fashion. It filters our bank list based on information that user supplies in succession. The primary program ("app.ipynb") uses Questionary to ask the user for data and then calls these four modules to perform the filtering.


## Contributors

The application was built by Peter Lieberman for Challenge 2 in the Columbia Engineering FinTech Bootcamp.

## License

Any student or person with authorization from Columbia University may use the application.