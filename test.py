'''
Tyrell Garza, Kevin Fu, Katie Vuong
Data Breach Analysis: Investigating Trends and Impact on Businesses

'''
import cleanup
import pandas as pd
from cse163_utils import assert_equals


def test_unique_loc(data: pd.DataFrame) -> None:
    assert_equals(6, len(cleanup.clean_entities(data)))
    assert_equals(1, cleanup.clean_entities(data)['E-mail'])
    assert_equals(9, sum(cleanup.clean_entities(data).values()))


def test_average_response(data: pd.DataFrame) -> None:
    assert_equals(float(16), cleanup.clean_dates(data).loc[1, 'response_time'])


def main():
    test_data = pd.read_csv("test.csv")
    test_unique_loc(test_data)
    test_average_response(test_data)


if __name__ == '__main__':
    main()
