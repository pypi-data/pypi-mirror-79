t = 1
# #Extracts command from the commit message
# def extract_command(commit):
#     start = '{'
#     end = '}'
#     try:
#         result = re.findall(re.escape(start)+"(?<=\{)\s*[^{]*?(?=[\},])"+re.escape(end),commit)[0]
#     except:
#         result = 'If you were trying to bump the version number, the current format of your instruction is Not Supported.'
#     finally:
#         return result

# #Converts a string to a dictionary
# def convert_to_dict(string):
#     try:
#         dicT = json.loads(string)
#     except:
#         dicT = 'Format not supported'
#     finally:
#         return dicT

# #Converts a dictionary to a string
# def convert_to_JSON(string):
#     try:
#         obj = json.dumps(string)
#     except:
#         obj = 'Format not supported'
#     finally:
#         return obj



# #Executes a command
# def execute_command(version, branch):
#     if (version == "major" or version == "minor" or version == "build" or version == "patch"):
#         command1 = "echo Changing '{version}' version".format(version = version)
#         command2 = "python3 /opt/egov-nexus-deployer/change-version.py -t '{version}' -a npm".format(version = version)
#         command3 = "python3 /opt/egov-nexus-deployer/push-changes.py -m '{version}' -b '{branch}'".format(version = version, branch=branch)

#         return results
#     else:
#         result = "Failed: Invalid version type specified.\n Please specify: 'major','minor', 'build' or 'patch'."
#         return result
