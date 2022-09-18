from simulator import build_fraction_list, transform_input_correlations


def test_build_correlation_list_1():
    assert build_fraction_list([20, 40]) == [.2, .4]

def test_build_correlation_list_with_zero():
    assert build_fraction_list([20, 40, 0]) == [.2, .4, 0]

def test_input_correlations():
    assert transform_input_correlations("10,20") == [10, 20]
    assert transform_input_correlations("10,50") == [10, 50]