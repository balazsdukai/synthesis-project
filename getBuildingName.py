def getBuildingName(string):
    """
    Subsets building name from the 'maploc' field.
    :param string: the value of the 'maploc' field of a single record in the database
    :return: str - the buildingid of the respective building, parsed to be compliant with createBuildingset()
    """
    campus = 'System Campus > '
    to_replace = ["-", " ", "(", ")", "&"]

    i = string.find(campus)
    if i >= 0:
        string = string.replace(campus, '')
        e = string.find(' > ')
        string = string[:e]
    else:
        pass
    res = ''.join([i for i in string if not i.isdigit()])
    for ch in to_replace:
        if ch in res:
            res = res.replace(ch, "_")
            if "___" in res:
                res = res.replace("___", "_")
    if res[0] == "_":
        building = res[1:].lower()
        return building
    else:
        building = res.lower()
        return building

# Example
s0 = 'System Campus > 21-BTUD > 1e verdieping'
s1 = 'Root Area'
getBuildingName(s0)
getBuildingName(s1)

