class APIData():
    
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
            "samplingRate": 250,
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
                "majorityVoting": True,
                "numEpochsToVote": 4,
                "numWinsRequired": 3,
                "epochWindowSize": 1.25,
                "slidingWindowHistory": 2,
                "useDynamicThreshold": True,
                "dynamicThreshold": 0.15,
                "dynamicThresholdEpochWindow": 10
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
                "stimuliActive": False
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

    
    def get_four_stimuli_layout(stimType:str):
        return {
            "messageType": "STIMULI_CONFIGURATION",
            "messageSource": "Some Application",
            "data": {
                "gyroMode": "DOF0",
                "cameraMode": "STEREO",
                "ccThreshold": .65,
                "samplingRateHz": 500,
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
                        "x": -7,
                        "y": 12,
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
                        "x": 7,
                        "y": 12,
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
                        "x": -7,
                        "y": -5,
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
                        "x" : 7,
                        "y" : -5,
                        "z" : 60
                    }
                }
        
                ]
            }
        }
    
    def get_eight_stimuli_layout(stimType:str):
         return {
            "messageType": "STIMULI_CONFIGURATION",
            "messageSource": "Some Application",
            "data": {
                "gyroMode": "DOF0",
                "cameraMode": "STEREO",
                "ccThreshold": .65,
                "samplingRateHz": 500,
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
                        "x": -9,
                        "y": 12,
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
                        "x": -3,
                        "y": 12,
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
                        "x": 3,
                        "y": 12,
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
                        "x" : 9,
                        "y" : 12,
                        "z" : 60
                    }
                },
                {
                        "stimuliId": 5,
                        "frequency": 9,
                        "dutyCycle": 0.5,
                        "classLabel": "5",
                        "size": 4,
                    "shape": f"{stimType}",
                    "label": "Target 5",
                    "position": {
                        "x": -9,
                        "y": 0,
                        "z": 60
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
                    "position": {
                        "x": -3,
                        "y": 0,
                        "z": 60
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
                    "position": {
                        "x": 3,
                        "y": 0,
                        "z": 60
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
                        "x" : 9,
                        "y" : 0,
                        "z" : 60
                    }
                }
        
                ]
            }
        }
    
    def get_twelve_stimuli_layout(stimType:str):
         return {
            "messageType": "STIMULI_CONFIGURATION",
            "messageSource": "Some Application",
            "data": {
                "gyroMode": "DOF0",
                "cameraMode": "STEREO",
                "ccThreshold": .65,
                "samplingRateHz": 500,
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
                        "x": 7,
                        "y": 12,
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
                        "x": 15,
                        "y": 12,
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
                        "x": 15,
                        "y": 3,
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
                        "x" : 15,
                        "y" : -6,
                        "z" : 60
                    }
                },
                {
                        "stimuliId": 5,
                        "frequency": 9,
                        "dutyCycle": 0.5,
                        "classLabel": "5",
                        "size": 4,
                    "shape": f"{stimType}",
                    "label": "Target 5",
                    "position": {
                        "x": 7,
                        "y": -6,
                        "z": 60
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
                    "position": {
                        "x": 0,
                        "y": -6,
                        "z": 60
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
                    "position": {
                        "x": -7,
                        "y": -6,
                        "z": 60
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
                        "x" : -15,
                        "y" : -6,
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
                        "x" : -15,
                        "y" : 3,
                        "z" : 60
                    }
                },
                {
                    "stimuliId": 10,
                    "frequency": 11.5,
                    "dutyCycle": 0.5,
                    "classLabel": "10",
                    "size": 4,
                    "shape": f"{stimType}",
                    "label": "Target 10",
                    "position" : {
                        "x" : -15,
                        "y" : 12,
                        "z" : 60
                    }
                },
                {
                    "stimuliId": 11,
                    "frequency": 12,
                    "dutyCycle": 0.5,
                    "classLabel": "11",
                    "size": 4,
                    "shape": f"{stimType}",
                    "label": "Target 11",
                    "position" : {
                        "x" : -7,
                        "y" : 12,
                        "z" : 60
                    }
                },
                {
                    "stimuliId": 12,
                    "frequency": 12.5,
                    "dutyCycle": 0.5,
                    "classLabel": "12",
                    "size": 4,
                    "shape": f"{stimType}",
                    "label": "Target 12",
                    "position" : {
                        "x" : 0,
                        "y" : 12,
                        "z" : 60
                    }
                }
                
        
                ]
            }
        }
        