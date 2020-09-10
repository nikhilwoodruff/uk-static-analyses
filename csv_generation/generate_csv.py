import csv
import os
import shutil
from tqdm import tqdm
import argparse
from random import random

def clean_dirs(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def write_person_file(data_dir, output_dir, weights=None):
    with open(os.path.join(output_dir, "person.csv"), "w+", encoding="utf-8", newline="") as g:
        with open(os.path.join(data_dir, "adult.tab"), encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=next(f).split("\t"), delimiter="\t")
            fieldnames = ["person_id", "household_id", "family_id", "role", "age_band", "JSA_receipt", "IS_receipt", "pension_income", "employee_earnings", "self_employed_earnings", "investment_income", "hours_worked", "adult_weight", "disabled"]
            writer = csv.DictWriter(g, fieldnames=fieldnames)
            writer.writeheader()
            skipped = 0
            for line in tqdm(reader, desc="Writing adults into person file", total=33238):
                try:
                    string_keys = ["person_id", "household_id", "family_id", "role"]
                    allowed_to_be_negative = ["self_employed_earnings"]
                    person = {
                        "person_id": line["sernum"] + "p" + line["PERSON"],
                        "household_id": line["sernum"],
                        "family_id": line["sernum"] + "f" + line["BENUNIT"],
                        "role": "adult",
                        "age_band": int(line["IAGEGR4"]),
                        "JSA_receipt": 1 if line["WAGEBEN6"] == '1' else 0,
                        "IS_receipt": 1 if line["WAGEBEN5"] == '1' else 0,
                        "pension_income": line["INPENINC"],
                        "employee_earnings": line["INEARNS"],
                        "self_employed_earnings": line["INCSEO2"] if line["INCSEO2"] != " " else 0,
                        "investment_income": line["ININV"],
                        "hours_worked": line["TOTHOURS"] if line["TOTHOURS"] != " " else 0,
                        "adult_weight": line["GROSS4"],
                        "disabled": line["LAREG"]
                    }
                    for key in person.keys():
                        if key not in string_keys and key not in allowed_to_be_negative:
                            assert float(person[key]) >= 0
                    writer.writerow(person)
                except Exception as e:
                    skipped += 1
            print(f"Adults: skipped {skipped} rows.")
        
        with open(os.path.join(data_dir, "child.tab"), encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=next(f).split("\t"), delimiter="\t")
            skipped = 0
            for line in tqdm(reader, desc="Writing children into person file", total=9849):
                try:
                    string_keys = ["person_id", "household_id", "family_id", "role"]
                    person = {
                        "person_id": line["sernum"] + "p" + line["PERSON"],
                        "household_id": line["sernum"],
                        "family_id": line["sernum"] + "f" + line["BENUNIT"],
                        "role": "child",
                        "age_band": 0,
                        "JSA_receipt": 0,
                        "IS_receipt": 0,
                        "pension_income": 0,
                        "employee_earnings": 0,
                        "self_employed_earnings": 0,
                        "investment_income": 0,
                        "hours_worked": 0,
                        "adult_weight": 0,
                        "disabled": line["LAREG"]
                    }
                    for key in person.keys():
                        if key not in string_keys:
                            assert float(person[key]) >= 0
                    writer.writerow(person)
                except:
                    skipped += 1
            print(f"Children: skipped {skipped} rows.")

def write_family_file(data_dir, output_dir, weights=None):
    with open(os.path.join(output_dir, "family.csv"), "w+", encoding="utf-8", newline="") as g:
        with open(os.path.join(data_dir, "benunit.tab"), encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=next(f).split("\t"), delimiter="\t")
            fieldnames = ["household_id", "family_id", "JSA_actual", "num_children_actual", "income_support_actual", "housing_benefit_actual", "child_tax_credit_actual", "working_tax_credit_actual", "child_benefit_actual", "family_weight"]
            writer = csv.DictWriter(g, fieldnames=fieldnames)
            writer.writeheader()
            skipped = 0
            family_data = {}
            for line in tqdm(reader, desc="Writing families into family file", total=22406):
                try:
                    string_keys = ["household_id", "family_id", "family_structure"]
                    family_id = line["sernum"] + "f" + line["BENUNIT"]
                    try:
                        total_benefit_income = float(line["BUIRBEN"]) + float(line["BUNIRBEN"]) + float(line["BUOTHBEN"])
                    except:
                        total_benefit_income = 0
                    family = {
                        "household_id": line["sernum"],
                        "family_id": family_id,
                        "num_children_actual": line["DEPCHLDB"],
                        "JSA_actual": 0,
                        "child_benefit_actual": 0,
                        "income_support_actual": 0,
                        "housing_benefit_actual": 0,
                        "child_tax_credit_actual": 0,
                        "working_tax_credit_actual": 0,
                        "family_weight": line["GROSS4"]
                    }
                    for key in family.keys():
                        if key not in string_keys:
                            assert float(family[key]) >= 0
                    family_data[family_id] = family
                except Exception as e:
                    skipped += 1
            print(f"Families: skipped {skipped} rows.")
        
        with open(os.path.join(data_dir, "benefits.tab"), encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=next(f).split("\t"), delimiter="\t")
            skipped = 0
            benefit_codes = {
                "14": "JSA",
                "3": "child_benefit",
                "19": "income_support",
                "94": "housing_benefit",
                "91": "child_tax_credit",
                "90": "working_tax_credit"
            }
            for line in tqdm(reader, desc="Writing benefits into family file", total=38475):
                try:
                    family_id = line["sernum"] + "f" + line["BENUNIT"]
                    if line["BENEFIT"] in benefit_codes:
                        family_data[family_id][benefit_codes[line["BENEFIT"]] + "_actual"] = float(line["BENAMT"])
                except:
                    skipped += 1
            print(f"Benefits: skipped {skipped} rows.")

        for family_id, family in tqdm(family_data.items(), desc="Writing family file"):
            writer.writerow(family)
        print("Wrote family file.")

def write_household_file(data_dir, output_dir, weights=None):
    with open(os.path.join(output_dir, "household.csv"), "w+", encoding="utf-8", newline="") as g:
        with open(os.path.join(data_dir, "househol.tab"), encoding="utf-8") as f:
            reader = csv.DictReader(f, fieldnames=next(f).split("\t"), delimiter="\t")
            fieldnames = ["household_id", "household_weight"]
            writer = csv.DictWriter(g, fieldnames=fieldnames)
            writer.writeheader()
            skipped = 0
            for line in tqdm(reader, desc="Writing households into household file", total=19169):
                try:
                    string_keys = ["household_id"]
                    household = {
                        "household_id": line["sernum"],
                        "household_weight": line["GROSS4"]
                    }
                    for key in household.keys():
                        if key not in string_keys:
                            assert float(household[key]) >= 0
                    writer.writerow(household)
                except Exception as e:
                    skipped += 1
            print(f"Households: skipped {skipped} rows.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Utility for generating OpenFisca-UK-compatible input files from Family Resources Survey data files.")
    parser.add_argument("--data_dir", default="csv_generation/UKDA-8633-tab/tab", help="Directory containing FRS TAB files.")
    parser.add_argument("--output_dir", default="inputs", help="Directory in which to store OpenFisca-UK CSV files.")
    args = parser.parse_args()
    clean_dirs(args.output_dir)
    write_person_file(args.data_dir, args.output_dir)
    write_family_file(args.data_dir, args.output_dir)
    write_household_file(args.data_dir, args.output_dir)