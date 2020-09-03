from .__meta__ import __version__

# from janis_pipelines.alignment.alignment import BwaAlignment

from janis_pipelines.wgs_germline.wgsgermline import (
    WGSGermlineMultiCallers,
    WGSGermlineMultiCallersVariantsOnly,
)
from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk import (
    WGSGermlineGATK,
    WGSGermlineGATKVariantsOnly,
)

from janis_pipelines.wgs_somatic.wgssomatic import (
    WGSSomaticMultiCallers,
    WGSSomaticMultiCallersVariantsOnly,
)
from janis_pipelines.wgs_somatic_gatk.wgssomaticgatk import (
    WGSSomaticGATK,
    WGSSomaticGATKVariantsOnly,
)
