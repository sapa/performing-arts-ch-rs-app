import re
from SemanticFieldDefinitionGenerator import generator

inputFile = 'fieldDefinitions.yml'
outputFile = '../data/templates/http%3A%2F%2Fpage-module.performing-arts.ch%2FFieldDefinitions.html'

def addLocalisation(jsonString, bundle):

    def replaceWithLocalised(match):
        key = "field_" + re.sub(r'[\W\s]', '_', match.group(1)).lower()
        return '"label": "[[i18n "' + key + '" bundle="' + bundle + '"]]"'

    pattern = r'"label": "(.*)"'
    return re.sub(pattern, replaceWithLocalised, jsonString)


model = generator.loadSourceFromFile(inputFile)

output = generator.generate(model, generator.INLINE)
output = addLocalisation(output, 'sapa-fields')
# The generator produces a JSON array for the "domain" property, but we need a string. So we replace it with a regex.
output = re.sub(r'"domain"\s*:\s*\[\s*[\'"]([^\'"]+)[\'"]\s*\]', r'"domain" : "\1"', output)
output = re.sub(r'"range"\s*:\s*\[\s*[\'"]([^\'"]+)[\'"]\s*\]',  r'"range" : ["\1"]', output)

with open(outputFile, 'w') as f:
    f.write(output)