# import json
#
# with open('dat3.json') as f:
#     data = json.load(f)
# resurseBlanaoo = data
# for resursa in resurseBlanaoo:
# #     print resursa['sub-meniu']
# import re
#
# pathRoute="1233456s1sad2"
#
# try:
#     print re.match("(\d{7,10})",pathRoute).group(0)
# except:
#     pass
#     # print "match"
#     # print "Done"
import json

def do_update(data_to_commit,file):
    with open(file,'w') as f:
        f.write(json.dumps(data_to_commit))
# data_json = data
# print data_json
