import requests


def fetch_json(url, params):
    response = requests.get(url, params=params)
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
    

def get_hh_vacancy():
    result = []
    lang_salary = dict()
    langs = ['python', 'java']
    url = "https://api.hh.ru/vacancies"
    for lang in langs:
        path = {
            'text': 'программист {}'.format(lang),
            'area': 1,
            'period': 30
        }
        data = fetch_json(url, path)
        result.append(data)
    return result


def get_avg_salary_hh(hh_vacancies):
    for lang in hh_vacancies:
        vacancies_found = lang['found']
        vacancies_data = lang['items']
        print(vacancies_found) # 6 step of 17


if __name__ == "__main__":
    hh_vacancies = get_hh_vacancy()
    get_avg_salary_hh(hh_vacancies)