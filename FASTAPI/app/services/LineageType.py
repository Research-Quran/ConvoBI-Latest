from enum import Enum
# from enum import StrEnum


class LineageType(Enum):
    TOP_TO_BOTTOM_FULL_LINEAGE='1'
    TOP_TO_BOTTOM_FILTER='2'
    TOP_TO_BOTTOM_HOLDING='3'
    TOP_TO_BOTTOM_STITCH_EXCEPTION='4'
    TOP_TO_BOTTOM_ORPHAN='5'
    BOTTOM_TO_TOP_FULL_LINEAGE='6'
    
    def get_lineage_type(type):
        try:
            return LineageType(type).name
        except Exception as ex:
            raise ex