import os
from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Dict
# from typing import TypedDict
from pydantic.class_validators import ROOT_KEY, validator

from inoft_vocal_engine.utils.general import load_json
from inoft_vocal_engine.utils.paths import get_inoft_vocal_engine_root_path


# Init of static variables
# todo: upgrade from Python 3.7 to Python 3.8 and re-use the TypedDict
class AlexaCountryObject:  # (TypedDict):
    name: str
    code: str

alexa_countries: List[AlexaCountryObject] = load_json(os.path.join(get_inoft_vocal_engine_root_path(), "web_interface/static/deployment/alexaCountries.json"))
alexa_countries_keys_codes: List[str] = list()
for country in alexa_countries:
    alexa_countries_keys_codes.append(country["code"])


# todo: upgrade from Python 3.7 to Python 3.8 and re-use the TypedDict
class AlexaLocalObject:  # (TypedDict):
    keyName: str
    code: str

alexa_locales: List[AlexaLocalObject] = load_json(os.path.join(get_inoft_vocal_engine_root_path(), "web_interface/static/deployment/alexaLocales.json"))
alexa_locales_key_codes: List[str] = list()
for local in alexa_locales:
    alexa_locales_key_codes.append(local["code"])


alexa_skill_categories: List[str] = load_json(os.path.join(get_inoft_vocal_engine_root_path(), "web_interface/static/deployment/alexaSkillCategories.json"))


# Utils functions
def raise_if_local_key_invalid(localKeyCode: str):
    if not isinstance(localKeyCode, str):
        raise Exception(f"LocalKeyCode was not of string instance."
                        f"\n  --localKeyCode:{localKeyCode}"
                        f"\n  --type(localKeyCode):{type(localKeyCode)}")
    if localKeyCode not in alexa_locales_key_codes:
        raise Exception(f"LocalKeyCode was an invalid key code."
                        f"\n  --localKeyCode:{localKeyCode}"
                        f"\n  --alexa_locales_key_codes:{alexa_locales_key_codes}")


# Requests data models
class ApplicationManifestGetRequestData(BaseModel):
    typeKeyName: str
    data: dict

class ApplicationManifestUpdateRequestData(BaseModel):
    typeKeyName: str
    data: dict


# Custom validation models
class BaseDataModel(BaseModel):
    def __init__(self, database_path: Dict[str, type], **kwargs):
        super().__init__(**kwargs)
        self.__dict__["database_path"] = database_path
        # We use the __dict__ function to set this attribute, so that
        # pydantic will not attempt to validate the database path.

    def export(self):
        # We need a custom export function, because the pydantic dict() will render us a dict of the object, even if
        # the object has only the __root__ key (in which case, we just want the __root__ as the exported value).
        # And the json() function, which will correctly give us only the __root__ variable, will try to serialize
        # any string, and so, it will try to add junk " or ' to the start and end of the string. Here is our solution.
        data = self.dict(exclude={"database_path"})
        if self.__custom_root_type__:
            data = data[ROOT_KEY]
        return data

class BaseLocalizedDataModel(BaseDataModel):
    def __init__(self, localKeyCode: str, database_path: Dict[str, type], **kwargs):
        super().__init__(database_path=database_path, **kwargs)
        raise_if_local_key_invalid(localKeyCode=localKeyCode)
        # todo: replace raise Exception by a non-crashing validation error


# Fields getters, updaters and senders data models

# Alexa specific diffusion countries models
class AlexaSkillDiffusionCountriesModel(BaseDataModel):
    def __init__(self, **kwargs):
        database_path = {"publishing": dict, "alexa": dict, "diffusionCountries": dict, "selectedCountriesCodes": list}
        super().__init__(database_path=database_path, **kwargs)

class AlexaSkillDiffusionCountriesUpdateModel(AlexaSkillDiffusionCountriesModel):
    __root__: List[str]

    def __init__(self, selectedCountriesCodes: List[str]):
        super().__init__(__root__=selectedCountriesCodes)

    @validator('__root__', each_item=True)
    def check_countries_key_codes(cls, countryKeyCode: str):
        assert countryKeyCode in alexa_countries_keys_codes, (
            f"CountryKeyCode was an invalid key code."
            f"\n  --countryKeyCode:{countryKeyCode}"
            f"\n  --alexa_countries_key_codes:{alexa_countries_keys_codes}")
        return countryKeyCode

