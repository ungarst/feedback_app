import sys, re, os

for file_name in os.listdir("errors/"):

    with open("temp.html", "r") as f:
        html_data = f.read()



    with open("errors/" + file_name, "r") as f:
        error_data = f.read()

    html_data = re.sub (r'\<DAVES\-CODE\>', error_data, html_data)


    with open("fitted-errors/" + file_name, "w") as f:
        f.write(html_data)
