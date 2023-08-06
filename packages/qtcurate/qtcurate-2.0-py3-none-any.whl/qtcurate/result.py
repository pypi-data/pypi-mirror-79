from __future__ import annotations
import json
import os
from typing import List
from qtcurate.exceptions import QtArgumentError, QtFileTypeError
from qtcurate.qt import Qt
from qtcurate.utilities import connect


category = "category"
vocab_name = "dict_name"
vocab_id = "dict_id"
type_field = "type"
str_field = "str"
double_value = "doubleValue"
int_value = "intValue"
datetime_value = "datetimeValue"


class FieldValue:
    def __init__(self):
        self.str_value = None
        self.double_value = None
        self.int_value = None
        self.datetime_value = None

    def __repr__(self):
        return f"{self.double_value}, {self.str_value}"

    def set_str(self, str_val: str) -> FieldValue:
        self.str_value = str_val
        return self

    def get_str(self) -> str:
        return self.str_value

    def set_double_value(self, double: float) -> FieldValue:
        self.double_value = double
        return self

    def get_double_value(self) -> float:
        return self.double_value

    def set_int_value(self, int_val: int) -> FieldValue:
        self.int_value = int_val
        return self

    def get_int_value(self) -> int:
        return self.int_value

    def set_datetime_value(self, date_time: str) -> FieldValue:
        self.datetime_value = date_time
        return self

    def get_datetime_value(self) -> str:
        return self.datetime_value


class Field:

    def __init__(self):
        self.vocab_name = None
        self.vocab_id = None
        self.category = None
        self.type = None
        self.str = None
        self.values = None

    def __repr__(self):
        return f"{self.vocab_id}, {self.str}"

    def set_values(self, val : List) -> None:
        self.values = val

    def get_values(self) -> List:
        return self.values

    def set_str(self, str_value: str) -> Field:
        self.str = str_value
        return self

    def set_type(self, type_value: str) -> Field:
        self.type = type_value
        return self

    def set_vocab_name(self, name: str) -> Field:
        self.vocab_name = name
        return self

    def set_category(self, cat: str) -> Field:
        self.category = cat
        return self



    def set_vocab_id(self, voc_id: str) -> Field:
        self.vocab_id = voc_id
        return self

    def get_vocab_id(self) -> str:
        return self.vocab_id

    def get_vocab_name(self) -> str:
        return self.vocab_name

    def get_category(self) -> str:
        return self.category

    def get_str(self) -> str:
        return self.str

    def get_type(self) -> str:
        return self.type


class Result:

    def __init__(self, dp_id):
        self.id = dp_id
        self.headers = {"X-API-Key": Qt.api_key}
        self.url = Qt.url

    def raw_exporter(self, path: str) -> None:
        """Exporting in JSON format"""

        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".json":
            raise QtFileTypeError("File type error: Please use json extension saving file")
        res = connect("get", f"{self.url}reports/{self.id}/json", self.headers)
        with open(path, "w") as json_file:
            json.dump(res.json(), json_file)

    def result_xlsx_exporter(self, path: str) -> None:
        """Exporting in Excel format"""

        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".xlsx":
            raise QtFileTypeError("File type error: Please use xlsx extension saving file")
        res = connect("get", f"{self.url}reports/{self.id}/xlsx", self.headers)

        with open(path, 'wb') as excel_file:
            excel_file.write(res.content)

    def read(self) -> List:
        """Convert to Object namedtuple"""
        result_list = []
        res = connect("get", f"{self.url}reports/{self.id}/json", self.headers)
        for item in res.json():
            if "values" in item:
                for i in item["values"]:
                    field = Field()
                    if str_field in i:
                        field.set_str(i[str_field])
                    if type_field in i:
                        field.set_type(i[type_field])
                    if category in i:
                        field.set_category(i[category])
                    if vocab_name in i:
                        field.set_vocab_name(i[vocab_name])
                    if vocab_id in i:
                        field.set_vocab_id(i[vocab_id])
                    if "extIntervalSimples" in i:
                        list_field_ext = []
                        for ext_int_item in i["extIntervalSimples"]:
                            field_value = FieldValue()
                            if str_field in ext_int_item:
                                field_value.set_str(ext_int_item[str_field])
                            if int_value in ext_int_item:
                                field_value.set_int_value(ext_int_item[int_value])
                            if datetime_value in ext_int_item:
                                field_value.set_datetime_value(ext_int_item[datetime_value])
                            if double_value in ext_int_item:
                                field_value.set_double_value(ext_int_item[double_value])
                            list_field_ext.append(field_value)
                    field.set_values(list_field_ext)
                    result_list.append(field)
        return result_list

