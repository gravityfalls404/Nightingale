import requests
import json

# url = "https://covid-19-data.p.rapidapi.com/country"
# querystring = {"name":"asv"}
# headers = {
#     'x-rapidapi-key': "aaf84cd0c3msh21b415f44e90825p1b4738jsnaf40c68a7447",
#     'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
#     }


# response = requests.request("GET", url, headers=headers, params=querystring)
# response = json.loads(response.text)[0]
# print(response["country"])

response_flag = requests.request("GET",f"https://restcountries.eu/rest/v2/alpha/in")
print(response_flag.status_code)
response_flag = json.loads(response_flag.text)
print(response_flag["name"])
