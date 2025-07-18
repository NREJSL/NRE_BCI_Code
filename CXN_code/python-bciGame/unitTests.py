import statistics
import math
from MVC.resultsModel import GameStats
from MVC.PlayerScore import GameResults
from solvers.Solvers import StatsSolvers
import unittest

class SolverTests(unittest.TestCase):   
    
    def test_get_min_selection_time_returns_expected(self):
 
        testcase_0 = SelectionTimeTestCase(selectionTimes=[1.0,2.0,3.0,4.0,5.0,6.0], expected_min=1)
        testcase_1 = SelectionTimeTestCase(selectionTimes=[6.0,5.0,4.0,3.0,2.0,1.0], expected_min=1)
        testcase_2 = SelectionTimeTestCase(selectionTimes=[6.0,2.0,1.0,3.0,5.0,1.0], expected_min=1)
        testcase_3 = SelectionTimeTestCase(selectionTimes=[1], expected_min=1)
        testcase_4 = SelectionTimeTestCase(selectionTimes=[], expected_min=-1)
        testcase_5 = SelectionTimeTestCase(selectionTimes=None, expected_min=-1)
        testcase_6 = SelectionTimeTestCase(selectionTimes="test", expected_min=-2)
        
        tests = [testcase_0, 
                 testcase_1,
                 testcase_2,
                 testcase_3,
                 testcase_4,
                 testcase_5,
                 testcase_6]
        
        i=-1
        for case in tests:
            i += 1 
            with self.subTest(i=i):
                solver = StatsSolvers()
                actual = solver.get_min_selection_time(case.selection_times)
                self.assertEqual(actual, case.expected_min)
         
    def test_get_max_selection_time_returns_expected(self):
 
        testcase_0 = SelectionTimeTestCase(selectionTimes=[1,2,3,4,5,6], expected_max=6)
        testcase_1 = SelectionTimeTestCase(selectionTimes=[6,5,4,3,2,1], expected_max=6)
        testcase_2 = SelectionTimeTestCase(selectionTimes=[6,2,1,3,5,1], expected_max=6)
        testcase_3 = SelectionTimeTestCase(selectionTimes=[1], expected_max=1)
        testcase_4 = SelectionTimeTestCase(selectionTimes=[], expected_max=-1)
        testcase_5 = SelectionTimeTestCase(selectionTimes=None, expected_max=-1)
        testcase_6 = SelectionTimeTestCase(selectionTimes="test", expected_max=-2)
        
        tests = [testcase_0, 
                 testcase_1,
                 testcase_2,
                 testcase_3,
                 testcase_4,
                 testcase_5,
                 testcase_6]
        
        i=-1
        for case in tests:
            i += 1 
            with self.subTest(i=i):
                solver = StatsSolvers()
                actual = solver.get_max_selection_time(case.selection_times)
                self.assertEqual(actual, case.expected_max)
    
    def test_get_avg_selection_time_returns_expected(self):
 
        testcase_0 = SelectionTimeTestCase(selectionTimes=[1,2,3,4,5,6], expected_avg=3.5)
        testcase_1 = SelectionTimeTestCase(selectionTimes=[6,5,4,3,2,1], expected_avg=3.5)
        testcase_2 = SelectionTimeTestCase(selectionTimes=[6,2,1,3,5,1], expected_avg=3)
        testcase_3 = SelectionTimeTestCase(selectionTimes=[1], expected_avg=1)
        testcase_4 = SelectionTimeTestCase(selectionTimes=[], expected_avg=-1)
        testcase_5 = SelectionTimeTestCase(selectionTimes=None, expected_avg=-1)
        testcase_6 = SelectionTimeTestCase(selectionTimes="test", expected_avg=-2)
        
        tests = [testcase_0, 
                 testcase_1,
                 testcase_2,
                 testcase_3,
                 testcase_4,
                 testcase_5,
                 testcase_6]
        
        i=-1
        for case in tests:
            i += 1 
            with self.subTest(i=i):
                solver = StatsSolvers()
                actual = solver.get_average_selection_time(case.selection_times)
                self.assertEqual(actual, case.expected_avg)
    
    def test_get_percent_correct_returns_expected(self):
     
        testcase_0 = PercentCorrectTestCase(0, 1, 0)
        testcase_1 = PercentCorrectTestCase(10,10,100)
        testcase_2 = PercentCorrectTestCase(33,100, 33)
        testcase_3 = PercentCorrectTestCase(0,0,-1)
        testcase_4 = PercentCorrectTestCase(1.0,4.0,-2)
        
        tests = [testcase_0, 
                 testcase_1,
                 testcase_2,
                 testcase_3,
                 testcase_4]
        
        i=-1
        for case in tests:
            i += 1 
            with self.subTest(i=i):
                solver = StatsSolvers()
                actual = solver.get_percent_correct(
                    successes=case.correct_count,
                    attempts=case.attempts)
                self.assertEqual(actual, case.expected)
    
    def test_get_duration_test(self):
        testcase_0 = SelectionTimeTestCase(selectionTimes=[1,2,3,4,5,6], expected_duration=21)
        testcase_1 = SelectionTimeTestCase(selectionTimes=[6,5,4,3,2,1], expected_duration=21)
        testcase_2 = SelectionTimeTestCase(selectionTimes=[6,2,1,3,5,1], expected_duration=18)
        testcase_3 = SelectionTimeTestCase(selectionTimes=[1], expected_duration=1)
        testcase_4 = SelectionTimeTestCase(selectionTimes=[], expected_duration=-1)
        testcase_5 = SelectionTimeTestCase(selectionTimes=None, expected_duration=-1)
        testcase_6 = SelectionTimeTestCase(selectionTimes="test", expected_duration=-2)
        testcase_7 = SelectionTimeTestCase(selectionTimes=[1.1,2.2,3.3,4.4,5.5,6.6,7.7], expected_duration=30.8)
        
        tests = [testcase_0, 
                 testcase_1,
                 testcase_2,
                 testcase_3,
                 testcase_4,
                 testcase_5,
                 testcase_6,
                 testcase_7]
        
        i=-1
        for case in tests:
            i += 1 
            with self.subTest(i=i):
                solver = StatsSolvers()
                actual = solver._get_duration(case.selection_times)
                self.assertEqual(actual, case.expected_duration)
    
    def test_calculate_itr(self):
        
        hundred_seconds = 100000.0/ 1000.0
        tests = [
            #4 target test case
            ITRTestCase(
                num_choices=4,
                successful_selections=4,
                total_attempted_classifications=5,
                trial_duration_seconds=hundred_seconds,           
                expected=2.88,
            ),
            # just above accuracy
            ITRTestCase(
                num_choices=4,
                successful_selections=3,
                total_attempted_classifications=10,
                trial_duration_seconds=hundred_seconds,
                expected=0.06
            ),
            # below accuracy
            ITRTestCase(
                num_choices=4,
                successful_selections=2,
                total_attempted_classifications=10,
                trial_duration_seconds=hundred_seconds,
                expected=0.06,
                expected_warning=StatsSolvers.BELOW_CHANCE_WARNING
            ),
            # all incorrect
            ITRTestCase(
                successful_selections=0,
                trial_duration_seconds=hundred_seconds,
                num_choices=4,
                total_attempted_classifications=15,
                expected=0.00,
                expected_warning=StatsSolvers.BELOW_CHANCE_WARNING
            ),
            #below accuracy
            ITRTestCase(
                successful_selections=10,
                trial_duration_seconds=hundred_seconds,
                num_choices=4,
                total_attempted_classifications=50,
                expected=0.3,
                expected_warning=StatsSolvers.BELOW_CHANCE_WARNING
            ),
            #perfect 50
            ITRTestCase(
                successful_selections=50,
                num_choices=4,
                total_attempted_classifications=50,
                trial_duration_seconds=hundred_seconds,
                expected=60
            ),
            # 8 target test cases
            #perfect 10
            ITRTestCase(
                num_choices=8,
                successful_selections=10,
                total_attempted_classifications=10,
                trial_duration_seconds=hundred_seconds,
                expected=18
            ),
            #just above chance threshold 
            ITRTestCase(
                num_choices=8,
                successful_selections=2,
                total_attempted_classifications=10,
                trial_duration_seconds=hundred_seconds,
                expected=0.19
            ),
            #just below 
            ITRTestCase(
                num_choices=8,
                successful_selections=1,
                total_attempted_classifications=10,
                trial_duration_seconds=hundred_seconds,
                expected=0.03,
                expected_warning=StatsSolvers.BELOW_CHANCE_WARNING
            ),
            #completely wrong
            ITRTestCase(
                num_choices=8,
                successful_selections=0,
                total_attempted_classifications=10,
                trial_duration_seconds=hundred_seconds,
                expected=0.00,
                expected_warning=StatsSolvers.BELOW_CHANCE_WARNING
            ),
            
            #12 targets
            
            #perfect 10
            ITRTestCase(
                num_choices=12,
                successful_selections=10,
                total_attempted_classifications=10,
                trial_duration_seconds=hundred_seconds,
                expected=21.51
            ),
            #just above chance threshold 
            ITRTestCase(
                num_choices=12,
                successful_selections=2,
                total_attempted_classifications=20,
                trial_duration_seconds=hundred_seconds,
                expected=0.03
            ),
            #just below 
            ITRTestCase(
                num_choices=12,
                successful_selections=1,
                total_attempted_classifications=20,
                trial_duration_seconds=hundred_seconds,
                expected=0.15,
                expected_warning=StatsSolvers.BELOW_CHANCE_WARNING
            ),
            #completely wrong
            ITRTestCase(
                num_choices=12,
                successful_selections=0,
                total_attempted_classifications=20,
                trial_duration_seconds=hundred_seconds,
                expected=0.00,
                expected_warning=StatsSolvers.BELOW_CHANCE_WARNING
            ),
            
        ]
        
        i=-1
        for case in tests:
            i += 1 
            with self.subTest(i=i):
                solver = StatsSolvers()
                actual = solver.calculate_itr_bci(
                    successful_selections=case.successful_selections,
                    num_choices=case.num_choices,
                    total_attempted_classifications=case.total_attempted_classifications,
                    trial_duration_seconds=case.trial_duration_seconds ,
                    log=False
                )
                itr = actual[0]
                warning = actual[1]
                self.assertEqual(itr, case.expected_itr)
                self.assertEqual(warning, case.expected_warning)
    
    
