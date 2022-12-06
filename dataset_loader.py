import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import isoparse
import itertools
from label import Label
from ast import literal_eval

def load_dataset():
    df_issues = pd.read_csv("issues.csv")
    df_issues = df_issues.drop_duplicates("id")

    # calculate time-to-complete
    df_issues["closed_at"] = df_issues["closed_at"].apply(isoparse)
    df_issues["created_at"] = df_issues["created_at"].apply(isoparse)
    df_issues["time_to_complete"] = (df_issues["closed_at"] - df_issues["created_at"])
    df_issues["time_to_complete"] = df_issues["time_to_complete"].apply(timedelta.total_seconds)
    # remove outliers
    parsed_labels = [literal_eval(label_list) for idx, label_list in df_issues["labels"].items()] #parse labels
    flattened_labels = [Label(**item) for item in itertools.chain.from_iterable(parsed_labels)] # flatten and convert to Label
    label_set = set(flattened_labels)
    df_issues_no_outliers = df_issues
    mean = df_issues["time_to_complete"].mean()
    std = df_issues["time_to_complete"].std()
    std_times_three = std * 3
    low_cut, hi_cut = mean - std_times_three, mean + std_times_three
    df_issues_no_outliers = df_issues.loc[(low_cut < df_issues["time_to_complete"]) & (df_issues["time_to_complete"] < hi_cut)]
    # Convert labels to binary number
    label_set = set(sorted(label_set, key=lambda label: label.name))
    def convert_label_to_number(label: str):
        bit_flags = 0
        for i, l in enumerate(label_set):
            if l.node_id in label:
                value_to_add = 1 << i # bit shift to the position of the label
                bit_flags += value_to_add
        return bit_flags
    df_issues_no_outliers["label_crunched"] = df_issues_no_outliers["labels"].apply(convert_label_to_number)
    # revert times
    df_issues_no_outliers["closed_at"] = df_issues["closed_at"].apply(datetime.timestamp)
    df_issues_no_outliers["created_at"] = df_issues["created_at"].apply(datetime.timestamp)
    return df_issues_no_outliers

if __name__ == "__main__":
    load_dataset()