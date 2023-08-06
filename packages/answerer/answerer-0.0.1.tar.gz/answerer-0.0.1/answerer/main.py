"""
    Copyright 2020 Andrew Brown (aka SherpDaWerp)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import csv
from time import time
from nspywrapper import nsRequests
from random import choice
# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options

__version__ = "0.0.1"
__browser__ = False


def answer_issues():
    s_time = time()

    # setup
    main_nation_name = "sherpdawerp"  # str(input("Name of your main nation: "))
    assert main_nation_name not in ("", " ", None)
    nsapi = nsRequests("1:1 issue answering script by SherpDaWerp, in use by " + main_nation_name)

    # import files
    auth = []
    try:
        with open("./code/puppets.csv") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                auth.append([row[0].replace(" ", "_"), row[1]])
    except (OSError, FileNotFoundError, IOError) as err:
        print("Oh no!")
        print(err)

    priorities = []
    try:
        with open("./code/priorities.csv") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                priorities.append([row[0], row[1]])
    except (OSError, FileNotFoundError, IOError) as err:
        print("Oh no!")
        print(err)

    try:
        with open("./code/output.txt", "w") as file:
            file.write("")
    except (OSError, FileNotFoundError, IOError):
        pass

    # actual code
    for credentials in auth:
        response = nsapi.nation(credentials[0], "issues", auth=(credentials[1], "", ""))
        for issue in response.data["NATION"]["ISSUES"]:
            issue_id = issue["@id"]
            issue_options = [option["@id"] for option in issue["ISSUE"]["OPTIONS"]]

            if __browser__:
                pass
            else:
                chosen_op = None

                p_id = [priority[0] for priority in priorities]
                try:
                    index = p_id.index(issue_id)
                    if priorities[index][1] in issue_options:
                        chosen_op = priorities[index][1]
                except ValueError:
                    pass

                if chosen_op is None:
                    chosen_op = choice(issue_options)

                out_url = f"https://www.nationstates.net/page=enact_dilemma/choice-{chosen_op}=1/dilemma={issue_id}/" \
                          f"asnation={credentials[0]}/container={credentials[0]}/nation={credentials[0]}/\n"

                with open("./code/output.txt", "a+") as file:
                    file.write(out_url)

        print(credentials[0])

    e_time = time()
    r_time = e_time-s_time
    print("runtime: "+str(r_time)[:5]+" secs")


if __name__ == "__main__":
    answer_issues()