from tsotsa import TSOTSA_ORKG
from orkg import ORKG

ork = ORKG()
print(ork._authenticate(email="jeanpetityvelos@gmail.com", password="2002jeanpetit"))


orkg = TSOTSA_ORKG()

# orkg.create_contribution("R903121", token="og_fcMz__PH-rGZCWJ7FQo0vMBE",
#                          json_template="tsotsa_orkg/data/spec_json_template.json")
print(orkg.create_comparison(token="og_fcMz__PH-rGZCWJ7FQo0vMBE",
                             comparison_file_input='tsotsa_orkg/data/comparison.json'))

# data = {
#   "title" : "test1",
#   "description" : "comparison description",
#   "research_fields" : [ "R141823" ],
#   "authors" : [ {
#     "id": null,
#     "name" : "Jean petit",
#     "identifiers": null,
#     "homepage": null
#   }],
#   "references": [],
#   "contributions" : [ "R837784", "R837785"],

#   "observatories" : [ "eeb1ab0f-0ef5-4bee-aba2-2d5cea2f0174" ],
#   "organizations" : [ "f9965b2a-5222-45e1-8ef8-dbd8ce1f57bc" ],
#   "is_anonymized" : False,
#   "extraction_method" : "UNKNOWN"
# }
