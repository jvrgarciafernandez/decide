'''
import unittest
from selenium import webdriver
import os


class TestSignup(unittest.TestCase):

    def setUp(self):
        locate = os.name
        if locate == 'nt':
            self.path = os.path.realpath("../drivers/phantomjs.exe")
        else:
            self.path = os.path.realpath("../drivers/phantomjs")
        self.driver = webdriver.PhantomJS(executable_path=self.path)

    # Test 1:
    # Testing that the graph is showed to the user on a tallied test
    # Must return true if the canvas is displayer
    def test_exist_canvas_on_tallied_test(self):
        self.driver.get("http://localhost:8000/visualizer/3/")
        canvas = self.driver.find_elements_by_tag_name("canvas")
        self.assertTrue(len(canvas) > 0)

    # Test 2
    # Testing there is a form to change the chartjs type of the representation
    # Must return true if there are 1 select displayed and 5 options
    # inside the select
    def test_form_select_tallied_test(self):
        self.driver.get("http://localhost:8000/visualizer/2/")
        select = self.driver.find_elements_by_tag_name("select")
        options = self.driver.find_elements_by_tag_name("option")
        self.assertTrue(len(select) == 1 and len(options) == 5)


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()

'''