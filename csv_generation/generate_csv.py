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


def safe(*texts):
    num = 0
    for text in texts:
        try:
            num += float(text)
        except:
            pass
    return num


def write_person_file(data_dir, output_dir):
    with open(
        os.path.join(output_dir, "person.csv"),
        "w+",
        encoding="utf-8",
        newline="",
    ) as g:
        with open(os.path.join(data_dir, "adult.tab"), encoding="utf-8") as f:
            reader = csv.DictReader(
                f, fieldnames=next(f).split("\t"), delimiter="\t"
            )
            fieldnames = [
                "person_id",
                "household_id",
                "benunit_id",
                "role",
                "is_male",
                "is_head",
                "is_state_pension_age",
                "age_band",
                "hours_worked",
                "adult_weight",
                "disabled",
            ]
            same_name_fields = [
                "INEARNS",
                "SEINCAM2",
                "ININV",
                "INTXCRED",
                "INDISBEN",
                "INOTHBEN",
                "INRPINC",
                "INPENINC",
                "INRINC",
                "INDUC",
                "INDINC",
                "NINDINC",
            ]
            writer = csv.DictWriter(
                g, fieldnames=fieldnames + same_name_fields
            )
            writer.writeheader()
            skipped = 0
            person_data = {}
            for line in tqdm(
                reader, desc="Writing adults into person file", total=33238
            ):
                try:
                    person_id = (
                        line["sernum"]
                        + "f"
                        + line["BENUNIT"]
                        + "p"
                        + line["PERSON"]
                    )
                    person = {
                        "person_id": line["sernum"] + "p" + line["PERSON"],
                        "household_id": line["sernum"],
                        "benunit_id": line["sernum"] + "f" + line["BENUNIT"],
                        "is_male": line["SEX"] == 1,
                        "is_head": line["COMBID"] == 1,
                        "is_state_pension_age": line["PENFLAG"] == "1",
                        "role": "adult",
                        "age_band": int(line["IAGEGR4"]),
                        "hours_worked": safe(line["TOTHOURS"]),
                        "adult_weight": line["GROSS4"],
                        "disabled": line["DISACTA1"] == "1",
                    }
                    for field in same_name_fields:
                        person[field] = safe(line[field])
                    person_data[person_id] = person
                except:
                    skipped += 1
            print(f"Adults: skipped {skipped} rows.")

        with open(os.path.join(data_dir, "child.tab"), encoding="utf-8") as f:
            reader = csv.DictReader(
                f, fieldnames=next(f).split("\t"), delimiter="\t"
            )
            skipped = 0
            for line in tqdm(
                reader, desc="Writing children into person file", total=9849
            ):
                try:
                    person_id = (
                        line["sernum"]
                        + "f"
                        + line["BENUNIT"]
                        + "p"
                        + line["PERSON"]
                    )
                    person = {
                        "person_id": line["sernum"] + "p" + line["PERSON"],
                        "household_id": line["sernum"],
                        "benunit_id": line["sernum"] + "f" + line["BENUNIT"],
                        "role": "child",
                        "age_band": 0,
                        "hours_worked": 0,
                        "adult_weight": 0,
                        "disabled": line["DISACTC1"] == "1",
                    }
                    for field in same_name_fields:
                        person[field] = 0
                    person["INRINC"] = safe(line["CHRINC"])
                    person["INEARNS"] = safe(line["CHEARNS"])
                    person_data[person_id] = person
                except:
                    skipped += 1
            print(f"Children: skipped {skipped} rows.")

        with open(
            os.path.join(data_dir, "benefits.tab"), encoding="utf-8"
        ) as f:
            reader = csv.DictReader(
                f, fieldnames=next(f).split("\t"), delimiter="\t"
            )
            skipped = 0
            benefit_codes = {}
            for line in tqdm(
                reader, desc="Writing benefits into person file", total=38475
            ):
                try:
                    person_id = (
                        line["sernum"]
                        + "f"
                        + line["BENUNIT"]
                        + "p"
                        + line["PERSON"]
                    )
                    if line["BENEFIT"] in benefit_codes:
                        person_data[person_id][
                            benefit_codes[line["BENEFIT"]] + "_actual"
                        ] = float(line["BENAMT"])
                except:
                    skipped += 1
            print(f"Benefits: skipped {skipped} rows.")

        for person_id, person in tqdm(
            person_data.items(), desc="Writing person file"
        ):
            writer.writerow(person)
        print("Wrote person file.")


