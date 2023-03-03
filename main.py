import pandas as pd


def main():
    priv_rights_data = pd.read_csv("PRC Data Breach Chronology - 1.13.20.csv")
    vincent_data = pd.read_csv("breaches.csv")


if __name__ == '__main__':
    main()
