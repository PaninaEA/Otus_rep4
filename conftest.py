def pytest_addoption(parser):
    parser.addoption("--url", type=str, default="https://ya.ru", help="Url for check")

    parser.addoption(
        "--status_code",
        type=int,
        default="200",
        help="Response status code",
    )
