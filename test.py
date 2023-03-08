import cleanup
import pandas as pd
import plots


def test_split_dates(data: pd.DataFrame) -> pd.DataFrame:
    print(cleanup.split_dates(data))


def main():
    vincent_data = pd.read_csv("breaches.csv")
    test_data = pd.read_csv("test.csv")

    # test_split_dates(test_data)
    # print(cleanup.apply_split(test_data))
    # print(cleanup.clean_entities(vincent_data))
    # plots.plot_most_common_entity(vincent_data)
    # print(cleanup.calculate_years(test_data))
    plots.plot_average_response(cleanup.split_dates(vincent_data))


if __name__ == '__main__':
    main()
