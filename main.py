import os
import re
import openai
import json
import math

from merge import merge_dicts
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()

full_context = """
    Given the text block that follows, extract these data points into a JSON object. Uncertain or missing values should be null.

    Property Name
    Purchase Price
    Number of Units
    Price per Unit
    Average Unit Sq. Ft.
    Total Rentable Sq. Ft.
    Average Monthly Rent
    Average Rent / Sq. Ft.
    Occupancy Rate
    Sponsor
    Zip Code

  """

openai.api_key = os.getenv('OPENAI_API_KEY')

reader = PdfReader("memorandum.pdf")
number_of_pages = len(reader.pages)

data = {
  "Property Name": None,
  "Purchase Price": None,
  "Number of Units": None,
  "Price per Unit": None,
  "Average Unit Square Feet": None,
  "Total Rentable Square Feet": None,
  "Average Monthly Rent Per Unit": None,
  "Average Rent / Square Feet": None,
  "Occupancy Rate": None,
  "Sponsor": None,
  "Zip Code": None,
}

# Pulls generic information and returns dictionary
def parse_generic(text):
  content = """
    Given the text block that follows, extract these data points into a JSON object. Uncertain or missing values should be null. All other values should be string types. Do not include anything other than the JSON object in the response.

    Property Name
    Sponsor
    Zip Code

  """ + text
  completion = openai.ChatCompletion.create(model="gpt-4", messages=[{
    "role": "user",
    "content": content
  }])
  return completion.choices[0].message.content


# Pulls Underwrite information and returns dictionary
def parse_underwrite(text):
  content = """
    Given the text block that follows, extract these data points into a JSON object. All values should be strings. Do not include anything other than the JSON object in the response.

    Purchase Price
    Number of Units
    Average Unit Square Feet
    Total Rentable Square Feet
    Average Monthly Rent Per Unit
    Average Rent / Square Feet
    Occupancy Rate

  """ + text
  completion = openai.ChatCompletion.create(model="gpt-4", messages=[{
    "role": "user",
    "content": content
  }])
  return completion.choices[0].message.content

for i in range(number_of_pages):
  page = reader.pages[i]
  text = page.extract_text()
  is_underwrite = re.search("underwrite", text, flags=re.IGNORECASE)
  if is_underwrite is not None:
    underwrite_values = json.loads(parse_underwrite(text))
    data = merge_dicts(data, underwrite_values)
    continue
  is_generic = re.search("(executive summary)|(memorandum)", text, flags=re.IGNORECASE)
  if is_generic is not None:
    generic_values = json.loads(parse_generic(text))
    data = merge_dicts(data, generic_values)
    continue

# Manually calculate this data.
# For whatever reason, asking the LLM to parse this data is not only wrong, but it also creates
# confusion with the average monthly rent.
data["Price per Unit"] = int(data["Purchase Price"].replace(',', '')) / int(data["Number of Units"].replace(',', ''))

# Some type checking
if len(data["Zip Code"]) > 5:
  raise Exception("Zip Code invalid format, check output")

# Check to see if extracted values are close to calculated values
# Large discrepancies here would indicate some sort of extraction mistake
# and would warrant a further check, either rerunning the extraction or a manual check.
avgMonthlyRent = int(data["Average Monthly Rent Per Unit"].replace(',', ''))
avgSqFt = int(data["Average Unit Square Feet"].replace(',', ''))
calculatedAvgRentPerSqFt = round(avgMonthlyRent / avgSqFt, 2)
if math.isclose(calculatedAvgRentPerSqFt, float(data["Average Rent / Square Feet"]), rel_tol=0.01) is False:
  raise Exception("Mismatch between calculated and extracted value, check output")

print(json.dumps(data))