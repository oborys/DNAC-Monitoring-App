# from django.utils import timezone
import datetime

def calc_mttr(all_dates=[]):
    mttri_diffs = [el['date_end'] - el['date'] for el in all_dates]
    mttr_diffs = [el['date_end'] - el['date_start'] for el in all_dates]

    if mttri_diffs and mttr_diffs:
        mttri_diffs_in_seconds = [date.total_seconds() for date in mttri_diffs]
        mttr_diffs_in_seconds = [date.total_seconds() for date in mttr_diffs]

    mttr = datetime.timedelta(seconds=(sum(mttr_diffs_in_seconds) / len(mttr_diffs_in_seconds)))
    mttri = datetime.timedelta(seconds=(sum(mttri_diffs_in_seconds) / len(mttri_diffs_in_seconds)))

    # print(date_diffs_in_seconds, mttr)

    return (mttr, mttri)

def calc_customer_satisfactions():
    pass

def calc_device_availability():
    pass

if __name__ == "__main__":
    calc_mttr()