import re
from contextlib import suppress

from ipapp.db.pg import PgSpan
from ipapp.http._base import HttpSpan
from ipapp.mq.pika import AmqpSpan


class MaskData:

    mask_ann_names = [
        HttpSpan.ANN_REQUEST_BODY,
        HttpSpan.ANN_RESPONSE_BODY,
        AmqpSpan.ANN_IN_BODY,
        AmqpSpan.ANN_OUT_BODY,
        PgSpan.ANN_PARAMS,
        PgSpan.ANN_RESULT,
    ]

    def mask_value_of_tag(self, annotation_dict: dict, mask_rule: dict) -> dict:
        for key, value in annotation_dict.items():
            changing_value = annotation_dict.get(key)
            if isinstance(changing_value, int):
                changing_value = str(changing_value)
            with suppress(KeyError):
                mask_regex = mask_rule[key]
                annotation_dict[key] = re.sub(
                    mask_regex[0], mask_regex[1], changing_value,
                )
        for nested in annotation_dict.values():
            if isinstance(nested, dict):
                self.mask_value_of_tag(nested, mask_rule)
        return annotation_dict