class SelectionTimeTestCase():
    selection_times:list[float]
    expected_min:float
    expected_avg:float
    expected_max:float
    expected_duration:float
    
    def __init__(self, selectionTimes:list[float],
                 expected_min:float = -1, 
                 expected_avg:float = -1,
                 expected_max:float = -1,
                 expected_duration:float = -1):
        self.expected_avg = expected_avg
        self.expected_duration = expected_duration
        self.expected_max = expected_max
        self.expected_min = expected_min
        self.selection_times = selectionTimes
        
class PercentCorrectTestCase():
    expected:float
    correct_count:int
    attempts:int    
    def __init__(self, correct_count:int, attempts:int, expected:float):
        self.correct_count = correct_count
        self.attempts = attempts
        self.expected =expected
      
class ITRTestCase():
    successful_selections:int
    expected_itr:float
    expected_warning:str
    num_choices:int
    total_attempted_classifications:int
    trial_duration_seconds:float
    
    def __init__(self,
        successful_selections:int,
        expected:float,
        num_choices:int,
        total_attempted_classifications:int,
        trial_duration_seconds:float,
        expected_warning:str = ""):
    
        self.expected_itr = expected
        self.num_choices = num_choices
        self.total_attempted_classifications = total_attempted_classifications
        self.successful_selections = successful_selections
        self.trial_duration_seconds = trial_duration_seconds
        self.expected_warning = expected_warning
            

  
if __name__ == '__main__':       
    unittest.main()