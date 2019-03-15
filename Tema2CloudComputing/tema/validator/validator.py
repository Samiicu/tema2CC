from cerberus import *

schema_meniu = {'id_sub-meniu': {'type': 'integer'}, "continut": {'type': ['string', 'list']},
                "cantitate": {'type': 'string'}, "denumire": {'type': 'string'}, "pret": {'type': 'string'},
                "id": {'type': 'integer'}}
v = Validator(schema_meniu)
document = {
    "id_sub-meniu": 1,
    "continut": "espresso",
    "cantitate": "30 ml",
    "denumire": "espresso",
    "pret": "5 ron"
}
print v.validate(document)