 # *********************************************************************
 # This Original Work is copyright of 51 Degrees Mobile Experts Limited.
 # Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
 # Caversham, Reading, Berkshire, United Kingdom RG4 7BY.
 #
 # This Original Work is licensed under the European Union Public Licence (EUPL) 
 # v.1.2 and is subject to its terms as set out below.
 #
 # If a copy of the EUPL was not distributed with this file, You can obtain
 # one at https://opensource.org/licenses/EUPL-1.2.
 #
 # The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
 # amended by the European Commission) shall be deemed incompatible for
 # the purposes of the Work and the provisions of the compatibility
 # clause in Article 5 of the EUPL shall not apply.
 # 
 # If using the Work as, or as part of, a network application, by 
 # including the attribution notice(s) required under Article 5 of the EUPL
 # in the end user terms of the application under an appropriate heading, 
 # such notice(s) shall fulfill the requirements of that article.
 # ********************************************************************


from fiftyone_pipeline_engines.engine import Engine
from fiftyone_pipeline_engines.aspectdata_dictionary import AspectDataDictionary
from fiftyone_pipeline_core.aspectproperty_value import AspectPropertyValue

import json

"""
    This is a template for all 51Degrees cloud engines.
    It requires the 51Degrees cloudRequestEngine to be placed in a
    pipeline before it. It takes that raw JSON response and
    parses it to extract the device part.
    It also uses this data to generate a list of properties and an evidence key filter

"""
class CloudEngine(Engine):

    def __init__(self):

        super(CloudEngine, self).__init__()

        self.datakey = "CloudEngineBase" # This should be overriden

    def on_registration(self, pipeline):
 
        """
        Callback called when an engine is added to a pipeline
        In this case sets up the properties list for the element from
        data in the CloudRequestEngine

        @type pipeline: Pipeline
        @param pipeline

        """

        if not "cloud" in pipeline.flow_elements_list:
            raise Exception("CloudRequestEngine needs to be placed before cloud elements in Pipeline")

        # Add properties from the CloudRequestEngine which should already have them
        self.properties = pipeline.flow_elements_list["cloud"].flow_element_properties[self.datakey]


    def process_internal(self, flowData):
  
        cloudData = flowData.get("cloud").get("cloud")

        cloudData = json.loads(cloudData)

        engineData = cloudData[self.datakey]

        result = {}

        for key, value in engineData.items():

            if key + "nullreason" in cloudData[self.datakey]:
                result[key] = AspectPropertyValue(no_value_message=cloudData[self.datakey][key + "nullreason"])
            else:
                result[key] = AspectPropertyValue(None, value)

        data = AspectDataDictionary(self, result)
            
        flowData.set_element_data(data)
