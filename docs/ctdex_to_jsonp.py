import json
import datetime

INDEX_COLUMN = "CTDPRS"
PARAM_COLUMN = "CTDSAL"
PARAM_UNIT = "PSU"

CTD_QUALITY_MAP = {
        "1": 0.8,
        "2": 0.95,
        "3": 0.5,
        "4": 0.3,
        "6": 0.9,
        "7": 0.85,
        }

output = {
        "type": "c"
        }

with open("exchange_profile_ct1.csv", 'r') as f:
    data = f.read().splitlines()

## we are going to assume our input file is perfectly valid

def split_headers(header_lines):
    headers = {}
    for line in header_lines:
        header, value = line.split("=")
        headers[header.strip()] = value.strip()
    return headers

def dt_to_rfcstring(date, time):
    dt = date + time # string values
    dt_obj = datetime.datetime.strptime(dt, "%Y%m%d%H%M")
    return dt_obj.strftime("%Y-%m-%dT%H:%M:%SZ")


for i, line in enumerate(data):
    if line.startswith("CTD"):
        continue
    if line.startswith("#"):
        continue 

    if line.startswith("NUMBER_HEADERS"):
        header_index = i

    if line.startswith("END_DATA"):
        end_data_index = i

number_headers = int(data[header_index].split("=")[1])
params_index = header_index + number_headers
units_index = params_index + 1
data_index = units_index + 1

headers = split_headers(data[header_index:params_index])

params = [param.strip() for param in data[params_index].split(",")]
units = [unit.strip() for unit in data[units_index].split(",")]

output["cruise"] = headers["EXPOCODE"]
output["station"] = headers["STNNBR"]
output["cast"] = headers["CASTNO"]
output["lat"] = float(headers["LATITUDE"])
output["lon"] = float(headers["LONGITUDE"])
output["date"] = dt_to_rfcstring(headers["DATE"], headers["TIME"])
output["date_precision"] = 60

output["index_parameter"] = INDEX_COLUMN
output["index_unit"] = "dbar"
output["index_type"] = "decimal"

output["data_parameter"] = PARAM_COLUMN
output["data_unit"] = PARAM_UNIT
output["data_precision"] = 1

data_values = data[data_index:end_data_index]

index_index = params.index(INDEX_COLUMN)
value_index = params.index(PARAM_COLUMN)
quality_index = params.index(PARAM_COLUMN + "_FLAG_W")

index = []
data = []
confidence = []
awaiting = []

for datum in data_values:
    split = [d.strip() for d in datum.split(",")]

    index.append(float(split[index_index]))
    data.append(float(split[value_index]))
    confidence.append(CTD_QUALITY_MAP[split[quality_index]])

output["index"] = index
output["data"] = data
output["confidence"] = quality


print(json.dumps(output))
