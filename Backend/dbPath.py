import os
import sys

def db_pfad():
    if getattr(sys, "frozen", False):
        basis_pfad = os.path.dirname(sys.executable)
    else:
        basis_pfad = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(basis_pfad, "Jackpot_DB.db")

