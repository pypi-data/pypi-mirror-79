import os
from dataclasses import field

from ask_smapi_model.v1.skill.manifest import SkillManifest
from pydantic import BaseModel, validator, constr
from typing import List, Dict, Optional


class InoftVocalEnginePublishingInfos(BaseModel):
    class AlexaSpecificModel(BaseModel):
        class LocalizedTabDataModel(BaseModel):
            alexaSkillName: Optional[str]
            alexaSkillDescription: Optional[str] = ""
            alexaSkillSummary: Optional[str] = ""
            alexaTermsOfUseUrl: Optional[str] = ""
            alexaPrivacyPolicyUrl: Optional[str] = ""
            alexaSkillExamplePhrases: Optional[List[str]] = list()
            alexaSkillKeywords: Optional[List[str]] = list()

            @validator("alexaSkillName")
            def check_length_of_name(cls, value):
                if value is not None and isinstance(value, str) and len(value) > 1:
                    return value
                return "Temporary name"

        selectedCountriesCode: List[str]
        selectedSkillCategory: Optional[str] = ""
        testInstructionsForAmazon: Optional[str] = ""
        localizedTabsExportedData: Dict[str, LocalizedTabDataModel]

        @validator("selectedSkillCategory")
        def check_if_skill_category_valid(cls, value):
            if value is None or value == "":
                return value

            from inoft_vocal_engine.utils.paths import get_inoft_vocal_engine_root_path
            skill_categories_json_filepath = os.path.join(get_inoft_vocal_engine_root_path(), "web_interface/static/deployment/alexaSkillCategories.json")

            from inoft_vocal_engine.utils.general import load_json
            valid_categories = load_json(filepath=skill_categories_json_filepath)

            if value in valid_categories:
                return value
            else:
                raise ValueError(f"The category with the key {value} was not found in the valid categories json file : {valid_categories}")

    alexaSpecific: AlexaSpecificModel

    def to_alexa_manifest(self) -> SkillManifest:
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
                locales={},
                distribution_countries=self.alexaSpecific.selectedCountriesCode,
                is_available_worldwide=False,
                testing_instructions=self.alexaSpecific.testInstructionsForAmazon,
                category=self.alexaSpecific.selectedSkillCategory
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

        for localLanguageKeyName, localInfosData in self.alexaSpecific.localizedTabsExportedData.items():
            from ask_smapi_model.v1.skill.manifest import SkillManifestLocalizedPublishingInformation
            alexa_manifest.publishing_information.locales[localLanguageKeyName] = (
                SkillManifestLocalizedPublishingInformation(
                    name=localInfosData.alexaSkillName,
                    description=localInfosData.alexaSkillDescription,
                    summary=localInfosData.alexaSkillSummary,
                    example_phrases=localInfosData.alexaSkillExamplePhrases,
                    keywords=localInfosData.alexaSkillKeywords
                )
            )

            from ask_smapi_model.v1.skill.manifest import SkillManifestLocalizedPrivacyAndCompliance
            alexa_manifest.privacy_and_compliance.locales[localLanguageKeyName] = (
                SkillManifestLocalizedPrivacyAndCompliance(
                    privacy_policy_url=localInfosData.alexaPrivacyPolicyUrl,
                    terms_of_use_url=localInfosData.alexaTermsOfUseUrl
                )
            )
            # todo: check if the urls are valid http or https url, otherwise
            #  there will be an internal client error when sending the data
        # serialized_manifest = nested_serialize(alexa_manifest)
        return alexa_manifest
