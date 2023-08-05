__all__ = ["DefaultImageInfoParser", "FasterRCNNParser", "MaskRCNNParser"]

from mantisshrimp.imports import *
from mantisshrimp.parsers.parser import *
from mantisshrimp.parsers.mixins import *


class DefaultImageInfoParser(
    Parser, FilepathMixin, SizeMixin, ABC,
):
    pass


class FasterRCNNParser(Parser, LabelsMixin, BBoxesMixin, ABC):
    pass


class MaskRCNNParser(FasterRCNNParser, MasksMixin, IsCrowdsMixin, ABC):
    pass
