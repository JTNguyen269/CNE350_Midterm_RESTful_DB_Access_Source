# Code reference: https://github.com/ellisju37073/States
# Regex reference: https://www.youtube.com/watch?v=wnuBwl2ekmo&ab_channel=NeuralNine
# Regex cheat sheet: https://www.geeksforgeeks.org/python-regex-cheat-sheet/
# Regex python library: https://docs.python.org/3/library/re.html
# Tuple unpacking: https://stackabuse.com/unpacking-in-python-beyond-parallel-assignment/
# HTML cheat sheet: https://www.codecademy.com/learn/learn-html/modules/learn-html-elements/cheatsheet
# CSS website styling: https://www.codecademy.com/learn/styling-a-website/modules/learn-css-selectors-visual-rules/cheatsheet
# Flask cheat sheet: https://www.codecademy.com/learn/introduction-to-flask/modules/flask-templates-and-forms/cheatsheet


import pandas as pd
from sqlalchemy import create_engine
import json

# MySQL connection details
hostname = "127.0.0.1"
uname = "root"
pwd = ""
dbname = "pll_algorithms"

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}")

# Read JSON file
with open("PLL.json", "r") as file:
    pll_data = json.load(file)

# Flatten the JSON structure and convert to DataFrame
pll_list = []
for pll_name, pll_info in pll_data["pll_algorithms"].items():
    pll_info["name"] = pll_name
    pll_list.append(pll_info)

pll_df = pd.DataFrame(pll_list)

# Connect to database and insert data
connection = engine.connect()
pll_df.to_sql('pll_algorithms', con=engine, if_exists='replace')
connection.close()

print(pll_df)
