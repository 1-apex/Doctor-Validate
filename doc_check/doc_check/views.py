import time
from abc import ABC

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def index(request):
    return render(request, 'index.html')


def submit(request):
    if request.method == 'POST':

        params = {'name': '', 'reg_num': 0, 'content': ''}
        name = request.POST.get('doc_name', '')
        reg_num = request.POST.get('doc_reg_num', 0)
        params['name'] = name
        params['reg_num'] = reg_num
        params['content'] = check(request, name, reg_num)
        if params['content']:
            return render(request, 'render.html', params)
        return HttpResponse("<h2>Doctor Invalid</h2>")


def check(request, name, registration_number):
    driver = webdriver.Chrome()

    url = 'https://www.nmc.org.in/information-desk/indian-medical-register/'
    driver.get(url)

    username_input = driver.find_element(By.ID, 'doctorName')
    username_input.send_keys(name)

    password_input = driver.find_element(By.ID, 'doctorRegdNo')
    password_input.send_keys(registration_number)

    submit_button = driver.find_element(By.ID, 'doctor_advance_Details')
    submit_button.click()

    time.sleep(8)

    window_handles = driver.window_handles

    if len(window_handles) > 1:
        new_window_handle = window_handles[-1]
        driver.switch_to.window(new_window_handle)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'id': 'doct_info5'})

    empty_cell = table.find('td', {'class': 'dataTables_empty'})
    if empty_cell and "No data available" in empty_cell.text:
        driver.quit()
        return False

    column_names = ['sr_no', 'Year of Info', 'Registration Number', 'State', 'Name']
    data_rows = []

    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            row_data = []
            row_data = [cell.text.strip() for cell in cells]
            data_rows.append(row_data)

    data_rows = [row[:-2] for row in data_rows]

    driver.quit()

    return data_rows[-1][-1]
