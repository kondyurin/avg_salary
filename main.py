import os
import requests
from itertools import count
from statistics import mean
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('SJ_TOKEN')


def fetch_json(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data


def predict_rub_salary(vacancy):
    if not vacancy or vacancy['currency'] != 'RUR':
        return None
    salary_from = vacancy['from']
    salary_to = vacancy['to'] 
    if salary_from:
        salary = salary_from * 1.2
    elif salary_to:
        salary = salary_to * 0.8
    else:
        salary = (salary_from + salary_to)/2
    return salary
    

def get_mean_salary(vacancy_salaries):
    new = [salary for salary in vacancy_salaries if salary is not None]
    return int(mean(new))


def get_vacancies_processed(vacancy_salaries):
    new = [salary for salary in vacancy_salaries if salary is not None]
    return len(new)


def get_sj_vacancy_data():
    path = {
        'town': 4,
        'catalogues': 48
    }
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': TOKEN
    }
    data = fetch_json(url, path, headers)
    for item in data['objects']:
        print(item['profession'], item['town']['title'])

# def get_hh_vacancy_data(lang):
#     data_result = []
#     for page in count():
#         url = "https://api.hh.ru/vacancies"
#         path = {
#             'text': 'программист {}'.format(lang),
#             'area': 1,
#             'period': 30,
#             'page': page
#         }
#         data = fetch_json(url, path)
#         data_result.append(data)
#         if page >= data['pages']:
#             break
#     return data_result


# def get_hh_lang_info(hh_vacancy_data):
#     salaries = []
#     for item in hh_vacancy_data:
#         for vacancy in item['items']:
#             salaries.append(predict_rub_salary(vacancy['salary']))
#     vacancies_count = item['found']
#     mean_salary = get_mean_salary(salaries)
#     vacancy_salaries = get_vacancies_processed(salaries)
#     return vacancies_count, mean_salary, vacancy_salaries


if __name__ == "__main__":
    # lang_info = dict()
    # langs = ['python', 'java']
    # for lang in langs:
    #     vacancy_data = get_hh_vacancy_data(lang)
    #     vacancies_count, mean_salary, vacancy_salaries = get_hh_lang_info(vacancy_data)
    #     lang_info.update(
    #         {
    #             lang: {
    #                 "vacancies_count": vacancies_count, 
    #                 "vacancies_processed": vacancy_salaries,
    #                 "average_salary": mean_salary
    #             }
    #         }
    #     )
    # print(lang_info)
    res = get_sj_vacancy_data()
    print(res)