class AlexaSkillDiffusionCountriesSenderModel(BaseModel):
    selectedCountriesCodes: List[str]


# Alexa specific test instructions models
class AlexaSkillTestInstructionsModel(BaseDataModel):
    def __init__(self, **kwargs):
        database_path = {"publishing": dict, "alexa": dict, "testInstructions": str}
        super().__init__(database_path=database_path, **kwargs)

class AlexaSkillTestInstructionsUpdateModel(AlexaSkillTestInstructionsModel):
    __root__: str

    def __init__(self, testInstructions: str):
        super().__init__(__root__=testInstructions)

class AlexaSkillTestInstructionsSenderModel(BaseModel):
    testInstructions: str


# Alexa specific test instructions models
class AlexaSkillCategoryModel(BaseDataModel):
    def __init__(self, **kwargs):
        database_path = {"publishing": dict, "alexa": dict, "skillCategory": str}
        super().__init__(database_path=database_path, **kwargs)

class AlexaSkillCategoryUpdateModel(AlexaSkillCategoryModel):
    __root__: str

    def __init__(self, skillCategory: str):
        super().__init__(__root__=skillCategory)

    @validator('__root__')
    def check_skill_category(cls, skillCategory: str):
        assert skillCategory in alexa_skill_categories, (
            f"SkillCategory was an invalidation category."
            f"\n  --skillCategory:{skillCategory}"
            f"\n  --alexa_skill_categories:{alexa_skill_categories}")
        return skillCategory

class AlexaSkillCategorySenderModel(BaseModel):
    skillCategory: str


# Alexa specific localized skill name models
class AlexaSpecificLocalesSkillNameModel(BaseLocalizedDataModel):
    def __init__(self, localKeyCode: str, **kwargs):
        database_path = {"publishing": dict, "alexa": dict, "locales": dict, localKeyCode: dict, "skillName": str}
        super().__init__(localKeyCode=localKeyCode, database_path=database_path, **kwargs)

class AlexaSpecificLocalesSkillNameUpdateModel(AlexaSpecificLocalesSkillNameModel):
    __root__: str

    def __init__(self, localKeyCode: str, skillName: str):
        super().__init__(localKeyCode=localKeyCode, __root__=skillName)

class AlexaSpecificLocalesSkillNameSenderModel(BaseModel):
    skillName: str


# Alexa specific localized skill summary models
class AlexaSpecificLocalesSkillSummaryModel(BaseLocalizedDataModel):
    def __init__(self, localKeyCode: str, **kwargs):
        database_path = {"publishing": dict, "alexa": dict, "locales": dict, localKeyCode: dict, "skillSummary": str}
        super().__init__(localKeyCode=localKeyCode, database_path=database_path, **kwargs)

class AlexaSpecificLocalesSkillSummaryUpdateModel(AlexaSpecificLocalesSkillSummaryModel):
    __root__: str

    def __init__(self, localKeyCode: str, skillSummary: str):
        super().__init__(localKeyCode=localKeyCode, __root__=skillSummary)

class AlexaSpecificLocalesSkillSummarySenderModel(BaseModel):
    skillSummary: str


# Alexa specific localized skill description models
class AlexaSpecificLocalesSkillDescriptionModel(BaseLocalizedDataModel):
    def __init__(self, localKeyCode: str, **kwargs):
        database_path = {"publishing": dict, "alexa": dict, "locales": dict, localKeyCode: dict, "skillDescription": str}
        super().__init__(localKeyCode=localKeyCode, database_path=database_path, **kwargs)

class AlexaSpecificLocalesSkillDescriptionUpdateModel(AlexaSpecificLocalesSkillDescriptionModel):
    __root__: str

    def __init__(self, localKeyCode: str, skillDescription: str):
        super().__init__(localKeyCode=localKeyCode, __root__=skillDescription)

class AlexaSpecificLocalesSkillDescriptionSenderModel(BaseModel):
    skillDescription: str


