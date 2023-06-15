from unittest import TestCase
from django.test import Client
from django.urls import reverse
import json
import pytest

from companies.models import Company


@pytest.mark.django_db
class BasicCompanyApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")
    
    def tearDown(self) -> None:
        pass


class TestGetCompanies(BasicCompanyApiTestCase):
    
    def test_zero_companies_should_return_empty_list(self)->None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self)->None:
        test_company = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response_content.get("name"), "Amazon")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

        test_company.delete()


class TestPostCompanies(BasicCompanyApiTestCase):
    def test_create_company_without_arguments_should_fail(self)->None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)

    def test_create_existing_company_should_fail(self)->None:
        Company.objects.create(name="apple")
        response = self.client.post(path=self.companies_url,
                                    data={"name":"apple"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content),
                         {"name":["company with this name already exists."]})
    
    def test_create_company_only_name_all_fields_should_be_default(self)->None:
        response = self.client.post(path=self.companies_url,
                                    data={"name":"test company name"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_should_succeed(self)->None:
        response = self.client.post(path=self.companies_url,
                                    data={"name":"test company name",
                                          "status": "Layoffs"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("status"), "Layoffs")
    
    def test_create_company_with_wrong_status_should_fail(self)->None:
        response = self.client.post(path=self.companies_url,
                                    data={"name":"test company name",
                                          "status": "WrongStatus"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("WrongStatus", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))

@pytest.mark.xfail
def test_should_be_xfail()->None:
    assert 1 == 2

@pytest.mark.skip
def test_should_be_skipped()->None:
    assert 1 == 1
    
def raise_covid19_exception()->None:
    raise ValueError("Covid19-Error")
    
def test_raise_covid19_exception_should_be_pass()->None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "Covid19-Error" == str(e.value)

import logging

logger = logging.getLogger("CORONA_LOGS")

def function_that_logs_something()-> None:
    try:
        raise ValueError("CoronaVirusException")
    except ValueError as e:
        logger.warning(f"I am logging in {str(e)}")

def test_logged_warning_level(caplog)->None:
    function_that_logs_something()
    assert "I am logging in CoronaVirusException" in caplog.text

def test_logged_info_level(caplog)->None:
    with caplog.at_level(logging.INFO):
        logger.info("I am loggin at info level")
        assert "I am loggin at info level" in caplog.text
