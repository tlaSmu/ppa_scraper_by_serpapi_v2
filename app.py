import csv
import queue
from serpapi import GoogleSearch
from time import sleep



def write_data(filename, res_data):
    with open(f'{filename}', 'a', encoding='utf-8') as res_file:
        res_file.write(res_data)

def clear_file(filename):
    with open(f"{filename}",'w') as f:
        pass


def get_list_of_paa_google(keyword, L, api_key):
    params = {
        "q": keyword,
        "location": "Austin, Texas, United States",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "us",
        "api_key": api_key
    }
    
    search = GoogleSearch(params)
    
    try:
        results = search.get_dict()
        related_questions = results["related_questions"]

        for res in related_questions:
            question = res['question']

            # snippet = res['snippet']
            #data = f"\"google\",\"{keyword}\",\"{question}\",\"{snippet}\"\n"
            data = f"\"google\",\"{keyword}\",\"{question}\"\n"
            write_data('result.csv', data)

            try:
                next_page_token = res['next_page_token']
                get_paa_from_next_page(keyword, next_page_token, L, api_key)
            except KeyError:
                print('null')

        return related_questions
    except Exception as e:
        print(e.message)
        print('=========')
        print(e.args)


def get_paa_from_next_page(keyword, next_page_token, L, api_key):
    params = {
    "engine": "google_related_questions",
    "next_page_token": next_page_token,
    "api_key": api_key 
    }
    search = GoogleSearch(params)
    
    try:
        results = search.get_dict()
        related_questions = results["related_questions"]

        for res in related_questions:
            question = res['question']

            #snippet = res['snippet']
            #data = f"\"google\",\"{keyword}\",\"{question}\",\"{snippet}\"\n"
            data = f"\"google\",\"{keyword}\",\"{question}\"\n"
            write_data('result.csv', data)

            next_page_token = res['next_page_token']
            L.put(next_page_token)

        return related_questions
    except KeyError:
        print(keyword+' -- Google is null')

    

# main
data = f"\"se\",\"keyword\",\"question\",\"snippet\"\n"
write_data('result', data)
L = queue.Queue()
Fake_L = queue.Queue()
api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

with open('cluster.csv', mode='r') as infile:
    reader = csv.reader(infile)

    for row in reader:
        keyword = row[0]
        print('=================')
        get_list_of_paa_google(keyword, L, api_key)

        for _ in range(50):
            next_page_token = L.get()
            get_paa_from_next_page(keyword, next_page_token, L, api_key)
            print(L.qsize())

        for _ in range(L.qsize()):
            next_page_token = L.get()
            get_paa_from_next_page(keyword, next_page_token, Fake_L, api_key)
            print(L.qsize())
        
print(' == DONE ==')