# Alexa specific localized skill privacy policy models
class AlexaSpecificLocalesPrivacyPolicyModel(BaseLocalizedDataModel):
    def __init__(self, localKeyCode: str, **kwargs):
        database_path = {"publishing": dict, "alexa": dict, "locales": dict, localKeyCode: dict, "skillPrivacyPolicyUrl": str}
        super().__init__(localKeyCode=localKeyCode, database_path=database_path, **kwargs)

class AlexaSpecificLocalesPrivacyPolicyUpdateModel(AlexaSpecificLocalesPrivacyPolicyModel):
    __root__: str

    def __init__(self, localKeyCode: str, skillPrivacyPolicyUrl: str):
        super().__init__(localKeyCode=localKeyCode, __root__=skillPrivacyPolicyUrl)

class AlexaSpecificLocalesPrivacyPolicySenderModel(BaseModel):
    skillPrivacyPolicyUrl: str
    
    
# Alexa specific localized skill terms of use models
class AlexaSpecificLocalesTermsOfUseModel(BaseLocalizedDataModel):
    def __init__(self, localKeyCode: str, **kwargs):
        database_path = {"publishing": dict, "alexa": dict, "locales": dict, localKeyCode: dict, "skillTermsOfUseUrl": str}
        super().__init__(localKeyCode=localKeyCode, database_path=database_path, **kwargs)

class AlexaSpecificLocalesTermsOfUseUpdateModel(AlexaSpecificLocalesTermsOfUseModel):
    __root__: str

    def __init__(self, localKeyCode: str, skillTermsOfUseUrl: str):
        super().__init__(localKeyCode=localKeyCode, __root__=skillTermsOfUseUrl)

class AlexaSpecificLocalesTermsOfUseSenderModel(BaseModel):
    skillTermsOfUseUrl: str


# Switch statements
@dataclass
class SwitchValidatorsWrapper:
    base: any
    update: any
    sender: any

switch_key_type_to_data_models: Dict[str, SwitchValidatorsWrapper] = {
    "AlexaSkillDiffusionCountries": SwitchValidatorsWrapper(
        base=AlexaSkillDiffusionCountriesModel,
        update=AlexaSkillDiffusionCountriesUpdateModel,
        sender=AlexaSkillDiffusionCountriesSenderModel
    ),
    "AlexaSkillTestInstructions": SwitchValidatorsWrapper(
        base=AlexaSkillTestInstructionsModel,
        update=AlexaSkillTestInstructionsUpdateModel,
        sender=AlexaSkillTestInstructionsSenderModel
    ),
    "AlexaSkillCategory": SwitchValidatorsWrapper(
        base=AlexaSkillCategoryModel,
        update=AlexaSkillCategoryUpdateModel,
        sender=AlexaSkillCategorySenderModel
    ),
    "AlexaLocalizedName": SwitchValidatorsWrapper(
        base=AlexaSpecificLocalesSkillNameModel,
        update=AlexaSpecificLocalesSkillNameUpdateModel,
        sender=AlexaSpecificLocalesSkillNameSenderModel
    ),
    "AlexaLocalizedSummary": SwitchValidatorsWrapper(
        base=AlexaSpecificLocalesSkillSummaryModel,
        update=AlexaSpecificLocalesSkillSummaryUpdateModel,
        sender=AlexaSpecificLocalesSkillSummarySenderModel
    ),
    "AlexaLocalizedDescription": SwitchValidatorsWrapper(
        base=AlexaSpecificLocalesSkillDescriptionModel,
        update=AlexaSpecificLocalesSkillDescriptionUpdateModel,
        sender=AlexaSpecificLocalesSkillDescriptionSenderModel
    ),
    "AlexaSkillLocalizedPrivacyPolicy": SwitchValidatorsWrapper(
        base=AlexaSpecificLocalesPrivacyPolicyModel,
        update=AlexaSpecificLocalesPrivacyPolicyUpdateModel,
        sender=AlexaSpecificLocalesPrivacyPolicySenderModel
    ),
    "AlexaSkillLocalizedTermsOfUse": SwitchValidatorsWrapper(
        base=AlexaSpecificLocalesTermsOfUseModel,
        update=AlexaSpecificLocalesTermsOfUseUpdateModel,
        sender=AlexaSpecificLocalesTermsOfUseSenderModel
    ),
}


