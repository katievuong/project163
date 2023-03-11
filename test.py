'''
Tyrell Garza, Kevin Fu, Katie Vuong
Data Breach Analysis: Investigating Trends and Impact on Businesses
Testing file imports cleanup.py and cse163_utils.py
for validating accuracy in results and calculations
drawing from test.py's smaller data
'''
import cleanup
import pandas as pd
from cse163_utils import assert_equals


# research question 1 tests
def test_filter_by_year(data: pd.DataFrame) -> None:
    '''

    Tests filter_by_year, returns dataframe with 7 rows,
    year ranges from 2009 to 2017.
    '''
    filtered_data = cleanup.filter_by_year(data, 2009, 2017)
    assert_equals(7, len(filtered_data))
    assert_equals(2009, filtered_data['year'].min())
    assert_equals(2014, filtered_data['year'].max())


def test_breach_trend(data: pd.DataFrame) -> None:
    '''

    Tests that breach trend is increasing by using
    count_breach_by_year to check number of breaches
    in latest year (2013) > breaches in earliest year
    (2009).
    '''
    earliest, latest = cleanup.count_breaches_by_year(data)
    assert latest > earliest
    assert earliest == 1
    assert latest == 2


# research question 3 tests
def test_average_response(data: pd.DataFrame) -> None:
    '''
    Tests cleanup.py's clean_dates function, ensures correct
    time passed between two dates calculations, returns None
    '''
    end1 = cleanup.clean_dates(data).loc[4, "Date_Posted_or_Updated"].split('/'
                                                                            )
    start1 = cleanup.clean_dates(data).loc[4, "breach_start"].split('/')
    months1 = int(end1[1]) - int(start1[1])
    days1 = (int(end1[2]) - int(start1[2])) / (365.25 / 12)
    test1 = (months1 + days1)
    assert_equals(test1, cleanup.clean_dates(data).loc[4, 'response_time'])
    assert_equals(51 + (11/(365.25 / 12)),
                  cleanup.clean_dates(data).loc[0, 'response_time'])
    assert_equals(
        19/(365.25 / 12), cleanup.clean_dates(data).loc[5, 'response_time'])


# research question 4 tests
def test_unique_loc(data: pd.DataFrame) -> None:
    '''
    Tests cleanup.py's clean_entities function, ensures correct
    amount of unique locations, returns None
    '''
    assert_equals(6, len(cleanup.clean_entities(data)))
    assert_equals(1, cleanup.clean_entities(data)['E-mail'])
    assert_equals(9, sum(cleanup.clean_entities(data).values()))


# research question 5 tests
def test_split_by_comma(data: pd.DataFrame) -> None:
    '''

    Tests the split_by_comma function. Returns a
    dataframe with 7 rows, where 'Type of Breach'
    column contains correct values after splitting
    by comma.
    '''
    exploded_data = cleanup.split_by_comma(data, 'Type_of_Breach')
    assert_equals(7, len(exploded_data))
    assert_equals('Theft', exploded_data.iloc[1]['Type_of_Breach'])
    assert_equals('Theft', exploded_data.iloc[2]['Type_of_Breach'])


def test_total_individuals_affected(data: pd.DataFrame) -> None:
    '''

    Tests total_individuals_affected method by proving
    what visual showed (Theft affects most indivduals).
    This method compares 'Theft' to other breach methods.
    '''
    total_affected = cleanup.total_individuals_affected(data)
    assert total_affected['Theft'] > total_affected['Other']


def test_total_records_by_breach_type(data: pd.DataFrame) -> None:
    '''
    Tests total_records_by_breach_type method by proving that 'HACK'
    has the most amount of records. This method compares 'HACK'
    to other breach types.
    '''
    total_records = cleanup.total_records_by_breach_type(data)
    # test 1
    assert total_records[
        'HACK'
    ] > total_records['DISC']
    # test 2
    assert total_records[
        'HACK'
    ] > total_records['PORT']


def main():
    test_data = pd.read_csv("test.csv")
    prc_data = pd.read_csv("PRC Data Breach Chronology - 1.13.20.csv")
    test_unique_loc(test_data)
    test_average_response(test_data)
    test_filter_by_year(test_data)
    test_split_by_comma(test_data)
    test_total_individuals_affected(test_data)
    test_breach_trend(test_data)
    test_total_records_by_breach_type(prc_data)


if __name__ == '__main__':
    main()
