import pytest
from robots_controller.connectors.ServiceProxyConnector import ServiceProxyConnector


# @pytest.mark.getInqueryByNumber
def test_getInqueryByNumber():
    spc = ServiceProxyConnector()
    data = spc.getInqueryByNumber("1-688357270685")

    # print(data)

    assert data


test_getInqueryByNumber()
