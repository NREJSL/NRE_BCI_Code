

def getConfigureData(name):
    configure_telemetry_data = {
        "messageType": "DATA_ACCESS_CONFIGURATION",
        "messageSource": "Impedance Sample App",
        "data": {
            "experimentName": name
        }
    }
    return configure_telemetry_data

# End Session API post request data
end_session_data = {
    "messageSource": "Impedance Sample App",
    "messageType": "END_SESSION_COMMAND"
}

# Impedance API post request data, by channel
def getChannelData(channel):
    channel_data = {
        "messageType": "MEASURE_IMPEDANCE_COMMAND",
        "messageSource":"Impedance Sample App",
        "data":
            {
                "samplingRateHz": 250,
                "channel": channel
            }
        }
    return channel_data


def getBCIConfigurationData():
    bci_config_data = {
        "messageType": "BCI_CONFIGURATION",
        "messageSource": "Some Application",
        "data": {
            "majorityVoting": True,
            "numEpochsToVote": 4,
            "numWinsRequired": 3,
            "epochWindowSize": 1,
            "slidingWindowHistory": 1,
            "useDynamicThreshold": True,
            "dynamicThreshold": 0.15,
            "dynamicThresholdEpochWindow": 10
        }
    }
    return bci_config_data