import os
import sys

def db_path():
    if getattr(sys, "frozen", False):
        basis_pfad = os.path.dirname(sys.executable)
        return os.path.join(basis_pfad, "_internal", "backend", "Jackpot_DB.db")
    
    else:
        basis_pfad = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(basis_pfad, "Jackpot_DB.db")