"""Import CSV Function for User Prompt"""

import csv

# "load_csv" function reades the csv file from path provided by the user

def load_csv(csvpath):

    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skips the CSV Header
        next(csvreader)

        # Reads the CSV data
        for row in csvreader:
            data.append(row)
    
    # Returns a list of lists than contains rows of date from the csv file
    return data
