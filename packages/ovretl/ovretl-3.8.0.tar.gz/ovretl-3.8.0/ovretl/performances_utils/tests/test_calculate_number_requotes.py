import pandas as pd
from pandas.util.testing import assert_frame_equal

from ovretl.performances_utils.calculate_number_requotes import calculate_number_requotes


def test_calculate_number_requotes():
    activities_df = pd.DataFrame(
        data={
            "shipment_id": [0, 0, 1, 1],
            "employee_id": [0, 1, 2, 3],
            "header": ["quotation_purchase_ready", "quotation_purchase_ready", "quotation_purchase_ready", "bar"],
        }
    )
    shipments_df = pd.DataFrame(data={"shipment_id": [0, 1]})
    result = calculate_number_requotes(activities_df=activities_df, shipments_df=shipments_df)
    result_should_be = pd.DataFrame(data={"shipment_id": [0, 1], "nb_requotes": [2, 1]})
    assert_frame_equal(result, result_should_be)
