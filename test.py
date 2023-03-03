import project
import pandas as pd


def test_unique_breaches(data: pd.DataFrame) -> None:
    print(project.unique_breaches(data))


def code():
    priv_rights_data = pd.read_csv("PRC Data Breach Chronology - 1.13.20.csv")
    vincent_data = pd.read_csv("breaches.csv")
    test_unique_breaches(priv_rights_data)


if __name__ == '__main__':
    code()
