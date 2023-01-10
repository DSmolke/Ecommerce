from ecomerceapp.ecomerce_service.validator import ServiceDataValidator
from ecomerceapp.tests.test_ecomerce_service.ecommerce_service_fixtures import valid_customer_data, \
    invalid_customer_data, invalid_structured_data, valid_product_data, invalid_product_data, valid_order_data


class TestServiceDataValidator:
    class TestIsCustomerDataValid:
        def test_for_valid_data(self, valid_customer_data):
            assert ServiceDataValidator.is_customer_data_valid(valid_customer_data)

        def test_for_invalid_data(self, invalid_customer_data):
            assert ServiceDataValidator.is_customer_data_valid(invalid_customer_data) is False

        def test_for_invalid_structured_dict(self, invalid_structured_data):
            assert ServiceDataValidator.is_customer_data_valid(invalid_structured_data) is False

    class TestIsProductDataValid:
        def test_for_valid_data(self, valid_product_data):
            assert ServiceDataValidator.is_product_data_valid(valid_product_data)

        def test_for_invalid_data(self, invalid_product_data):
            assert ServiceDataValidator.is_product_data_valid(invalid_product_data) is False

        def test_for_invalid_structured_dict(self, invalid_structured_data):
            assert ServiceDataValidator.is_product_data_valid(invalid_structured_data) is False

    class TestValidateOrderData:
        def test_for_valid_data(self, valid_order_data):
            assert ServiceDataValidator.validate_order_data(valid_order_data)

        def test_for_invalid_structured_dict(self, invalid_structured_data):
            assert ServiceDataValidator.validate_order_data(invalid_structured_data) is False
