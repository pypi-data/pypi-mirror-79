# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The set of helper functions for data frames."""
import numpy as np
import pandas as pd
import scipy

from typing import Optional

from azureml.automl.core.shared import constants
from azureml.automl.core.shared.exceptions import DataFormatException,\
    InvalidDataTypeException
from azureml.automl.runtime.data_transformation import _add_raw_column_names_to_X
from azureml.automl.runtime.shared.types import DataInputType


def _get_df_or_raise(X: DataInputType,
                     x_raw_column_names: Optional[np.ndarray] = None,
                     ignore_errors: bool = False) -> pd.DataFrame:
    """
    Create a pandas DataFrame based on the raw column names or raise an exception if it is not possible.

    :param X: The input data to be converted to a data frame.
    :param x_raw_column_names: The names for columns of X.
    :param ignore_errors: if True, the absent column names will not trigger the exception.
    :raises: InvalidDataTypeException if X is not a data frame and columns are not provided.
    """
    if isinstance(X, pd.DataFrame):
        return X
    if x_raw_column_names is not None:
        # check if there is any conflict in the x_raw_column_names
        if not ignore_errors:
            _check_timeseries_input_column_names(x_raw_column_names)
            # generate dataframe for tsdf.
            return _add_raw_column_names_to_X(x_raw_column_names, X)
        df = pd.DataFrame(X, columns=x_raw_column_names)
    else:
        df = pd.DataFrame(X)
        if not ignore_errors:
            # if x_raw_column_name is None, then the origin input data is ndarray.
            raise InvalidDataTypeException(
                "Timeseries only support pandas DataFrame as input X. The raw input X is {}.".format(
                    "sparse" if scipy.sparse.issparse(X) else "ndarray"
                )).with_generic_msg("Timeseries only support pandas DataFrame as input X.")
    return df


def _check_timeseries_input_column_names(x_raw_column_names: np.ndarray) -> None:
    """
    Check if the column name is not in the reserved column name list.

    :param x_raw_column_names: The list of the columns names.
    :raises: DataFormatException if the column is contained in the reserved column list.
    """
    for col in x_raw_column_names:
        if col in constants.TimeSeriesInternal.RESERVED_COLUMN_NAMES:
            print("Column name {} is in the reserved column names list, please change that column name.".format(col))
            raise DataFormatException(
                "Column name is in the reserved column names list, please change that column name.",
                has_pii=False
            )
