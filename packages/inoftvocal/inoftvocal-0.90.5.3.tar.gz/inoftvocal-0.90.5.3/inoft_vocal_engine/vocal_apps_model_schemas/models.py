from enum import Enum

from pydantic import BaseModel
from typing import List, Optional, Any, Dict

from pydantic.dataclasses import dataclass


class AlexaModelConfiguration(BaseModel):
    class FallbackIntentSensitivityModel(BaseModel):
        class LevelOptions(str, Enum):
            HIGH = "HIGH"
            MEDIUM = "MEDIUM"
            LOW = "LOW"
        level: LevelOptions
    fallbackIntentSensitivity: Optional[FallbackIntentSensitivityModel] = None

class AlexaModelSchema(BaseModel):
    class InteractionModelModel(BaseModel):
        class LanguageModelModel(BaseModel):
            invocationName: str
            modelConfiguration: Optional[AlexaModelConfiguration] = None
        languageModel: LanguageModelModel

        class IntentModel(BaseModel):
            class SlotModel(BaseModel):
                name: str
                type: str
                samples: List[str]
            name: str
            samples: List[str]
            slots: List[SlotModel]
        intents: List[IntentModel]

    interactionModel: InteractionModelModel


class InoftVocalEngineModelSchema(BaseModel):
    invocationName: str
    LanguageModel: Optional[str] = None

    class IntentModel(BaseModel):
        class SlotModel(BaseModel):
            name: str
            type: str
            samples: Optional[List[str]] = list()
        intentId: str
        name: str
        samples: Optional[List[str]] = list()
        slots: Optional[List[SlotModel]] = list()
    intents: Optional[Dict[str, IntentModel]] = dict()

    class AlexaSpecific(BaseModel):
        modelConfiguration: Optional[AlexaModelConfiguration] = None
    alexaSpecific: Optional[AlexaSpecific] = None

    class PublishingModel(BaseModel):
        class AlexaModel(BaseModel):
            class LocaleModel(BaseModel):
                skillName: str
            locales: Dict[str, LocaleModel]
        alexa: AlexaModel
    publishing: PublishingModel

class InoftVocalEngineModelSchemaDatabaseComplete(InoftVocalEngineModelSchema):
    accountProjectId: str = None


def inoft_vocal_engine_model_schema_to_alexa_model_schema(inoft_vocal_engine_model_instance: InoftVocalEngineModelSchema) -> AlexaModelSchema:
    intents: List[AlexaModelSchema.InteractionModelModel.IntentModel] = list()
    for src_intent in inoft_vocal_engine_model_instance.intents.values():
        intents.append(AlexaModelSchema.InteractionModelModel.IntentModel(
            name=src_intent.name,
            samples=src_intent.samples,
            slots=src_intent.slots
        ))

    output_alexa_model_schema = AlexaModelSchema(
        interactionModel=AlexaModelSchema.InteractionModelModel(
            languageModel=AlexaModelSchema.InteractionModelModel.LanguageModelModel(
                invocationName=inoft_vocal_engine_model_instance.invocationName,
                modelConfiguration=inoft_vocal_engine_model_instance.alexaSpecific.modelConfiguration
            ), intents=intents
        )
    )
    return output_alexa_model_schema

# todo: save the alexa model schema in json format and store it in S3 ? I have no fucking clue, i'm too tired, i just want to sleep --'


if __name__ == "__main__":
    m = InoftVocalEngineModelSchema(invocationName="test", LanguageModel="test", intents={},
                                    alexaSpecific={"modelConfiguration": {
                                        "fallbackIntentSensitivity": {
                                          "level": "LOW"
                                        }
                                    }})
    print(m)
    print(inoft_vocal_engine_model_schema_to_alexa_model_schema(m))

