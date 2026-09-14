import re
import glob
import json
from SemanticFieldDefinitionGenerator import generator

pathFolderFiles = './fieldDefinitions'
#inputFile = 'fieldDefinitions.yml'
outputFile = '../data/templates/http%3A%2F%2Fpage-module.performing-arts.ch%2FFieldDefinitions.html'

"""
    Function custom for generate the model fieldDefinition
    input: FieldDefinition Directory 
    output: model of json file data
        EX: 
            {
                'fields' : [
                    { id: RDFType .........},
                    { id: PerformancePlan .........},
                    { id: PerformanceSerie .........},
                    .
                    .
                    .
                ]
            }

"""
def generateModelFromFiles(pathFolderFiles:str):

    # ********************************************************************
    # Read all fieldDefinitions files to fieldDefinition folder
    # Production, Performance, Non-Performatice Expression, etc
    # ********************************************************************
    pathFiles = glob.glob(f"{pathFolderFiles}/*.yml",recursive=True) 
    # Generate the model 
    model_generator = [generator.loadSourceFromFile(inputFile) for inputFile in pathFiles]
    #
    fieldDefinitions_config = list() 
    # Get all values
    [fieldDefinitions_config.extend(fd.get('fields')) for fd in model_generator ]
    # Create a json file output
    output_field = dict()
    output_field["fields"] = fieldDefinitions_config
    return output_field

def addLocalisation(jsonString, bundle):

    def replaceWithLocalised(match):
        key = "field_" + re.sub(r'[\W\s]', '_', match.group(1)).lower()
        return '"label": "[[i18n "' + key + '" bundle="' + bundle + '"]]"'

    pattern = r'"label": "(.*)"'
    return re.sub(pattern, replaceWithLocalised, jsonString)

model = generateModelFromFiles(pathFolderFiles)

# ********************************************************************
# Get the model for one file definition
# ********************************************************************
#model = generator.loadSourceFromFile(inputFile)

output = generator.generate(model, generator.INLINE)
output = addLocalisation(output, 'sapa-fields')
# The generator produces a JSON array for the "domain" property, but we need a string. So we replace it with a regex.
output = re.sub(r'"domain"\s*:\s*\[\s*[\'"]([^\'"]+)[\'"]\s*\]', r'"domain" : "\1"', output)
output = re.sub(r'"range"\s*:\s*\[\s*[\'"]([^\'"]+)[\'"]\s*\]',  r'"range" : ["\1"]', output)

with open(outputFile, 'w') as f:
    f.write(output)