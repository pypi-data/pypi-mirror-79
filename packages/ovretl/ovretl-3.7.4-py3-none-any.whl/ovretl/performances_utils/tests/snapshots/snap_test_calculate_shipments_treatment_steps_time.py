# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots["test_calculate_shipments_treatment_steps_time 1"] = GenericRepr(
    "header  shipment_id  ... billing_available_paid_days\n0            6049.0  ...                        None\n1            6238.0  ...                        None\n2            6392.0  ...                        None\n3            7082.0  ...                        None\n4            7255.0  ...                        None\n..              ...  ...                         ...\n190          9647.0  ...                        None\n191          9649.0  ...                        None\n192          9650.0  ...                        None\n193          9651.0  ...                        None\n194          9652.0  ...                        None\n\n[195 rows x 19 columns]"
)
