from behave_pytest.hook import install_pytest_asserts


def before_all(context):
    install_pytest_asserts()
