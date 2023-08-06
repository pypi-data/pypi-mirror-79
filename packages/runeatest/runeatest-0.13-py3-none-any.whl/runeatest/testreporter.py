def addtestcase(name, issuccess):
    return {"test": name, "issuccess": str(issuccess), "result": (getresult(issuccess))}


def getresult(issuccess):
    if issuccess:
        return str("success")
    else:
        return str("failure")
