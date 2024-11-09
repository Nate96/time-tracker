import os
import json
from datetime import datetime

# TODO: import presenter form Python/ dir. Delete present in current dir
import presenter

PREFIX = "python3 ../Python/tt.py"
# "dotnet run --project ../CSharp/TimeTracker.csproj"

COMMENT = "test comment"

f = open("../Messages/Errors.json")
ERROR_MESSAGES = json.load(f)

in_timestamp = str(datetime.now())
out_timestamp = str(datetime.now())

tests = [
        # Tests for no database
        [1, PREFIX, " status",       ERROR_MESSAGES["NO_ENTRIES"]],
        [2, PREFIX, " show month",   ERROR_MESSAGES["NO_ENTRIES"]],
        [3, PREFIX, f" o {COMMENT}", ERROR_MESSAGES["NO_ENTRIES"]],
        [4, PREFIX, f" i {COMMENT}", presenter.format_punch((1,
                                                             "in",
                                                             in_timestamp,
                                                             COMMENT))],
        [6, PREFIX, f" i {COMMENT}", ERROR_MESSAGES["PUNCHIN_INVALID"]],
        [7, PREFIX, f" o {COMMENT}", presenter.format_entry((1,
                                                             in_timestamp,
                                                             out_timestamp,
                                                             1.0,
                                                             COMMENT,
                                                             COMMENT))],
        [8, PREFIX, f" o {COMMENT}", ERROR_MESSAGES['PUNCHOUT_INVALID']],
]

if __name__ == "__main__":
    for test in tests:
        if test[0] == 7:
            os.wait(60)

        output = os.popen(str(test[1]) + str(test[2])).read()

        if test[3] == "Display":
            print(output)
        elif output == test[3]:
            print(f"{test[0]} : PASS")
            print(f"ex: {test[3]}, act: {output}")
        else:
            print(f"{test[0]} : FAIL")
            print(f"ex: {test[3]}, act: {output}")
