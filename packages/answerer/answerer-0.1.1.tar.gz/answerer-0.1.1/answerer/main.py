"""
    Copyright 2020 9003
    Modifications Copyright 2020 Andrew Brown (aka SherpDaWerp)

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

from csv import reader
from nspywrapper import nsRequests
from time import time
from random import choice
# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options
# from bs4 import BeautifulSoup

__browser__ = False
ALLOWABLE = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
             "12", "13", "14", "15", "16", "17", "18", "19", "20", "!")


def answer_issues():
    s_time = time()

    # setup
    main_nation_name = str(input("Name of your main nation: "))
    assert main_nation_name not in ("", " ", None)
    nsapi = nsRequests("manual issue answering script-thing by SherpDaWerp, in use by " + main_nation_name)

    # import files
    auth = []
    try:
        with open("./puppets.csv") as csv_file:
            csv_reader = reader(csv_file)
            for row in csv_reader:
                auth.append([row[0].replace(" ", "_"), row[1]])
    except (OSError, FileNotFoundError, IOError) as err:
        print("Oh no!")
        print(err)

    priorities = []
    try:
        with open("./priorities.csv") as csv_file:
            csv_reader = reader(csv_file)
            for row in csv_reader:
                priorities.append([row[0], row[1]])
    except (OSError, FileNotFoundError, IOError) as err:
        print("Oh no!")
        print(err)

    with open("./output.txt", "w+") as file:
        file.write("")

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

                if chosen_op is None or chosen_op not in ALLOWABLE:
                    chosen_op = choice(issue_options)

                if chosen_op != "!":
                    out_url = f"https://www.nationstates.net/container={credentials[0]}/page=enact_dilemma/" \
                              f"choice-{chosen_op}=1/dilemma={issue_id}/template-overall=none/" \
                              f"nation={credentials[0]}/asnation={credentials[0]}"
                else:
                    out_url = f"https://www.nationstates.net/container={credentials[0]}/page=show_dilemma/" \
                              f"dilemma={issue_id}/nation={credentials[0]}/asnation={credentials[0]}"

                with open("./output.txt", "a+") as file:
                    file.write(out_url)

        print(credentials[0])

    e_time = time()
    r_time = e_time-s_time
    print("\nruntime: "+str(r_time)[:5]+" secs")


def generate_links():
    with open('output.txt') as f:
        puppets = f.read().split('\n')

    puppets = list(filter(None, puppets))

    links = """
    <html>
    <head>
    <style>
    td.createcol p {
        padding-left: 10em;
    }

    a {
        text-decoration: none;
        color: black;
    }

    a:visited {
        color: grey;
    }

    table {
        border-collapse: collapse;
        display: table-cell;
        max-width: 100%;
    }

    td p {
        padding: 0.5em;
    }

    tr:hover {
        background-color: lightgrey;
    }

    </style>
    </head>
    <body>
    <table>
    """

    for k in puppets:
        links += f'<tr><td><p><a target="_blank" href="{k}">Link to Issue</a></p></td></tr>\n'

    links += '<tr><td><p><a target="_blank"' \
             'href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td></tr>'
    links += """
    </table>
    <script>
    document.querySelectorAll("td").forEach(function(el) {
        el.addEventListener("click", function() {
            let myidx = 0;
            const row = el.parentNode;
            let child = el;
            while((child = child.previousElementSibling) != null) {
                myidx++;
            }
            row.nextElementSibling.childNodes[myidx].querySelector("p > a").focus();
            row.parentNode.removeChild(row);
        });
    });
    </script>
    </body>
    """

    with open("./output.html", "w+") as f:
        f.write(links)
