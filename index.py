from Classes.JSONReader import JSONReader
from stock_wrapper import Shares, robin

credentials = JSONReader.read_file("Credentials.json")
robin.login(credentials['email'], credentials['password'])

# data = robin.build_portfolio()
# print(data)
# print(ual.quantity)

data = Shares("UAL").equity
print(data)