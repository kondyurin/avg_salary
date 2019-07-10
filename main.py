import os
import math
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


def get_predict_salary(salary_from, salary_to):
    if salary_from:
        salary = salary_from * 1.2
    elif salary_to:
        salary = salary_to * 0.8
    else:
        salary = (salary_from + salary_to)/2
    return salary


def predict_rub_salary_hh(vacancy):
    if not vacancy or vacancy['currency'] != 'RUR':
        return None
    salary_from = vacancy['from']
    salary_to = vacancy['to'] 
    return get_predict_salary(salary_from, salary_to)


def predict_rub_salary_sj(vacancy):
    if not vacancy or vacancy['currency'] != 'rub':
        return None
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']  # может не быть в ответе api
    return get_predict_salary(salary_from, salary_to)


def get_mean_salary(vacancy_salaries):
    new = [salary for salary in vacancy_salaries if salary is not None]
    return int(mean(new))


def get_vacancies_processed(vacancy_salaries):
    new = [salary for salary in vacancy_salaries if salary is not None]
    return len(new)


def get_sj_vacancy_data(lang):
    data_result = []
    for page in count():
        print(page)
        path = {
            'profession': 'программист {}'.format(lang),
            'town': 4,
            'catalogues': 48,
            'count': 20,
            'page': page
        }
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': TOKEN
        }
        data = fetch_json(url, path, headers)
        pages = math.ceil(data['total']/path['count']) - 1
        data_result.append(data)
        if page >= pages:
            break
    return data_result


def get_sj_lang_info(sj_vacancy_data):
    salaries = []
    for item in sj_vacancy_data:
        for vacancy in item['objects']:
            salaries.append(predict_rub_salary_sj(vacancy))
    salaries = [salary for salary in salaries if salary != 0]
    vacancies_count = item['total']
    mean_salary = get_mean_salary(salaries)
    vacancy_salaries = get_vacancies_processed(salaries)
    return vacancies_count, mean_salary, vacancy_salaries


def get_hh_vacancy_data(lang):
    data_result = []
    for page in count():
        url = "https://api.hh.ru/vacancies"
        path = {
            'text': 'программист {}'.format(lang),  # если текст в названии вакансии, условие 
            'area': 1,
            'period': 30,
            'page': page
        }
        data = fetch_json(url, path, headers={})
        data_result.append(data)
        if page >= data['pages']:
            break
    return data_result


def get_hh_lang_info(hh_vacancy_data):
    salaries = []
    for item in hh_vacancy_data:
        for vacancy in item['items']:
            salaries.append(predict_rub_salary_hh(vacancy['salary']))
    vacancies_count = item['found']  # проверить!
    mean_salary = get_mean_salary(salaries)
    vacancy_salaries = get_vacancies_processed(salaries)
    return vacancies_count, mean_salary, vacancy_salaries


if __name__ == "__main__":
    lang_info_hh = dict()
    lang_info_sj = dict()
    langs = ['python', 'java']
    for lang in langs:
        vacancy_data_hh = get_hh_vacancy_data(lang)
        vacancy_data_sj = get_sj_vacancy_data(lang)
        vacancies_count_hh, mean_salary_hh, vacancy_salaries_hh = get_hh_lang_info(vacancy_data_hh)
        vacancies_count_sj, mean_salary_sj, vacancy_salaries_sj = get_sj_lang_info(vacancy_data_sj)
        lang_info_hh.update(  # в отдельную функцию
            {
                lang: {
                    "vacancies_count": vacancies_count_hh, 
                    "vacancies_processed": vacancy_salaries_hh,
                    "average_salary": mean_salary_hh
                }
            }
        )
        lang_info_sj.update(
            {
                lang: {
                    "vacancies_count": vacancies_count_sj, 
                    "vacancies_processed": vacancy_salaries_sj,
                    "average_salary": mean_salary_sj
                }
            }
        )
    print(lang_info_hh)
    print(lang_info_sj)