from stackapi import *
import requests as req
from bs4 import BeautifulSoup

# output


def output(param):
    print(param)

# gettitng tags from с-ped


def get_tags():
    return ['python', 'sort']

# searching function


def search(tags, min_=20, from_date=1457136000, to_date=1457222400):
    try:
        SITE = StackAPI('stackoverflow')
    except StackAPIError as e:
        print(e.message)

    # GET json tree by tags
    questions = SITE.fetch('questions', fromdate=from_date,
                           todate=to_date, min=min_, tagged=tags, sort='votes')
    answer_id, question_link = [], []

    # extracting url and accepted answer from json tree, if no accepted answer - skip
    for element in questions["items"]:
        try:
            answer_id.append(element['accepted_answer_id'])
            question_link.append(element['link'])
        except:
            pass

    # extracting accepted answer from url by answer-id
    all_code = []
    for i in range(len(question_link)):
        code_from_url = []
        requiredHtml = req.get(question_link[i])
        soup = BeautifulSoup(requiredHtml.content, 'html.parser')
        for data in soup.findAll('div', id='answer-'+str(answer_id[i])):
            for values in data.findAll('code'):
                code_from_url.append(values.text)
        all_code.append(code_from_url)
    return all_code, question_link


output(search(get_tags()))
