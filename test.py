import project
import pandas as pd


def test_unique_breaches(data: pd.DataFrame) -> list[str]:
    print(project.prc_unique_breaches(data))


def test_vin_unique_breaches(data: pd.DataFrame) -> list[str]:
    print(project.vin_unique_breaches(data))


def main():
    priv_rights_data = pd.read_csv("PRC Data Breach Chronology - 1.13.20.csv")
    vincent_data = pd.read_csv("breaches.csv")

    test_unique_breaches(priv_rights_data)
    test_vin_unique_breaches(vincent_data)


if __name__ == '__main__':
    main()
