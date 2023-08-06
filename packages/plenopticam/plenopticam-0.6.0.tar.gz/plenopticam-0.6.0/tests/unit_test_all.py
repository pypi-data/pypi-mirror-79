from tests.unit_test_custom import PlenoptiCamTesterCustom
from tests.unit_test_illum import PlenoptiCamTesterIllum
from tests.unit_test_cli import PlenoptiCamTesterCli
from tests.unit_test_gui import PlenoptiCamTesterGui
from tests.unit_test_err import PlenoptiCamErrorTester

test_classes = [PlenoptiCamTesterCli, PlenoptiCamErrorTester,
                PlenoptiCamTesterCustom, PlenoptiCamTesterIllum, PlenoptiCamTesterGui]

for test_class in test_classes:
    obj = test_class()
    obj.setUp()
    obj.test_all()
    del obj
