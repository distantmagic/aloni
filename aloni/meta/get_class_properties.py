from typing import Any, Dict, Type

from .class_property_info import ClassPropertyInfo


def get_class_properties(cls: Type[Any]) -> Dict[str, ClassPropertyInfo]:
    properties: Dict[str, ClassPropertyInfo] = {}
    annotations = cls.__annotations__

    for name, type_ in annotations.items():
        property_info = ClassPropertyInfo(
            default_value=None,
            is_default_provided=False,
            name=name,
            type=type_,
        )

        if name in cls.__dict__:
            property_info.is_default_provided = True
            property_info.default_value = cls.__dict__[name]

        properties[property_info.name] = property_info

    return properties
