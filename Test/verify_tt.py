import os
import json

PREFIX = "python3 ../Python/tt.py"
# "dotnet run --project ../CSharp/TimeTracker.csproj"

COMMENT = "test comment"

f = open("../Messages/Errors.json")
ERROR_MESSAGES = json.load(f)

# TODO: punch in at 11:59 pm and pucnh out 12:01 am next day

tests = [
        # Tests for no database
        [1, PREFIX, " status",       ERROR_MESSAGES["NO_ENTRIES"]],
        [2, PREFIX, " show month",   ERROR_MESSAGES["NO_ENTRIES"]],
        [3, PREFIX, f" o {COMMENT}", ERROR_MESSAGES["NO_ENTRIES"]],
        [4, PREFIX, f" i {COMMENT}", ERROR_MESSAGES["PUNCHIN_SUCCESS"]],
        [5, PREFIX, f" i {COMMENT}", ERROR_MESSAGES["INVALID_STATE"]],
        [6, PREFIX, " status",       "Display"],
        [7, PREFIX, f" o {COMMENT}", ERROR_MESSAGES["PUNCHIN_SUCCESS"]],
        [8, PREFIX, f" o {COMMENT}", ERROR_MESSAGES["INVALID_STATE"]],
        [9, PREFIX, " status",       "Display"],
]

if __name__ == "__main__":
    for test in tests:
        output = os.popen(str(test[1]) + str(test[2])).read()

        if test[3] == "Display":
            print(output)
        elif output == test[3]:
            print(f"{test[0]} : PASS")
        else:
            print(f"{test[0]} : FAIL")
