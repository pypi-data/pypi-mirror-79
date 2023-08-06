import json
from contextlib import suppress

from ipapp.logger.adapters.requests import RequestsAdapter as RequestsAdapter_
from ipapp.logger.span import Span

from ..config import MaskConfig, MaskRequestsConfig
from ..logic.masking import MaskData


class MaskRequestsAdapter(RequestsAdapter_):
    mask_cfg: MaskConfig

    def __init__(self, cfg: MaskRequestsConfig, mask_cfg: MaskConfig):
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

        req_ann = {self.name: {}}
        for key_ann in mask_ann_names:
            ann_d = None
            if not span.annotations.get(key_ann):
                continue
            annotate = span.annotations[key_ann]
            _annotate, _ts = annotate[0]
            with suppress(TypeError, json.JSONDecodeError):
                ann_d = json.loads(_annotate)
                if ann_d is not None:
                    ann_d = self.logic.mask_value_of_tag(ann_d, mask_rule)
            if ann_d:
                mask_annotate = json.dumps(ann_d)
                req_ann[self.name].update({key_ann: [(mask_annotate, _ts)]})
        span._annotations4adapter.update(req_ann)

        super().handle(span)
