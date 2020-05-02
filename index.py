from Classes.JSONReader import JSONReader
import stocks_wrapper

credentials = JSONReader.read_file("Credentials.json")
stocks_wrapper.robin.login(credentials['email'], credentials['password'])

