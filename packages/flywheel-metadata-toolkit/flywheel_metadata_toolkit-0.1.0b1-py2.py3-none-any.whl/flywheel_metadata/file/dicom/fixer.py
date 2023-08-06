"""Fixer callbacks for pydicom"""
from contextlib import contextmanager
from copy import copy

import pydicom
from pydicom import config as pydicom_config
from pydicom.datadict import get_entry
from pydicom.multival import MultiValue
from pydicom.util.fixer import fix_mismatch_callback


def backslash_in_VM1_string_callback(raw_elem):
    """A callback function to fix the value of RawDataElement with VM=1 and VR of type
    string that contains the an invalid ``\`` character (``\`` is the array delimiter in
    Dicom standard)
    """
    try:
        # Only fixing VM for tag supported by get_entry
        vr, vm, _, _, _ = get_entry(raw_elem.tag)
        # only fix if VR matches
        if vr == raw_elem.VR and vm == "1":
            # only fix if is a VR string
            if vr not in [
                "UT",
                "ST",
                "LT",
                "FL",
                "FD",
                "AT",
                "OB",
                "OW",
                "OF",
                "SL",
                "SQ",
                "SS",
                "UL",
                "OB/OW",
                "OW/OB",
                "OB or OW",
                "OW or OB",
                "UN",
                "US",
            ]:
                value = pydicom.values.convert_value(raw_elem.VR, raw_elem)
                if isinstance(value, MultiValue) and len(value) > 1:
                    # replace \\ byte with /
                    raw_elem = raw_elem._replace(
                        value=raw_elem.value.decode().replace("\\", "/").encode()
                    )
    except KeyError:
        pass
    return raw_elem


def converter_exception_callback(raw_elem, **kwargs):
    """A callback function to catch NotImplementedError when raw_elem contains an
    invalid VR"""
    try:
        raw_elem = fix_mismatch_callback(raw_elem, **kwargs)
    except NotImplementedError:
        # Handle invalid VR for which a converters are not defined
        if raw_elem.tag in [0xFFFEE0DD]:
            # 0xFFFEE0DD is a sequence delimiter with VR='NONE' in pydicom,
            # To handle the edge case where an extra sequence delimiter is
            # found in the DataSet setting its VR to OB to avoid conversion (setting
            # it to UN or None will raise because VR inference will happen downstream).
            raw_elem = raw_elem._replace(VR="OB")
        else:
            # Replacing the VR by None to treat tag as if it was implicit. Downstream
            # pydicom will apply its logic to infer the VR.
            raw_elem = raw_elem._replace(VR=None)

    return raw_elem


def data_element_callback(raw_elem, **kwargs):
    raw_elem = converter_exception_callback(raw_elem, **kwargs)
    # currently not applying multiple fixes
    # (e.g. unknown VR and backslash in VM1 string)
    raw_elem = backslash_in_VM1_string_callback(raw_elem)
    if "callback" in kwargs:
        callback = kwargs.get("callback")
        callback(raw_elem)
    return raw_elem


@contextmanager
def fw_pydicom_config(with_VRs=["PN", "DS", "IS"]):
    """A callback contextmanager to fix:

    1) RawDataElements elements with invalid VR.
    2) RawDataElements elements that are not translatable with their provided VRs.
    3) RawDataElements string elements containing ``\\``.

    Args:
        with_VRs : list, [['PN', 'DS', 'IS']]
            A list of VR strings to attempt if the raw data element value cannot
            be translated with the raw data element's VR.

    Returns
    -------
    No return value.  The callback function will return either
    the original RawDataElement instance, or one with a fixed VR or value.
    """
    data_element_callback_bk = copy(pydicom_config.data_element_callback)
    data_element_callback_kwargs_bk = copy(pydicom_config.data_element_callback_kwargs)
    pydicom_config.data_element_callback = data_element_callback
    pydicom_config.data_element_callback_kwargs = {
        "with_VRs": with_VRs,
    }
    yield
    pydicom_config.data_element_callback = data_element_callback_bk
    pydicom_config.data_element_callback_kwargs = data_element_callback_kwargs_bk
