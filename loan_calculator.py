import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, required=False, choices=["annuity", "diff"], help="")
parser.add_argument("--principal", type=int, required=False, help="")
parser.add_argument("--periods", type=int, required=False, help="")
parser.add_argument("--interest", type=float, required=False, help="")
parser.add_argument("--payment", type=int, required=False, help="")

args = vars(parser.parse_args())

type_ = args["type"]
a = args["payment"]
p = args["principal"]
interest = args["interest"]
n = args["periods"]

if (type_ is None) or (type_ == "diff" and a is not None) or (interest is None) or (n is not None and n < 0):
    print("Incorrect parameters")
else:
    i = interest / (12 * 100)
    if type_ == "diff":
        overpayment = p
        for m in range(1, n + 1):
            d1 = math.ceil(p/n + i * (p - p*(m - 1)/n))
            overpayment -= d1
            print(f"Month {m}: paid out {d1}")
        print(f"\r\nOverpayment = {abs(overpayment)}")
    elif type_ == "annuity":
        if n is None:
            n = math.ceil(math.log(a / (a - i * p), 1 + i))
            years = n // 12
            months = n % 12
            print(f"You need {years} years and {months} months to repay this credit!")
        elif p is None:
            p = math.floor(a / (i / (1 - 1 / math.pow(1 + i, n))))
            print(f"Your credit principal = {p}!")
        else:
            a = math.ceil(p * i / (1 - 1 / math.pow(1 + i, n)))
            print(f"Your annuity payment = {a}!")
        overpayment = n * a - p
        print(f"Overpayment = {overpayment}")

# sql = "INSERT INTO meals (meal_name) VALUES (?)"
# val = list(data["meals"])
# val2 = [[x] for x in val]
# cur.executemany(sql, val2)
