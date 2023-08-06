from ask_smapi_model.v1.skill import SkillSummary
from ask_smapi_model.v1.skill.manifest import SkillManifest
from ask_smapi_sdk import StandardSmapiClientBuilder
from typing import List
from ask_smapi_model.v1.vendor_management import Vendors, Vendor
from inoft_vocal_engine.STATIC_DATA import StaticData



class SmapiBaseClient:
    def __init__(self, refresh_token: str):
        self._client_id = StaticData().ALEXA_INOFT_VOCAL_ENGINE_APPLICATION_CLIENT_ID
        self._client_secret = StaticData().ALEXA_INOFT_VOCAL_ENGINE_APPLICATION_CLIENT_SECRET

        self.smapi_client_builder = StandardSmapiClientBuilder(
            client_id=self._client_id,
            client_secret=self._client_secret,
            refresh_token=refresh_token
        )
        self.smapi_client = self.smapi_client_builder.client()

    def get_vendors_of_account(self) -> List[Vendor]:
        output_vendors: List[Vendor] = list()
        vendors_response: Vendors = self.smapi_client.get_vendor_list_v1()
        if vendors_response is not None:
            for vendor in vendors_response.vendors:
                output_vendors.append(vendor)
        return output_vendors

    def get_list_skills_of_account(self) -> List[SkillSummary]:
        from ask_smapi_model.v1.skill import ListSkillResponse
        output_skills: List[SkillSummary] = list()

        vendors = self.get_vendors_of_account()
        if len(vendors) > 0:
            response: ListSkillResponse = self.smapi_client.list_skills_for_vendor_v1(vendor_id=vendors[0].id)
            output_skills.extend(response.skills)

        return output_skills

    def create_skill_legacy(self, vendor_id: str):
        from inoft_vocal_engine.models.projects.project_deployment_infos import ProjectDeploymentInfo
        from inoft_vocal_engine.models.projects.project_deployment_infos import LocalInfos
        from inoft_vocal_engine.models.projects.project_deployment_infos import AlexaLanguage

        alexa_manifest = ProjectDeploymentInfo(alexa=ProjectDeploymentInfo.AlexaModel(
            invocationName="Le test",
            testingInstructionsText="Do nothing",
            category="SMART_HOME",
            localInfos=[
                LocalInfos(
                    language=AlexaLanguage.french_france.value,
                    skill_name="Le super test de ouf",
                    skill_description="Rien",
                    skill_summary="Rien",
                    example_phrases=["Hey", "Hoy"],
                    keywords=["One", "Two"],
                    termsOfUseUrl="http://www.termsofuse.sampleskill.com",
                    privacyPolicyUrl="http://www.myprivacypolicy.sampleskill.com"
                )
            ]
        )).to_alexa_manifest()

        alexa_manifest = {
          'manifestVersion': '1.0',
          'publishingInformation': {
            'locales': {
              'de-DE': {
                'name': "Th",
                'summary': '',
                'description': '',
                'examplePhrases': [],
                'keywords': []
              },
              'fr-FR': {
                'name': 'aeea',
                'summary': '',
                'description': 'aeaeea',
                'examplePhrases': [],
                'keywords': []
              }
            },
            'isAvailableWorldwide': False,
            'testingInstructions': 'aeeaeeaea',
            'category': 'ALARMS_AND_CLOCKS',
            'distributionCountries': []
          },
          'privacyAndCompliance': {
            'locales': {
              'de-DE': {
                'privacyPolicyUrl': '',
                'termsOfUseUrl': ''
              },
              'fr-FR': {
                'privacyPolicyUrl': 'http://www.termsofuse.sampleskill.com',
                'termsOfUseUrl': 'http://www.myprivacypolicy.sampleskill.com'
              }
            },
            'allowsPurchases': False,
            'usesPersonalInfo': False,
            'isChildDirected': False,
            'isExportCompliant': True
          },
          'apis': {
            'custom': {
              'endpoint': {
                'uri': 'arn:aws:lambda:us-east-1:032174894474:function:ask-custom-custome_cert'
              }
            }
          }
        }

        from ask_smapi_model.v1.skill import CreateSkillRequest
        self.smapi_client.create_skill_for_vendor_v1(create_skill_request=CreateSkillRequest(
            vendor_id=vendor_id, manifest=alexa_manifest))
        """"{
                  'apis': {
                    'custom': {
                      'endpoint': {
                        'uri': 'arn:aws:lambda:us-east-1:032174894474:function:ask-custom-custome_cert'
                      }
                    }
                  },
                  'manifest_version': '1.0',
                  'privacy_and_compliance': {
                    'locales': {
                    },
                  },
                  'publishing_information': {
                    'category': 'ALARMS_AND_CLOCKS',
                    'description': "eeee",
                    'distribution_countries': [
                      'FR'
                    ],
                    'locales': {

                    },
                    'name': "Le test de l'inoft vocal engine",
                    'testing_instructions': 'Le truc de ouf'
                  }
                }
        ))"""

    def create_skill(self, vendor_id: str, skill_manifest: SkillManifest):
        from ask_smapi_model.v1.skill import CreateSkillRequest
        response = self.smapi_client.create_skill_for_vendor_v1(create_skill_request=CreateSkillRequest(
            vendor_id=vendor_id, manifest=skill_manifest,
        ))
        return response


if __name__ == "__main__":
    refresh_token = "Atzr|IwEBIJPMVNBwbBGY2hum-1Q0ldBPx4wXyFiPr38X9F1Y4FgPYjHvTLK5UlsG5z4kXZlMZHIYGDQLtFFw7saqZ4ZEaRalmjLfdR62uBXe_PupGVrrsX3721TZrSG68Om7VvBCFqJS3BHM_AG5b9VFJkDIkmO5wz45vo9S-6JR1I2KLB12N_vGSKZ5SfIma1PSHjfeAeQgWBQfIa19KE0xBw8t9U0fyGaM-JvwxoLulf1k265hWUDDj3Uuve5CbUlU41NHtFYZXbVrj76vEGIw7-HZBoKU0ZA1-_oscarmnZ5b5ENFFIuKt-bGbQJw5ycgT0Gm0Ja3sxGI7EpakcGBIOECOl0Am4QZBCBRtRENvHVHKtjhT2PeZEZh9Re_DB4nRnnpJOXXXiwajfNdcvtSPHP9nOXtg64iaALnZBeZzzzhcVEXsqQh9TEwO1Y6nOGFMtDm-zOFulGjDwvz_ySLmA5qGbjz9o4p_-A5DEXG2zIgezPT0Z_SyqsiVq7GJ3ixAydyG_4R7nSGEo63_tt34Ffuq4-eSV605Rt7nEHUivm5M9QFOUargug98MlZJala-z_x1u5ETJAZpVhxkXfl4b-XMbqA1YkW2wfO9IkJf_P2UzX2rY1TPz9nGn_DUiVSeGucePo"
    smapi_client = SmapiBaseClient(refresh_token=refresh_token)
    skills_summaries = smapi_client.get_list_skills_of_account()

    smapi_client.create_skill_legacy(vendor_id=smapi_client.get_vendors_of_account()[0].id)