"""
Alexa :
    {
  "interactionModel": {
    "languageModel": {
      "invocationName": "my space facts",
      "modelConfiguration": {
        "fallbackIntentSensitivity": {
          "level": "LOW"
        }
      },
      "intents": [
        {
          "name": "GetTravelTime",
          "slots": [
            {
              "name": "DepartingPlanet",
              "type": "Planet",
              "samples": [
                "I'm starting from {DepartingPlanet} ",
                "{DepartingPlanet} ",
                "I'm going from {DepartingPlanet} to {ArrivingPlanet} "
              ]
            },
            {
              "name": "ArrivingPlanet",
              "type": "Planet",
              "samples": [
                "I'm going to {ArrivingPlanet} ",
                "{ArrivingPlanet} "
              ]
            }
          ],
          "samples": [
            "calculate travel time",
            "how long does it take to travel from {DepartingPlanet} to {ArrivingPlanet} "
          ]
        }
      ],
      "types": [
        {
          "name": "Planet",
          "values": [
            {
              "name": {
                "value": "Mercury"
              }
            },
            {
              "name": {
                "value": "Venus"
              }
            },
            {
              "name": {
                "value": "Earth"
              }
            },
            {
              "name": {
                "value": "Mars"
              }
            },
            {
              "name": {
                "value": "Jupiter"
              }
            },
            {
              "name": {
                "value": "Saturn"
              }
            },
            {
              "name": {
                "value": "Uranus"
              }
            },
            {
              "name": {
                "value": "Neptune"
              }
            },
            {
              "name": {
                "value": "Pluto"
              }
            }
          ]
        }
      ]
    },
    "dialog": {
      "intents": [
        {
          "name": "GetTravelTime",
          "confirmationRequired": false,
          "prompts": {},
          "slots": [
            {
              "name": "DepartingPlanet",
              "type": "Planet",
              "confirmationRequired": false,
              "elicitationRequired": true,
              "prompts": {
                "elicitation": "Elicit.Intent-GetTravelTime.IntentSlot-DepartingPlanet"
              },
              "validations": [
                {
                  "type": "isNotInSet",
                  "prompt": "Slot.Validation.596358663326.282490667310.1526107495625",
                  "values": [
                    "the sun",
                    "sun",
                    "our sun"
                  ]
                },
                {
                  "type": "hasEntityResolutionMatch",
                  "prompt": "Slot.Validation.596358663326.282490667310.1366622834897"
                }
              ]
            },
            {
              "name": "ArrivingPlanet",
              "type": "Planet",
              "confirmationRequired": false,
              "elicitationRequired": true,
              "prompts": {
                "elicitation": "Elicit.Intent-GetTravelTime.IntentSlot-ArrivingPlanet"
              }
            }
          ]
        }
      ],
      "delegationStrategy": "ALWAYS"
    },
    "prompts": [
      {
        "id": "Elicit.Intent-GetTravelTime.IntentSlot-DepartingPlanet",
        "variations": [
          {
            "type": "PlainText",
            "value": "Which planet do you want to start from?"
          }
        ]
      },
      {
        "id": "Elicit.Intent-GetTravelTime.IntentSlot-ArrivingPlanet",
        "variations": [
          {
            "type": "PlainText",
            "value": "Which planet do you want to travel to?"
          }
        ]
      },
      {
        "id": "Slot.Validation.596358663326.282490667310.1526107495625",
        "variations": [
          {
            "type": "PlainText",
            "value": "I can't answer this question about the sun, only planets. Please tell me a planet."
          },
          {
            "type": "PlainText",
            "value": "While the sun is the center of our solar system, it is not a planet. Please tell me a planet."
          }
        ]
      },
      {
        "id": "Slot.Validation.596358663326.282490667310.1366622834897",
        "variations": [
          {
            "type": "PlainText",
            "value": "{DepartingPlanet} is not a planet. Please tell me one of the nine planets in our solar system. "
          },
          {
            "type": "PlainText",
            "value": "I don't recognize {DepartingPlanet} as a planet in our solar system. Please tell me a planet."
          }
        ]
      }
    ]
  }
}
"""