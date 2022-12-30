import allure


def allure_attach_request(response):
    allure.attach(
        # response.url.encode('utf-8').decode('unicode-escape'),
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
