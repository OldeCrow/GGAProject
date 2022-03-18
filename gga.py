"""
Interview project for Generali Global Assistance
Test files are excluded from repo
"""
import os.path
from datetime import date, datetime, timedelta, timezone
import xml.etree.ElementTree as et
import json
import csv


class GGA:
    def __init__(self):
        self.xml_payload = "test_payload1.xml"
        self.json_payload = "test_payload.json"
        self.csv_payload1 = "Jmeter_log1.jtl"
        self.csv_payload2 = "Jmeter_log2.jtl"
        self.date_today = date.today()

    """
    1. Create a python method that takes arguments int X and int Y,
    and updates DEPART and RETURN fields
    in test_payload1.xml:

    - DEPART gets set to X days in the future from the current date
    (whatever the current date is at the moment of executing the code)
    - RETURN gets set to Y days in the future from the current date

    Please write the modified XML to a new file.
    """
    def update_xml_depart_return(self, x: int, y: int):
        xml_tree = et.parse(self.xml_payload)
        xml_data = xml_tree.getroot()
        # There may be more than one request in the quote
        for dep in xml_data.findall(".//DEPART"):
            dep.text = date.strftime(self.date_today + timedelta(days=x), "%Y%m%d")
        for ret in xml_data.findall(".//RETURN"):
            ret.text = date.strftime(self.date_today + timedelta(days=y), "%Y%m%d")
        xml_tree.write(self.update_filename(self.xml_payload))

    """
    2. Create a python method that takes a json element
    as an argument, and removes that element from test_payload.json.
    
    Please verify that the method can remove either nested or non-nested elements
    (try removing "outParams" and "appdate").
    
    Please write the modified json to a new file.
    """
    def remove_json_element(self, elem: str):
        json_data = json.load(open(self.json_payload))
        filtered_json_data = self.filter_json(json_data, elem)
        json.dump(filtered_json_data, open(self.update_filename(self.json_payload), "w"), indent=2)

    """
    3. Create a python script that parses jmeter log files in CSV format,
    and in the case if there are any non-successful endpoint responses recorded in the log,
    prints out the label, response code, response message, failure message,
    and the time of non-200 response in human-readable format in PST timezone
    (e.g. 2021-02-09 06:02:55 PST).
    
    Please use Jmeter_log1.jtl, Jmeter_log2.jtl as input files for testing out your script
    (the files have .jtl extension but the format is  CSV).
    """
    def find_failed_jmeter_responses(self, filename: str):
        csv_data = csv.DictReader(open(filename))
        for resp in csv_data:
            if resp["responseCode"] != "200":
                print(int(resp["timeStamp"]))
                print(resp["label"], resp["responseCode"], resp["responseMessage"], resp["failureMessage"],
                      datetime.fromtimestamp(int(resp["timeStamp"])/1000, tz=timezone(timedelta(hours=-7), name="PST"))
                      .strftime("%Y-%m-%d %H:%M:%S %Z"))

    # Simple method to create a new filename from a source filename
    def update_filename(self, fullpath: str) -> str:
        filename, file_ext = os.path.splitext(fullpath)
        return filename + "_update" + datetime.now().strftime("%Y%m%d%H%M%S") + "." + file_ext

    # Recursive method for json object iteration
    def filter_json(self, data, elem: str):
        if isinstance(data, dict):
            filtered_data = {}
            for k, v in data.items():
                if k != elem:
                    filtered_data[k] = self.filter_json(v, elem)
            return filtered_data
        elif isinstance(data, list):
            filtered_data = []
            for v in data:
                if v != elem:
                    filtered_data.append(self.filter_json(v, elem))
            return filtered_data
        else:
            return data


"""
Test code below.
"""
tester = GGA()
# tester.update_xml_depart_return(1, 2)
# tester.remove_json_element("outParams")
tester.find_failed_jmeter_responses(tester.csv_payload2)
