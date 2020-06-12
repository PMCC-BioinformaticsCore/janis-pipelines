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
    import inspect, os.path, shutil

    for W in workflows:
        w = W()

        outputdir = os.path.dirname(os.path.realpath(inspect.getfile(W)))
        dirs_to_remove = ["cwl", "wdl"]
        for od in dirs_to_remove:
            odd = os.path.join(outputdir, od)
            if os.path.exists(odd):
                shutil.rmtree(odd)

        args = {
            "to_console": False,
            "to_disk": True,
            "validate": True,
            "export_path": os.path.join(outputdir, "{language}"),
        }
        w.translate("cwl", **args)
        w.translate("wdl", **args)


if __name__ == "__main__":
    __name__ = None
    export_workflows()
