from stochastic_systems_engine.data.yahoo_loader import YahooFinanceLoader


def main() -> None:
    loader = YahooFinanceLoader()

    data = loader.load_history(
        symbol="BRNT.L",
        start="2022-01-01",
        end="2026-03-19",
    )

    print("\nHEAD:\n")
    print(data.head())

    print("\nTAIL:\n")
    print(data.tail())

    print("\nCOLUMNS:\n")
    print(data.columns.tolist())

    print("\nSHAPE:\n")
    print(data.shape)


if __name__ == "__main__":
    main()