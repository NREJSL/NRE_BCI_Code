
configure_zero_stimuli_data = {
    "messageType": "STIMULI_CONFIGURATION",
    "messageSource": "Some Application",
    "data": {
        "gyroMode": "DOF0",
        "cameraMode": "STEREO",
        "ccThreshold": 0.5,
        "samplingRateHz": 250,
        "activeChannels": [1,2,3,4,5,6],
        "stimuli": [{
                    "stimuliId": 1,
                    "frequency": 7,
                    "size": 4,
                    "shape": "CIRCLE",
                    "label": "UP",
                    "position" : {
                        "x" : 0,
                        "y" : 0,
                        "z" : 0
                    }
                }]
    }
}

configure_stimuli_data = {
    "messageType": "STIMULI_CONFIGURATION",
    "messageSource": "Some Application",
    "data": {
        "gyroMode": "DOF0",
        "cameraMode": "STEREO",
        "ccThreshold": .99990,
        "samplingRateHz": 250,
        "activeChannels": [1,2,3,4,5,6],
        "stimuli": [
            {
                "stimuliId": 1,
                "frequency": 7,
                "dutyCycle": 0.5,
                "classLabel": "1",
                "size": 4,
                "shape": "CIRCLE",
                "label": "Target test",
                "position": {
                    "x": -10,
                    "y": 20,
                    "z": 60
                }
            },
            {
                "stimuliId": 2,
                "frequency": 7.5,
                "dutyCycle": 0.5,
                "classLabel": "2",
                "size": 4,
                "shape": "CIRCLE",
                "label": "Target 2",
                "position": {
                    "x": 0,
                    "y": 20,
                    "z": 60
                }
            },
            {
                "stimuliId": 3,
                "frequency": 8,
                "dutyCycle": 0.5,
                "classLabel": "3",
                "size": 4,
                "shape": "CIRCLE",
                "label": "Target 3",
                "position": {
                    "x": 10,
                    "y": 20,
                    "z": 60
                }
            },
            {
                    "stimuliId": 4,
                    "frequency": 8.5,
                    "dutyCycle": 0.5,
                    "classLabel": "4",
                    "size": 4,
                    "shape": "CIRCLE",
                    "label": "Target 4",
                    "position" : {
                        "x" : -10,
                        "y" : 10,
                        "z" : 60
                    }
            },
            {
                "stimuliId": 6,
                "frequency": 9.5,
                "dutyCycle": 0.5,
                "classLabel": "6",
                "size": 4,
                "shape": "CIRCLE",
                "label": "Target 6",
                "position" : {
                    "x" : 10,
                    "y" : 10,
                    "z" : 60
                }
            },
            {
                "stimuliId": 7,
                "frequency": 10,
                "dutyCycle": 0.5,
                "classLabel": "7",
                "size": 4,
                "shape": "CIRCLE",
                "label": "Target 7",
                "position" : {
                    "x" : -10,
                    "y" : 0,
                    "z" : 60
                }
            },
            {
                "stimuliId": 8,
                "frequency": 10.5,
                "dutyCycle": 0.5,
                "classLabel": "8",
                "size": 4,
                "shape": "CIRCLE",
                "label": "Target 8",
                "position" : {
                    "x" : 0,
                    "y" : 0,
                    "z" : 60
                }
            },
            {
                "stimuliId": 9,
                "frequency": 11,
                "dutyCycle": 0.5,
                "classLabel": "9",
                "size": 4,
                "shape": "CIRCLE",
                "label": "Target 9",
                "position" : {
                    "x" : 10,
                    "y" : 0,
                    "z" : 60
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
        "samplingRate": 500,
        "sessionToken" : 100,
        "samplesPerEpoch" : 500,
        "enabledChannels" : 63,
        "measureImpedance" : False
    }
}

bci_config_data = {
        "messageType": "BCI_CONFIGURATION",
        "messageSource": "Some Application",
        "data": {
            """"majorityVoting": False,
                    "numEpochsToVote": 100,
                    "numWinsRequired": 90,
                    "epochWindowSize": 100,
                    "slidingWindowHistory": 2,
                    "useDynamicThreshold": False,
                    "dynamicThreshold": 0,
                    "dynamicThresholdEpochWindow": 100
                    
            """
            "majorityVoting": False,
            "numEpochsToVote": 100,
            "numWinsRequired": 90,
            "epochWindowSize": 100,
            "slidingWindowHistory": 2,
            "useDynamicThreshold": False,
            "dynamicThreshold": 1,
            "dynamicThresholdEpochWindow": 100
            
    
        }
}

stimuli_flashing_on_data = {
        "messageType": "STIMULI_FLASHING_CONTROL_MESSAGE",
        "messageSource": "Some application",
        "data": {
            "stimuliActive": True
        }
}

stimuli_flashing_off_data = {
        "messageType": "STIMULI_FLASHING_CONTROL_MESSAGE",
        "messageSource": "Some application",
        "data": {
            "stimuliActive": True
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

def get_stimuli_data_stim_type(stimType):
    return {
        "messageType": "STIMULI_CONFIGURATION",
        "messageSource": "Some Application",
        "data": {
            "gyroMode": "DOF0",
            "cameraMode": "STEREO",
            "ccThreshold": .99990,
            "samplingRateHz": 250,
            "activeChannels": [1,2,3,4,5,6],
            "stimuli": [
            {
                    "stimuliId": 1,
                    "frequency": 7,
                    "dutyCycle": 0.5,
                    "classLabel": "1",
                    "size": 4,
                "shape": f"{stimType}",
                "label": "Target 1",
                "position": {
                    "x": -10,
                    "y": 15,
                    "z": 60
                }
            },
            {
                "stimuliId": 2,
                "frequency": 7.5,
                "dutyCycle": 0.5,
                "classLabel": "2",
                "size": 4,
                "shape": f"{stimType}",
                "label": "Target 2",
                "position": {
                    "x": 0,
                    "y": 15,
                    "z": 60
                }
            },
            {
                "stimuliId": 3,
                "frequency": 8,
                "dutyCycle": 0.5,
                "classLabel": "3",
                "size": 4,
                "shape": f"{stimType}",
                "label": "Target 3",
                "position": {
                    "x": 10,
                    "y": 15,
                    "z": 60
                }
            },
            {
                "stimuliId": 4,
                "frequency": 8.5,
                "dutyCycle": 0.5,
                "classLabel": "4",
                "size": 4,
                "shape": f"{stimType}",
                "label": "Target 4",
                "position" : {
                    "x" : -10,
                    "y" : 5,
                    "z" : 60
                }
            },
            {
                "stimuliId": 6,
                "frequency": 9.5,
                "dutyCycle": 0.5,
                "classLabel": "6",
                "size": 4,
                "shape": f"{stimType}",
                "label": "Target 6",
                "position" : {
                    "x" : 10,
                    "y" : 5,
                    "z" : 60
                }
            },
            {
                "stimuliId": 7,
                "frequency": 10,
                "dutyCycle": 0.5,
                "classLabel": "7",
                "size": 4,
                "shape": f"{stimType}",
                "label": "Target 7",
                "position" : {
                    "x" : -10,
                    "y" : -5,
                    "z" : 60
                }
            },
            {
                "stimuliId": 8,
                "frequency": 10.5,
                "dutyCycle": 0.5,
                "classLabel": "8",
                "size": 4,
                "shape": f"{stimType}",
                "label": "Target 8",
                "position" : {
                    "x" : 0,
                    "y" : -5,
                    "z" : 60
                }
            },
            {
                "stimuliId": 9,
                "frequency": 11,
                "dutyCycle": 0.5,
                "classLabel": "9",
                "size": 4,
                "shape": f"{stimType}",
                "label": "Target 9",
                "position" : {
                    "x" : 10,
                    "y" : -5,
                    "z" : 60
                }
            }
        ]
    }
    }
    