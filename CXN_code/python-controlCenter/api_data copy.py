

configure_stimuli_data = {
    "messageType": "STIMULI_CONFIGURATION",
    "messageSource": "Some Application",
    "data": {
        "gyroMode": "DOF3",
        "cameraMode": "STEREO",
        "ccThreshold": 0.99,
        "samplingRateHz": 250,
        "activeChannels": [1,2,3,4,5,6],
        "stimuli": [
                {
                    "stimuliId": 1,
                    "frequency": 7,
                    "size": 8,
                    "shape": "CIRCLE",
                    "label": "UP",
                    "position" : {
                        "x" : 0,
                        "y" : -10,
                        "z" : 50
                    }
                },
                {
                    "stimuliId": 2,
                    "frequency": 7.5,
                    "size": 8,
                    "shape": "CIRCLE",
                    "label": "DOWN",
                    "position" : {
                        "x" : 0,
                        "y" : -30,
                        "z" : 50
                    }
                },
                 {
                    "stimuliId": 3,
                    "frequency": 8,
                    "size": 4,
                    "shape": "SQUARE",
                    "label": "LEFT",
                    "position" : {
                        "x" : -10,
                        "y" : -20,
                        "z" : 50
                    }
                },
                
                 {
                    "stimuliId": 4,
                    "frequency": 8.5,
                    "size": 4,
                    "shape": "SQUARE",
                    "label": "RIGHT",
                    "position" : {
                        "x" : 10,
                        "y" : -20,
                        "z" : 50
                    }
                }
        ]
    }
}

start_session_data = {
    "messageSource": "Some application",
    "messageType": "START_SESSION_COMMAND"
}

end_session_data = {
    "messageSource": "Some application",
    "messageType": "END_SESSION_COMMAND"
}

start_telemetry_data = {
    "messageType": "START_TELEMETRY_MESSAGE",
    "messageSource": "Test System",
    "data" : {
        "samplingRate": 2000,
        "sessionToken" : 100, 
        "enabledChannels" : 63,
        "measureImpedance" : False
    }
}

bci_config_data = {
        "messageType": "BCI_CONFIGURATION",
        "messageSource": "Some Application",
        "data": {
            "majorityVoting": False,
            "numEpochsToVote": 400,
            "numWinsRequired": 300,
            "epochWindowSize": 125,
            "slidingWindowHistory": 2,
            "useDynamicThreshold": False,
            "dynamicThreshold": 0,
            "dynamicThresholdEpochWindow": 1000
        }
}


def get_configure_telemetry_data(name):
    return {
        "messageType": "DATA_ACCESS_CONFIGURATION",
        "messageSource": "Some application",
        "data": {
            "experimentName": f"{name}"
        }
    }