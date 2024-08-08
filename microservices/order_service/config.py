import os
from urllib.parse import quote_plus

MSSQL_USER = os.environ.get('MSSQL_USER', 'sa')
MSSQL_PASSWORD = os.environ.get('MSSQL_PASSWORD', 'ItuYazilim1!')
MSSQL_HOST = os.environ.get('MSSQL_HOST', 'sqlpreview')
MSSQL_PORT = os.environ.get('MSSQL_PORT', '1433')
MSSQL_DB = os.environ.get('MSSQL_DB', 'RestaurantService')
MSSQL_DRIVER = os.environ.get('MSSQL_DRIVER', 'ODBC Driver 17 for SQL Server')

# ODBC bağlantı dizesi
ODBC_CONNECTION_STRING = (
    f"DRIVER={{{MSSQL_DRIVER}}};"
    f"SERVER={MSSQL_HOST},{MSSQL_PORT};"
    f"DATABASE={MSSQL_DB};"
    f"UID={MSSQL_USER};"
    f"PWD={MSSQL_PASSWORD};"
)

# SQLAlchemy için bağlantı dizesi
DATABASE_CONNECTION_STRING = f"mssql+pyodbc:///?odbc_connect={quote_plus(ODBC_CONNECTION_STRING)}"