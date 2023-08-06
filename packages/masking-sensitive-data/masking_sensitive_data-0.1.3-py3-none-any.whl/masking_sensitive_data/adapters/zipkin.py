import json
from contextlib import suppress

from ipapp.logger.adapters.zipkin import ZipkinAdapter as ZipkinAdapter_
from ipapp.logger.span import Span

from ..config import MaskConfig, MaskZipkinConfig
from ..logic.masking import MaskData


class MaskZipkinAdapter(ZipkinAdapter_):
    mask_cfg: MaskConfig

    def __init__(self, cfg: MaskZipkinConfig, mask_cfg: MaskConfig):
        super().__init__(cfg)
        self.cfg = cfg
        self.mask_cfg = mask_cfg
        self.logic: MaskData = MaskData()

    def handle(self, span: Span) -> None:

        if not self.cfg.masking_sensitive_data or not self.mask_cfg.rule:
            return super().handle(span)

        try:
            mask_rule = json.loads(self.mask_cfg.rule)
        except json.JSONDecodeError:
            return super().handle(span)

        if not mask_rule:
            return super().handle(span)

        mask_ann_names = self.logic.mask_ann_names

        for key_ann in mask_ann_names:
            ann_d = None
            if not span.annotations.get(key_ann):
                continue
            annotate = span.annotations[key_ann]
            _ann4adap, _timestamp = annotate[0]
            with suppress(TypeError, json.JSONDecodeError):
                ann_d = json.loads(_ann4adap)
                if ann_d is not None:
                    ann_d = self.logic.mask_value_of_tag(ann_d, mask_rule)
            if ann_d:
                mask_annotate = json.dumps(ann_d)
                new_annotate = [(mask_annotate, _timestamp)]
                span._annotations4adapter[self.name][key_ann] = new_annotate

        super().handle(span)
