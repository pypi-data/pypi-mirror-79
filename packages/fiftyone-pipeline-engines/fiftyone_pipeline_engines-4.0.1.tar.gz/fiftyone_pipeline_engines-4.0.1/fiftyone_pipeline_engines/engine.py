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

from fiftyone_pipeline_core.flowelement import FlowElement

import json

class Engine(FlowElement):

    def __init__(self):

        super(Engine, self).__init__()
    
    def set_cache(self, cache):
        """
        Add a cache to an engine
        @type casee: Cache
        @param cache: Cache with get and set methods

        """
        
        self.cache = cache


    def set_restricted_properties(self, properties_list):
        """"
        Add a subset of properties
        
        @type properties_list: string[] 
        @param properties_list: An array of properties to include
        
        """
 
        self.restricted_properties = properties_list
  

    def in_cache(self, flowData):
        """
        A method to check if a flowData's evidence is in the cache
        
        @type FlowData: FlowData
        @param FlowData:

        @rtype: bool
        @return: True or false: a flowData's evidence is in the cache

        """
    
        keys = self.filter_evidence(flowData)

        cacheKey = json.dumps(keys)

        cached = self.cache.get_cache_value(cacheKey)

        if cached is not None:
            flowData.set_element_data(cached)

            return True
        else:
            return False
  



    def process(self, flowdata):

        """
        Engine's core process function.
        Calls specific overriden processInternal methods but wraps it in a cache check
        and a cache put
        
        @type flowdata: FlowData
        @param flowData:
        
        """

        if hasattr(self, "cache"):

            if self.in_cache(flowdata):
                return True
            else:
                self.process_internal(flowdata)
                cacheKey = json.dumps(self.filter_evidence(flowdata))
                self.cache.set_cache_value(cacheKey, flowdata.get(self.datakey))

        else:

            self.process_internal(flowdata)
