import unittest
import tempfile
import shutil
import sys
from sbol.document import *

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEST_LOC_SBOL2 = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL2')
FILES_SBOL2 = os.listdir(TEST_LOC_SBOL2)
FILES_SBOL2.sort()
TEST_FILES_SBOL2 = []
for i in FILES_SBOL2:
    if i.endswith('rdf'):
        TEST_FILES_SBOL2.append(i)
    if i.endswith('xml'):
        TEST_FILES_SBOL2.append(i)


class TestRoundTripSBOL2(unittest.TestCase):
    def setUp(self):
        # Create temp directory
        self.temp_out_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove directory after the test
        shutil.rmtree(self.temp_out_dir)

    def run_round_trip(self, test_file):
        print(str(test_file))
        split_path = os.path.splitext(test_file)
        self.doc = Document()   # Document for read and write
        self.doc.read(os.path.join(TEST_LOC_SBOL2,
                                   split_path[0] + split_path[1]))
        self.doc.write(os.path.join(self.temp_out_dir, split_path[0] +
                                    '_out' + split_path[1]))

        self.doc2 = Document()  # Document to compare for equality
        self.doc2.read(os.path.join(self.temp_out_dir, split_path[0] +
                                    '_out' + split_path[1]))
        self.assertTrue(self.doc.compare(self.doc2))

    def test_sbol2_files(self):
        subtest = 1
        for f in TEST_FILES_SBOL2:
            with self.subTest(filename=f):
                self.setUp()
                self.run_round_trip(f)
                self.tearDown()


class TestRoundTripFailSBOL2(unittest.TestCase):
    def setUp(self):
        # Create temp directory
        self.temp_out_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove directory after the test
        shutil.rmtree(self.temp_out_dir)

    def run_round_trip_assert_fail(self, test_file):
        print(str(test_file))
        split_path = os.path.splitext(test_file)
        self.doc = Document()   # Document for read and write
        self.doc.read(os.path.join(TEST_LOC_SBOL2, split_path[0] + split_path[1]))
        self.doc.write(os.path.join(self.temp_out_dir,
                                    split_path[0] + '_out' + split_path[1]))

        self.doc2 = Document()  # Document to compare for equality
        self.doc2.read(os.path.join(self.temp_out_dir,
                                    split_path[0] + '_out' + split_path[1]))
        # Expected to fail
        self.assertRaises(AssertionError, lambda: self.assertEqual(self.doc.compare(self.doc2), 1))


class SimpleTest(unittest.TestCase):
    def test_read(self):
        test_file = str(TEST_FILES_SBOL2[0])
        print(str(test_file))
        split_path = os.path.splitext(test_file)
        self.doc = Document()   # Document for read and write
        self.doc.read(os.path.join(TEST_LOC_SBOL2, split_path[0] + split_path[1]))


def runTests(test_list):
    if test_list is None or test_list == []:
        return
    suite_list = []
    loader = unittest.TestLoader()
    for test_class in test_list:
        suite = loader.loadTestsFromTestCase(test_class)
        suite_list.append(suite)

    full_test_suite = unittest.TestSuite(suite_list)

    unittest.TextTestRunner(verbosity=2, stream=sys.stderr).run(full_test_suite)


def runRoundTripTests():
    runTests([TestRoundTripSBOL2, TestRoundTripFailSBOL2])


if __name__ == '__main__':
    print(sys.path)
    runRoundTripTests()
