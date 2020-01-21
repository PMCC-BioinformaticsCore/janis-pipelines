# pylint: disable=import-error
from wgs_germline.wgsgermline import WGSGermlineMultiCallers
from wgs_germline_gatk.wgsgermlinegatk import WGSGermlineGATK
from wgs_somatic.wgssomatic import WGSSomaticMultiCallers
from wgs_somatic_gatk.wgssomaticgatk import WGSSomaticGATK

workflows = [
    WGSGermlineMultiCallers,
    WGSGermlineGATK,
    WGSSomaticMultiCallers,
    WGSSomaticGATK,
]


def export_workflows(wfs=workflows):
    import inspect, os.path

    for W in workflows:
        w = W()
        args = {
            "to_console": False,
            "to_disk": True,
            "validate": True,
            "export_path": os.path.join(
                os.path.dirname(os.path.realpath(inspect.getfile(W))), "{language}"
            ),
        }
        w.translate("cwl", **args)
        w.translate("wdl", **args)


if __name__ == "__main__":
    __name__ = None
    export_workflows()
