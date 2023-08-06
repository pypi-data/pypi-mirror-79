import enum

from ask_smapi_model.v1.skill.manifest import DistributionCountries
from pydantic import BaseModel
from typing import List, Optional

from pydantic.dataclasses import dataclass


class LanguageModel(BaseModel):
    language_code: str
    country_code: DistributionCountries
    name: str

class LocalInfos(BaseModel):
    language: LanguageModel
    skill_name: str
    skill_description: Optional[str] = " "
    skill_summary: Optional[str] = " "
    example_phrases: Optional[List[str]] = list()
    keywords: Optional[List[str]] = list()
    termsOfUseUrl: Optional[str] = " "
    privacyPolicyUrl: Optional[str] = " "


class AlexaLanguage(enum.Enum):
    french_france: LanguageModel = LanguageModel(language_code="fr-FR", country_code=DistributionCountries.FR, name="French France")

"""
alexa_language_codes = [
    LanguageModel(language_code="de-DE", name="Deustch"),
    LanguageModel(language_code="en-AU", name="Australian"),
    LanguageModel(language_code="en-CA", name="Canadian"),
    LanguageModel(language_code="en-GB", name="German"),
    LanguageModel(language_code="en-IN", name="Deustch"),
    LanguageModel(language_code="en-US", name="Deustch"),
    LanguageModel(language_code="es-ES", name="Espagnol Espagne"),
    LanguageModel(language_code="es-MX", name="Deustch"),
    LanguageModel(language_code="es-US", name="Deustch"),
    LanguageModel(language_code="fr-CA", name="French Canadian"),
    LanguageModel(language_code="fr-FR", name="French France"),
    LanguageModel(language_code="hi-IN", name="Hindou India"),
    LanguageModel(language_code="it-IT", name="Deustch"),
    LanguageModel(language_code="ja-JP", name="Deustch"),
    LanguageModel(language_code="pt-BR", name="Deustch")
]
"""

def try_to_convert_to_dict(object_instance: any, return_none_on_failure: bool) -> dict or any:
    if hasattr(object_instance, "to_dict"):
        return object_instance.to_dict()
    elif hasattr(object_instance, "__dict__"):
        return object_instance.__dict__
    else:
        if return_none_on_failure is False:
            return object_instance
        else:
            return None

def nested_serialize(object_instance: any):
    if isinstance(object_instance, list):
        for i in range(len(object_instance)):
            object_instance[i] = nested_serialize(object_instance=object_instance[i])
        return object_instance
    elif isinstance(object_instance, dict):
        for key, item in object_instance.items():
            object_instance[key] = nested_serialize(object_instance=item)
        return object_instance
    else:
        object_data_dict: Optional[dict] = try_to_convert_to_dict(
            object_instance=object_instance, return_none_on_failure=True
        )

        if object_data_dict is not None:
            output_data_dict = object_data_dict.copy()
            attribute_map: Optional[dict] = getattr(object_instance, "attribute_map", None)

            for key, item in object_data_dict.items():
                print(f"{key} {item}")
                if attribute_map is not None:
                    attribute_map_key = attribute_map.get(key, None)
                    if attribute_map_key is not None and key != attribute_map_key:
                        output_data_dict[attribute_map_key] = try_to_convert_to_dict(
                            object_instance=nested_serialize(object_instance.__dict__[key]),
                            return_none_on_failure=False
                        )
                        output_data_dict.pop(key)
                        continue

                current_item_to_serialize = object_instance.__dict__.get(key, None)
                if current_item_to_serialize is None:
                    # In some rare cases, like with an Enum class, trying to access the data with the __dict__ super
                    # function will change the keys of the variable, and we need to access the data via the object_data_dict.
                    current_item_to_serialize = object_data_dict.get(key, None)
                if current_item_to_serialize is not None:
                    output_data_dict[key] = try_to_convert_to_dict(
                        object_instance=nested_serialize(current_item_to_serialize),
                        return_none_on_failure=False
                    )
            return output_data_dict
        else:
            return object_instance



class ProjectDeploymentInfo(BaseModel):
    class AlexaModel(BaseModel):
        invocationName: str
        testingInstructionsText: str
        category: str
        localInfos: List[LocalInfos]
    alexa: AlexaModel

    def to_alexa_manifest(self):
        from ask_smapi_model.v1.skill.manifest import SkillManifest
        from ask_smapi_model.v1.isp import PublishingInformation
        from ask_smapi_model.v1.isp import PrivacyAndCompliance
        from ask_smapi_model.v1.skill.manifest import SkillManifestEvents
        from ask_smapi_model.v1.skill.manifest import PermissionItems
        from ask_smapi_model.v1.skill.manifest import SkillManifestApis
        from ask_smapi_model.v1.skill.alexa_hosted import HostingConfiguration
        from ask_smapi_model.v1.skill.manifest import DistributionCountries
        from ask_smapi_model.v1.skill.manifest import CustomApis
        from ask_smapi_model.v1.skill.manifest import SkillManifestEndpoint

        from ask_smapi_model.v1.skill.manifest import SkillManifestPublishingInformation
        from ask_smapi_model.v1.skill.manifest import SkillManifestLocalizedPublishingInformation
        from ask_smapi_model.v1.skill.manifest import SkillManifestPrivacyAndCompliance
        alexa_manifest = SkillManifest(
            manifest_version="1.0",
            publishing_information=SkillManifestPublishingInformation(
                locales={}, distribution_countries=[],
                is_available_worldwide=False,
                testing_instructions="1) Say 'Alexa, discover my devices' 2)",
                category="SMART_HOME"
            ),
            privacy_and_compliance=SkillManifestPrivacyAndCompliance(
                locales={},
                allows_purchases=False,
                is_export_compliant=True,
                is_child_directed=False,
                uses_personal_info=False
            ),
            apis={
                "custom": {
                    "endpoint": {
                        "uri": "arn:aws:lambda:us-east-1:032174894474:function:ask-custom-custome_cert"
                    }
                }
            }
            # events=SkillManifestEvents(),
            # permissions=[PermissionItems()],
            # apis=SkillManifestApis(
            #    custom=CustomApis(
            #        endpoint=SkillManifestEndpoint(
            #            uri="arn:aws:lambda:eu-west-3:631258222318:function:testlambdacoolose"
            #        )
            #    )
            # )
        )

        for local in self.alexa.localInfos:
            local: LocalInfos
            if local.language.country_code not in alexa_manifest.publishing_information.distribution_countries:
                alexa_manifest.publishing_information.distribution_countries.append(local.language.country_code.value)

            from ask_smapi_model.v1.skill.manifest import SkillManifestLocalizedPublishingInformation
            alexa_manifest.publishing_information.locales[local.language.language_code] = (
                SkillManifestLocalizedPublishingInformation(
                    name=local.skill_name,
                    description=local.skill_description,
                    summary=local.skill_summary,
                    example_phrases=local.example_phrases,
                    keywords=local.keywords
                )
            )

            from ask_smapi_model.v1.skill.manifest import SkillManifestLocalizedPrivacyAndCompliance
            alexa_manifest.privacy_and_compliance.locales[local.language.language_code] = (
                SkillManifestLocalizedPrivacyAndCompliance(
                    privacy_policy_url=local.privacyPolicyUrl,
                    terms_of_use_url=local.termsOfUseUrl
                )
            )
            # todo: check if the urls are valid http or https url, otherwise
            #  there will be an internal client error when sending the data
        # serialized_manifest = nested_serialize(alexa_manifest)
        return alexa_manifest
