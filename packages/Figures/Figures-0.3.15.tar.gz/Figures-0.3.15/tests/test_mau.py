
from datetime import datetime
from freezegun import freeze_time
from dateutil.relativedelta import relativedelta
import pytest

from django.utils.timezone import utc

from courseware.models import StudentModule

from figures.sites import (
    get_student_modules_for_site,
    get_student_modules_for_course_in_site,
)
from figures.mau import (
    get_mau_from_student_modules,
    get_mau_from_site_course,
    mau_1g_for_month_as_of_day,
    site_mau_1g_for_month_as_of_day,
    store_mau_metrics,
)

from tests.factories import StudentModuleFactory
from tests.helpers import OPENEDX_RELEASE, GINKGO


def test_get_mau_from_site_course(sm_test_data):
    """Basic test for coverage with simple check
    TODO: Improve by adding more students to the StudentModule instances for
    the first course constructed in the `sm_test_data` fixture data set.
    """
    year_for = sm_test_data['year_for']
    month_for = sm_test_data['month_for']
    site = sm_test_data['site']

    # Get first course, check student modules for that
    course_overview = sm_test_data['course_overviews'][0]
    users = get_mau_from_site_course(site=site,
                                     course_id=str(course_overview.id),
                                     year=year_for,
                                     month=month_for)
    course_sm = StudentModule.objects.filter(course_id=course_overview.id)
    sm_check = course_sm.values_list('student__id', flat=True).distinct()
    assert set(users) == set(sm_check)


def test_get_mau_from_sm_for_site(sm_test_data):
    year_for = sm_test_data['year_for']
    month_for = sm_test_data['month_for']
    sm = get_student_modules_for_site(sm_test_data['site'])
    users = get_mau_from_student_modules(student_modules=sm,
                                         year=year_for,
                                         month=month_for)

    sm_check = sm.values_list('student__id', flat=True).distinct()
    assert set(users) == set(sm_check)


@pytest.mark.skipif(OPENEDX_RELEASE == GINKGO,
                    reason='Broken test. Apparent Django 1.8 incompatibility')
@pytest.mark.django_db
def test_mau_1g_for_month_as_of_day_first_day_next_month(db):
    """
    Test getting live MAU 1G values from StudentModule for the given day

    Quick-n-dirty data setup:

    We want to make sure we get the right records when the query happens on the
    first day of the next month. So we do the following

    * Add a StudentModule record for two months before
    * Add at least one StudentModule record for the month we want
    * Add at least one StudentModule record for after the month we want

    This sets up the scenario that we run the daily pipeline to capture MAU
    "as of" yesterday (the last day of the previous month) to capture MAU for
    the previous month
    """
    mock_today = datetime(year=2020, month=4, day=1).replace(tzinfo=utc)
    month_before = datetime(year=2020, month=2, day=2).replace(tzinfo=utc)
    in_dates = [datetime(year=2020, month=3, day=1).replace(tzinfo=utc),
                datetime(year=2020, month=3, day=15).replace(tzinfo=utc),
                datetime(year=2020, month=3, day=31).replace(tzinfo=utc)]
    date_for = mock_today.date() - relativedelta(days=1)

    # Create a student module in the month before, and in month after
    StudentModuleFactory(created=month_before, modified=month_before)
    StudentModuleFactory(created=mock_today, modified=mock_today)
    sm_in = [StudentModuleFactory(created=rec,
                                  modified=rec) for rec in in_dates]
    expected_user_ids = [obj.student_id for obj in sm_in]

    sm_queryset = StudentModule.objects.all()
    user_ids = mau_1g_for_month_as_of_day(sm_queryset=sm_queryset,
                                          date_for=date_for)
    assert set([rec['student__id'] for rec in user_ids]) == set(expected_user_ids)


def test_site_mau_1g_for_month_as_of_day(monkeypatch):
    """Test our wrapper function, site_mau_1g_for_month_as_of_day

    All we really care about is the call stack is what we expect with the args
    we expect
    """
    expected_site = 'this is our site'
    expected_date_for = 'this is my date'
    expected_sm_queryset = 'this is my expected student module queryset'
    expected_user_id_qs = 'this is my expected user id queryset'

    def mock_get_student_modules_for_site(site):
        assert site == expected_site
        return expected_sm_queryset

    def mock_mau_1g_for_month_as_of_day(sm_queryset, date_for):
        assert date_for == expected_date_for
        assert sm_queryset == expected_sm_queryset
        return expected_user_id_qs

    monkeypatch.setattr('figures.mau.mau_1g_for_month_as_of_day',
                        mock_mau_1g_for_month_as_of_day)
    monkeypatch.setattr('figures.mau.get_student_modules_for_site',
                        mock_get_student_modules_for_site)

    qs = site_mau_1g_for_month_as_of_day(site=expected_site,
                                         date_for=expected_date_for)
    assert qs == expected_user_id_qs


def test_store_mau_metrics(monkeypatch, sm_test_data):
    """
    Basic minimal test
    """
    mock_today = datetime(year=sm_test_data['year_for'],
                          month=sm_test_data['month_for'],
                          day=1)
    freezer = freeze_time(mock_today)
    freezer.start()
    site = sm_test_data['site']
    data = store_mau_metrics(site=site)
    freezer.stop()

    site_mau = data['smo'].mau
    assert site_mau == len(sm_test_data['student_modules'])
    assert data['smo'].year == mock_today.year
    assert data['smo'].month == mock_today.month
    assert len(data['cmos']) == len(sm_test_data['course_overviews'])
    for cmo in data['cmos']:
        assert cmo.year == mock_today.year
        assert cmo.month == mock_today.month
        expected_course_sm = get_student_modules_for_course_in_site(site=site,
                                                                    course_id=cmo.course_id)
        expected_mau = get_mau_from_student_modules(student_modules=expected_course_sm,
                                                    year=mock_today.year,
                                                    month=mock_today.month)
        # TODO: Fix, rudimentary check, improve
        assert expected_mau
