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


"""
   An AspectPropertyValue is a wrapper for a value
   It lets you check this wrapper has a value inside it
   If not value is set, a specific no value message is returned
"""

class AspectPropertyValue(object):

    """
    Constructor for AspectPropertyValue

    @type value: mixed
    @param value: the property value to store

    @type noValueMessage: string
    @param noValueMessage: if there is no value, the reason for there not being one

    """
    
    def __init__(self, no_value_message = None, value = "noValue"):

        self.noValueMessage = no_value_message

        if(value != "noValue"):
            self.__value = value
            self.__hasValue = True
        else:
            self.__hasValue = False

    def has_value(self):

        return self.__hasValue

    def value(self):
        
        if self.__hasValue:
            return self.__value
        else:
            raise Exception(self.no_value_message())

    def no_value_message(self):

        return self.noValueMessage
