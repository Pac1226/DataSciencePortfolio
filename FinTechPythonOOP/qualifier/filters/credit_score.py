"""Credit Score Filter"""

# This script contains a function that filters a bank list by the user's minimum credit score.

# Function calls data from one bank and one user supplied data source:

     # credit_score (int): The applicant's credit score.
     # bank_list (list of lists) = Available bank loans. This list is called from latest bank data in system.
        
# Function returns a list of qualifying bank loans.

def filter_credit_score(credit_score, bank_list):
    
    credit_score_approval_list = []
    
    for bank in bank_list:
        if credit_score >= int(bank[4]):
            credit_score_approval_list.append(bank)
            
    return credit_score_approval_list
