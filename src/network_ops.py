import requests

import csv

def report_error(msg):
    error_dict={"error":msg}
    url='https://jsonplaceholder.typicode.com/posts'
    requests.post(url,data=error_dict)


def read_usernames():
    with open("data/users.csv", "r") as user_data:
        reader = csv.reader(user_data)

        next(reader)  

        row_count = 0
        for row in reader:
            print(row[0])  
            row_count += 1
            if row_count == 5:
                break



if __name__=="__main__":
    report_error("Service not found error")
    read_usernames()