import csv

with open("inputs/example_input.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(
        csvfile, quotechar='"', delimiter=",", quoting=csv.QUOTE_MINIMAL
    )
    print(list(reader))