def write_benunit_file(data_dir, output_dir, weights=None):
    with open(
        os.path.join(output_dir, "benunit.csv"),
        "w+",
        encoding="utf-8",
        newline="",
    ) as g:
        with open(
            os.path.join(data_dir, "benunit.tab"), encoding="utf-8"
        ) as f:
            reader = csv.DictReader(
                f, fieldnames=next(f).split("\t"), delimiter="\t"
            )
            fieldnames = [
                "household_id",
                "benunit_id",
                "benunit_weight",
            ]
            skipped = 0
            benunit_data = {}
            benefit_codes = {
                "1": "DLA_SC",
                "2": "DLA_M",
                "3": "child_benefit",
                "4": "pension_credit",
                "5": "state_pension",
                "6": "BSP",
                "8": "AFCS",
                "10": "SDA",
                "12": "AA",
                "13": "carers_allowance",
                "15": "IIDB",
                "16": "ESA",
                "17": "incapacity_benefit",
                "19": "income_support",
                "21": "maternity_allowance",
                "37": "guardians_allowance",
                "62": "winter_fuel_payments",
                "90": "working_tax_credit",
                "91": "child_tax_credit",
                "94": "housing_benefit",
                "95": "universal_credit",
                "96": "PIP_DL",
                "97": "PIP_M",
            }
            benefit_names = list(
                map(
                    lambda benefit: benefit + "_reported",
                    benefit_codes.values(),
                )
            )
            contr = "JSA_contributory"
            inc = "JSA_income"
            comb = "JSA_combined"
            JSA_names = list(
                map(lambda x: x + "_reported", [contr, inc, comb])
            )
            JSA_types = {
                "1": contr,
                "2": inc,
                "3": contr,
                "4": inc,
                "5": comb,
                "6": comb,
            }
            writer = csv.DictWriter(
                g, fieldnames=fieldnames + benefit_names + JSA_names
            )
            writer.writeheader()
            for line in tqdm(
                reader, desc="Writing benunits into benunit file", total=22406
            ):
                try:
                    benunit_id = line["sernum"] + "f" + line["BENUNIT"]
                    benunit = {
                        "household_id": line["sernum"],
                        "benunit_id": benunit_id,
                        "benunit_weight": line["GROSS4"],
                    }
                    for field in benefit_names + JSA_names:
                        benunit[field] = 0
                    benunit_data[benunit_id] = benunit
                except:
                    skipped += 1
            print(f"Benunits: skipped {skipped} rows.")

        with open(
            os.path.join(data_dir, "benefits.tab"), encoding="utf-8"
        ) as f:
            reader = csv.DictReader(
                f, fieldnames=next(f).split("\t"), delimiter="\t"
            )
            skipped = 0
            for line in tqdm(
                reader, desc="Writing benefits into benunit file", total=38475
            ):
                try:
                    benunit_id = line["sernum"] + "f" + line["BENUNIT"]
                    code = line["BENEFIT"]
                    if code in benefit_codes:
                        benunit_data[benunit_id][
                            benefit_codes[code] + "_reported"
                        ] = safe(line["BENAMT"])
                    elif code == "14":
                        benunit_data[benunit_id][
                            JSA_types[line["VAR2"]] + "_reported"
                        ] = safe(line["BENAMT"])
                except:
                    skipped += 1
            print(f"Benefits: skipped {skipped} rows.")

        for benunit_id, benunit in tqdm(
            benunit_data.items(), desc="Writing benunit file"
        ):
            writer.writerow(benunit)
        print("Wrote benunit file.")


def write_household_file(data_dir, output_dir, weights=None):
    with open(
        os.path.join(output_dir, "household.csv"),
        "w+",
        encoding="utf-8",
        newline="",
    ) as g:
        with open(
            os.path.join(data_dir, "househol.tab"), encoding="utf-8"
        ) as f:
            reader = csv.DictReader(
                f, fieldnames=next(f).split("\t"), delimiter="\t"
            )
            fieldnames = [
                "household_id",
                "household_weight",
                "housing_cost",
                "council_tax",
            ]
            writer = csv.DictWriter(g, fieldnames=fieldnames)
            writer.writeheader()
            skipped = 0
            for line in tqdm(
                reader,
                desc="Writing households into household file",
                total=19169,
            ):
                try:
                    string_keys = ["household_id"]
                    household = {
                        "household_id": line["sernum"],
                        "household_weight": line["GROSS4"],
                        "housing_cost": safe(line["GBHSCOST"]),
                        "council_tax": safe(line["CTANNUAL"]) / 52,
                    }
                    for key in household.keys():
                        if key not in string_keys:
                            assert float(household[key]) >= 0
                    writer.writerow(household)
                except:
                    skipped += 1
            print(f"Households: skipped {skipped} rows.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility for generating OpenFisca-UK-compatible input files from Family Resources Survey data files."
    )
    parser.add_argument(
        "--data_dir",
        default="csv_generation/UKDA-8633-tab/tab",
        help="Directory containing FRS TAB files.",
    )
    parser.add_argument(
        "--output_dir",
        default="inputs",
        help="Directory in which to store OpenFisca-UK CSV files.",
    )
    args = parser.parse_args()
    clean_dirs(args.output_dir)
    write_person_file(args.data_dir, args.output_dir)
    write_benunit_file(args.data_dir, args.output_dir)
    write_household_file(args.data_dir, args.output_dir)
