import json

def convert_json(obj):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr)
                else:
                    #print(v)
                    v = "{0}".format(v).replace("\"","\"\"").replace('\n'," ").replace('\t'," ").replace('\r'," ")
                    #print(v)
                    str = "out_TransactionItem.SpecificContent("+ f"\"{k}\") = \"{v}\""
                    arr.append(str)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr)
        return arr

    results = extract(obj, arr)
    return results
