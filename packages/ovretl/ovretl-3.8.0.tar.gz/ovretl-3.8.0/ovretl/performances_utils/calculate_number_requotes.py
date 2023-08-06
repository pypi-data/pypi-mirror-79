import pandas as pd

KRONOS_ID = 125


def calculate_number_requotes(activities_df: pd.DataFrame, shipments_df: pd.DataFrame):
    activities_purchase_ready_df = activities_df[
        (activities_df["header"] == "quotation_purchase_ready") & (activities_df["employee_id"] != KRONOS_ID)
    ]
    activities_purchase_ready_df = activities_purchase_ready_df.groupby("shipment_id").size()
    return pd.merge(
        left=shipments_df,
        right=activities_purchase_ready_df.to_frame(name="nb_requotes"),
        left_on="shipment_id",
        right_index=True,
        how="left",
    )
