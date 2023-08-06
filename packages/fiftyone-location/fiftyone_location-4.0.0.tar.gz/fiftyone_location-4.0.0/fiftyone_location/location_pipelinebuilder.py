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

from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from fiftyone_pipeline_cloudrequestengine.cloudrequestengine import CloudRequestEngine
from .location_cloud import LocationCloud

"""
 # The Device Detection Pipeline Builder allows you to easily
 # Construct a pipeline containing the device detection cloud engine
 # 
 #  Internal function for getting evidence keys used by cloud engines
 #  
 #   @type settings: dict
 #   @param settings: Should contain a `resourceKey` and optionally a `cloudEndPoint` url
 #   if overriding the default one. An optional cache can be added by passing an instance of 
 #   the DataKeyedCache class as a `cache` setting 
 #   The pipeline builder can also contain JavaScriptBuilder settings
 #   see the documentation for the base PipelineBuilder and JavaScriptBuilder class 
 #   
"""
class LocationPipelineBuilder(PipelineBuilder):
    def __init__(self, settings):

        super(LocationPipelineBuilder, self).__init__(settings)

        # Add specific engines

        self.add(CloudRequestEngine(settings))

        location = LocationCloud(settings)

        if "cache" in settings:
            location.set_cache(settings["cache"])
        
        self.add(location)

