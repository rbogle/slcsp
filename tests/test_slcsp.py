import pytest
from slcsp import slcsp


def test_load_datafile():
    filename = "data/plans.csv"
    test_list = slcsp.load_datafile(filename)
    assert isinstance(test_list, list)
    assert len(test_list) == 22241
    assert isinstance(test_list[0], list)


def test_filter_plandata():
    filename = "data/plans.csv"
    test_list = slcsp.load_datafile(filename)
    silverplans = slcsp.filter_plans(test_list)
    assert isinstance(silverplans, dict)
    assert "GA" in silverplans
    assert isinstance(silverplans["GA"], dict)
    assert len(silverplans["GA"].keys()) == 16


def test_filter_zip_map():
    filename = "data/zips.csv"
    test_list = slcsp.load_datafile(filename)
    zip_map = slcsp.filter_zip_map(test_list)
    assert isinstance(zip_map, dict)


# 36855 -- twostates
def test_twostate_lookup_zip():
    filename = "data/zips.csv"
    test_list = slcsp.load_datafile(filename)
    zip_map = slcsp.filter_zip_map(test_list)
    answer = slcsp.lookup_state_area("36855", zip_map)
    assert answer is None


# 36850 -- tworates
def test_tworates_lookup_zip():
    filename = "data/zips.csv"
    test_list = slcsp.load_datafile(filename)
    zip_map = slcsp.filter_zip_map(test_list)
    answer = slcsp.lookup_state_area("36850", zip_map)
    assert answer is None


def test_badzip_lookup_zip():
    filename = "data/zips.csv"
    test_list = slcsp.load_datafile(filename)
    zip_map = slcsp.filter_zip_map(test_list)
    answer = slcsp.lookup_state_area("00000", zip_map)
    assert answer is None


# 36274 -- one rate 13, AL
def test_goodzip_lookup_zip():
    filename = "data/zips.csv"
    test_list = slcsp.load_datafile(filename)
    zip_map = slcsp.filter_zip_map(test_list)
    answer = slcsp.lookup_state_area("36274", zip_map)
    state, area = answer
    assert state == "AL"
    assert area == "13"


def test_lookup_rates():
    filename = "data/plans.csv"
    test_list = slcsp.load_datafile(filename)
    silverplans = slcsp.filter_plans(test_list)
    rates = slcsp.lookup_plan_rates("AL", "13", silverplans)
    assert isinstance(rates, list)
    assert rates[0] <= rates[1]


def test_badstate_lookup_rates():
    filename = "data/plans.csv"
    test_list = slcsp.load_datafile(filename)
    silverplans = slcsp.filter_plans(test_list)
    rates = slcsp.lookup_plan_rates("KY", "8", silverplans)
    assert rates is None


def test_badarea_lookup_rates():
    filename = "data/plans.csv"
    test_list = slcsp.load_datafile(filename)
    silverplans = slcsp.filter_plans(test_list)
    rates = slcsp.lookup_plan_rates("AL", "57", silverplans)
    assert rates is None
