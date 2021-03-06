use_fwlite = False
eosprefix = "root://eoscms.cern.ch/"
#root://cms-xrd-global.cern.ch/

def fedMap():
    d = {"HBHE": range(700, 718),
         "HF": range(718, 724),
         "HO": range(724, 732),
         "uHBHE": range(1100, 1118, 2),
         "uHF": [1118, 1120, 1122],
         "uC": [1132],
         }

    d["HBHEHF"] = d["HBHE"] + d["HF"]
    d["HBEF"] = d["HBHEHF"]
    d["HCAL"] = d["HBEF"] + d["HO"]

    d["uHBHEHF"] = d["uHBHE"] + d["uHF"]
    d["uHBEF"] = d["uHBHEHF"]
    d["uHBECF"] = d["uHBEF"] + d["uC"]
    d["uHCAL"] = d["uHBECF"] + d["HO"]

    return d


def fedList(s=""):
    d = fedMap()
    if not s:
        return []
    if s in d:
        return d[s]

    out = [int(x) for x in s.split(",")]
    return out


def format(treeName=""):
    def __isVme(fedId=None):
        return 700 <= fedId <= 731


    dct = {"CMSRAW": {"branch": lambda fedId: "%s%d" % ("HCAL_DCC" if __isVme(fedId) else "Chunk", fedId)}}

    if use_fwlite:
        dct["Events"] = {"rawCollection": "FEDRawDataCollection_rawDataCollector__LHC", "product": True}
    else:
        dct["Events"] = {"rawCollection": "FEDRawDataCollection_rawDataCollector__LHC.obj", "product": False}

    for item in ["LuminosityBlocks", "MetaData", "ParameterSets", "Parentage", "Runs"]:
        dct[item] = None

    out = dct.get(treeName, {"branch": lambda fedId: "%d" % fedId, "skipWords64": [0, 1]})

    if out:
        if treeName == "deadbeef":
            out["nBytesPer"] = 4
            out["skipWords64"] = [0]

        if "nBytesPer" not in out:
            out["nBytesPer"] = 8

        if "skipWords64" not in out:
            out["skipWords64"] = []

    return out
