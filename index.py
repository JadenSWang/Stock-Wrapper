from Classes.JSONReader import JSONReader
import stock_wrapper

credentials = JSONReader.read_file("Credentials.json")
stock_wrapper.robin.login(credentials['email'], credentials['password'])

# stock_wrapper.visualize.display_stocks(['UAL', 'AAPL'])
data = stock_wrapper.data.get_daily_history('UAL')
print(data)

stock_wrapper.visualize.graph('UAL')