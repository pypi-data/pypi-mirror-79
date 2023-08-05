from .config_chapter import ConfigChapter


class Configuration(ConfigChapter):
    validation_schema = {
        "definitions": {
            "alerting_rule": {
                "type": "object",
                "properties": {
                    "minTime": {
                        "title": "Period in format hh:mm:ss.",
                        "type": "string",
                        "format": "time",
                    },
                    "minThreshold": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 1000000000,
                    },
                    "maxThreshold": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 1000000000,
                    },
                }
            }
        },
        "type": "object",
        "required": [
            "cmd",
        ],
        "properties": {
            "additionalProperties": False,
            "state": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "title": "State filename. Default: state.dat,.",
                        "description": "State filename. Default: state.dat.",
                        "maxLength": 5_000
                    },
                    "required": {
                        "type": "boolean",
                        "title": "Is the state used in the service? Default: false",
                        "description": "Is the state used in the service? Default: false"
                    },
                },
                "title": "State configuration",
                "description": "State configuration",
            },
            "layers": {
                "type": ["array", "null"],
                "minItems": 0,
                "items": {
                    "type": "string",
                    "maxLength": 255
                },
                "title": "List of layers.",
                "description": "List of layers. Each layer identified by strict alias. For example, python-3.6.8, rust-x.y.z.",
            },
            "env": {
                "type": ["array", "null"],
                "minItems": 0,
                "items": {
                    "type": "string",
                },
                "title": "Environment variables for the service",
                "description": "Environment variables for the service. Will be applied for running instance of the service in a container.",
            },
            "cmd": {
                "type": "string",
                "title": "Path to Sign certificate",
                "description": "Path to the service provider certificate file, used for sign process.",
                "maxLength": 10_000
            },
            "workingDir": {
                "type": "string",
                "title": "Working dir for the service",
                "description": "	Working dir for the service. If not specified, the home user dir will be used.",
                "maxLength": 10_000
            },
            "quotas": {
                "type": ["object", "null"],
                "additionalProperties": False,
                "properties": {

                    "cpu": {
                        "type": "integer",
                        "title": "CPU quota.",
                        "description": "CPU quota. Available range 1-100",
                        "minimum": 1,
                        "maximum": 100,
                    },
                    "mem": {
                        "type": "string",
                        "title": "Memory quota.",
                        "description": "Available memory for service.",
                        "pattern": "^\\d*(\\.?\\d*) ?(k|K|kb|KB|m|M|mb|MB|g|G|gb|GB)?$"
                    },
                    "state": {
                        "type": "string",
                        "title": "State size quota.",
                        "description": "State size quota.",
                        "pattern": "^\\d*(\\.?\\d*) ?(k|K|kb|KB|m|M|mb|MB|g|G|gb|GB)?$"
                    },
                    "upload_speed": {
                        "type": "string",
                        "title": "Upload speed quota.",
                        "description": "Upload speed quota.",
                        "pattern": "^\\d*(\\.?\\d*) ?(k|K|kb|KB|m|M|mb|MB|g|G|gb|GB)?$"
                    },
                    "download_speed": {
                        "type": "string",
                        "title": "Download speed quota.",
                        "description": "Download speed quota.",
                        "pattern": "^\\d*(\\.?\\d*) ?(k|K|kb|KB|m|M|mb|MB|g|G|gb|GB)?$"
                    },
                    "upload": {
                        "type": "string",
                        "title": "Upload size quota",
                        "description": "Upload size quota.",
                        "pattern": "^\\d*(\\.?\\d*) ?(k|K|kb|KB|m|M|mb|MB|g|G|gb|GB)?$"
                    },
                    "download": {
                        "type": "string",
                        "title": "Download quota.",
                        "description": "Download quota.",
                        "pattern": "^\\d*(\\.?\\d*) ?(k|K|kb|KB|m|M|mb|MB|g|G|gb|GB)?$"
                    },
                    "temp": {
                        "type": "string",
                        "title": "Temp size quota.",
                        "description": "CPU quota.",
                        "pattern": "^\\d*(\\.?\\d*) ?(k|K|kb|KB|m|M|mb|MB|g|G|gb|GB)?$"
                    }
                },
            },
            "alert": {
                "type": ["object", "null"],
                "additionalProperties": False,
                "properties": {
                    "ram": {"$ref": "#/definitions/alerting_rule"},
                    "cpu": {"$ref": "#/definitions/alerting_rule"},
                    "mem": {"$ref": "#/definitions/alerting_rule"},
                    "state": {"$ref": "#/definitions/alerting_rule"},
                    "upload_speed": {"$ref": "#/definitions/alerting_rule"},
                    "download_speed": {"$ref": "#/definitions/alerting_rule"},
                    "upload": {"$ref": "#/definitions/alerting_rule"},
                    "download": {"$ref": "#/definitions/alerting_rule"},
                    "storage": {"$ref": "#/definitions/alerting_rule"},
                    "temp": {"$ref": "#/definitions/alerting_rule"},
                },
                "title": "Alerting rules",
                "description": "Define alerting rules.",
            },
            "ports": {
                "type": ["array", "null"],
                "minItems": 0,
                "items": {
                    "type": "string",
                    "pattern": "^()([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5]):()([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5])$"
                },
                "title": "List of exposed ports.",
                "description": "List of exposed ports in format ext_port_no:int_port_no.",
            },
            "devices": {
                "type": ["array", "null"],
                "title": "List of mounted into a container host devices",
                "description": "List of mounted into a container host devices. Device aliases are audio, camera.",
                "items": {
                    "type": "object",
                    "required": [
                        "name",
                        "mode"
                    ],
                    "properties": {
                        "name": {
                            "type": "string",
                            "title": "Device name.",
                            "description": "Device name.",
                            "maxLength": 500
                        },
                        "mode": {
                            "type": "string",
                            "title": "Mount type"
                        },
                    },
                },
            },
        },
    }

    @staticmethod
    def from_yaml(input_dict):
        p = Configuration()
        if p.validate(input_dict, validation_schema=p.validation_schema):
            return p
