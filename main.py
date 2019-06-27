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
    

def get_hh_vacancy_data(lang):
    url = "https://api.hh.ru/vacancies"
    path = {
        'text': 'программист {}'.format(lang),
        'area': 1,
        'period': 30
    }
    data = fetch_json(url, path)
    return data


def get_hh_lang_info(hh_vacancy_data):
    vacancies_count = hh_vacancy_data['found']
    lang_info = {
        lang: {
            'vacancies_found': vacancies_count, 
            'vacancies_processed':'', 
            'average_salary':''
        }
    }
    return lang_info


if __name__ == "__main__":

    langs = ['python', 'java']
    for lang in langs:
        hh_vacancies = get_hh_vacancy_data(lang)
        res = get_hh_lang_info(hh_vacancies)
        print(res)
        



# {
#     "Python": { 
#         "vacancies_found": 1068,
#         "vacancies_processed": 13,
#         "average_salary": 123853
#     },
#     "Java": {
#         "vacancies_found": 1592,
#         "vacancies_processed": 16,
#         "average_salary": 121456
#     },
#     "Javascript": { 
#         "vacancies_found": 3696,
#         "vacancies_processed": 18,
#         "average_salary": 140173
#     }
# }