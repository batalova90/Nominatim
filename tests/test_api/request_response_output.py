import allure
import requests


def allure_attach_request(response):
    allure.attach(
        response.url,
        name='Request: ',
        attachment_type=allure.attachment_type.TEXT
    )


def allure_attach_response(response):
    allure.attach(
        response.text,
        name='Response: ',
        attachment_type=allure.attachment_type.JSON
    )
