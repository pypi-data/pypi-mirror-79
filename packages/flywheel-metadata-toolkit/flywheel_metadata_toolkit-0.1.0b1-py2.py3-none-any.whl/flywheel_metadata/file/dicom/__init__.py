"""Dicom metadata module"""

import pydicom
from flywheel_metadata.file.dicom.fixer import fw_pydicom_config


@fw_pydicom_config()
def load_pydicom_dataset(*args, **kwargs):
    """
    Load a dicom dataset with Flywheel-recommended pydicom configuration
    settings.

    Args:
        *args: pydicom.dcmread args
        **kwargs: pydicom.dcmread kwargs

    Returns:
        pydicom.Dataset
    """
    dcm = pydicom.dcmread(*args, **kwargs)
    dcm.decode()  # decoding here to use fw_pydicom_config
    return dcm
