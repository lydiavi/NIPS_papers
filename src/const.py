import os

###############################################################
#         Important directories & files
###############################################################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

REPORTS_DIR = os.path.join(BASE_DIR, "reports")
HTML_REPORTS_DIR = os.path.join(REPORTS_DIR, "html")
GEXF_REPORTS_DIR = os.path.join(REPORTS_DIR, "gexf")
