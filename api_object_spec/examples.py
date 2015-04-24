import json

JSL = """
service_name = <string>
pb_name = <string>
package_name = <string>
message = <string>
field_name = <string>
enum_field = <string>
enum_type = <string>

handler_type = "enum"
handler_type = "static"
handlers = "handlers": {<payload_handler>...}

protobufs = <pb_name>: {
                        "package": <package_name>
                }
command = <string>


simple_payload_handler = {
        "handler_type": <handler_type>,
        "pb_name": <pb_name>,
        "message": <message>
}

message_mapping = <command>: {"pb_name": <pb_name>, "message": <message>}
message_mapping = <command>: {
        "pb_name": <pb_name>,
        "message": <message>,
        "handlers": {<simple_payload_handler>...}
}
message_mapping = <command>: null

message_map = {<message_mapping>...}


payload_handler = {
        "handler_type": <handler_type>,
        "pb_name": <pb_name>,
        "message": <message>,
        "handlers": {<payload_handler>...}
}

payload_handler = {
        "handler_type": <handler_type>,
        "enum_field": <enum_field>,
        "pb_name": <pb_name>,
        "enum_type": <enum_type>,
        "message_map": <message_map>
}

payload_handler = <simple_payload_handler>

service_specification = {
        "display_name": <string>,
        "listen_ports": [<number>...],
        "protobufs": {<protobufs>...},
        "request_payload_handler": <payload_handler>,
        "response_payload_handler": <payload_handler>
}

rpc_spec = <service_name>: <service_specification>

rpc = {
    <rpc_spec>...
}
"""


full = json.loads('''
{
    "argon": {
        "display_name": "Argon",
        "listen_ports": [6300],
        "protobufs": {
            "argon_pb": {
                "package": "com.urbanairship.argon.pb.argon"
            },
            "models_pb": {
                "package": "com.urbanairship.argon.pb.models"
            },
            "data_pb": {
                "package": "com.urbanairship.pb.data"
            }
        },
        "request_payload_handler": {
            "handler_type": "static",
            "pb_name": "argon_pb",
            "message": "ArgonRequest",
            "handlers": {
                "payload": {
                    "handler_type": "enum",
                    "enum_field": "type",
                    "pb_name": "argon_pb",
                    "enum_type": "ArgonMessageType",
                    "message_map": {
                        "RETRIEVE_APP": {
                            "pb_name": "argon_pb",
                            "message": "RetrieveApplicationRequest"
                        },
                        "RETRIEVE_LOCATION_APP_KEYS": {
                            "pb_name": "argon_pb",
                            "message": "RetrieveLocationAppKeysRequest"
                        },
                        "REFRESH_APP": {
                            "pb_name": "argon_pb",
                            "message": "RefreshApplicationRequest"
                        },
                        "DISABLE_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "DisableDeviceRegRequest"
                        },
                        "DESTROY_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "DestroyDeviceRegRequest"
                        },
                        "UNINSTALL_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "UninstallDeviceRegRequest"
                        },
                        "UPDATE_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "UpdateDeviceRegRequest",
                            "handlers": {
                                "device_reg": {
                                    "handler_type": "static",
                                    "pb_name": "data_pb",
                                    "message": "DeviceReg"
                                }
                            }
                        },
                        "DISABLE_INACTIVE_APID_DEVICE": {
                            "pb_name": "argon_pb",
                            "message": "DisableInactiveAPIDDeviceRequest"
                        },
                        "UPDATE_PUSH_ADDRESS": {
                            "pb_name": "argon_pb",
                            "message": "UpdatePushAddressRequest"
                        },
                        "IMPORT_PUSH_ADDRESS": {
                            "pb_name": "argon_pb",
                            "message": "ImportPushAddressRequest"
                        },
                        "DECAY_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "DecayDeviceRegRequest"
                        },
                        "DEVICE_REG_ADD_TAGS": {
                            "pb_name": "argon_pb",
                            "message": "DeviceRegTagManipulation"
                        },
                        "DEVICE_REG_REMOVE_TAGS": {
                            "pb_name": "argon_pb",
                            "message": "DeviceRegTagManipulation"
                        },
                        "DEVICE_REG_REPLACE_TAGS": {
                            "pb_name": "argon_pb",
                            "message": "DeviceRegTagManipulation"
                        },
                        "DEVICE_UPDATE_TIMEZONE": {
                            "pb_name": "argon_pb",
                            "message": "UpdateDeviceTimeZoneRequest"
                        },
                        "DEVICE_UPDATE_LOCATION": {
                            "pb_name": "argon_pb",
                            "message": "UpdateDeviceLocationRequest"
                        },
                        "DEVICE_OPEN": {
                            "pb_name": "argon_pb",
                            "message": "DeviceOpenRequest"
                        },
                        "DEVICE_LOCATION_TRANSITION": {
                            "pb_name": "argon_pb",
                            "message": "DeviceLocationTransitionRequest"
                        }
                    }
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "static",
            "pb_name": "argon_pb",
            "message": "ArgonResponse",
            "handlers": {
                "payload": {
                    "handler_type": "enum",
                    "enum_field": "type",
                    "pb_name": "argon_pb",
                    "enum_type": "ArgonMessageType",
                    "message_map": {
                        "RETRIEVE_APP": {
                            "pb_name": "argon_pb",
                            "message": "RetrieveApplicationResponse",
                            "handlers": {
                                "app": {
                                    "handler_type": "static",
                                    "pb_name": "models_pb",
                                    "message": "Application"
                                }
                            }
                        },
                        "RETRIEVE_LOCATION_APP_KEYS": {
                            "pb_name": "argon_pb",
                            "message": "RetrieveLocationAppKeysResponse"
                        },
                        "REFRESH_APP": null,
                        "DISABLE_DEVICE_REG": null,
                        "DESTROY_DEVICE_REG": null,
                        "UNINSTALL_DEVICE_REG": null,
                        "UPDATE_DEVICE_REG": null,
                        "DISABLE_INACTIVE_APID_DEVICE": null,
                        "UPDATE_PUSH_ADDRESS": null,
                        "IMPORT_PUSH_ADDRESS": null,
                        "DECAY_DEVICE_REG": null,
                        "DEVICE_REG_ADD_TAGS": null,
                        "DEVICE_REG_REMOVE_TAGS": null,
                        "DEVICE_REG_REPLACE_TAGS": null,
                        "DEVICE_UPDATE_TIMEZONE": null,
                        "DEVICE_UPDATE_LOCATION": null,
                        "DEVICE_OPEN": null,
                        "DEVICE_LOCATION_TRANSITION": null
                    }
                }
            }
        }
    },
    "hodor": {
        "display_name": "Hodor",
        "listen_ports": [8250],
        "protobufs": {
            "hodor_pb": {
                "package": "com.urbanairship.hodor.pb"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "hodor_pb",
            "enum_type": "RequestType",
            "message_map": {
                "SAVE_MAPPING_REQUEST": {
                    "pb_name": "hodor_pb",
                    "message": "SaveMappingRequest"
                },
                "GET_MASTER_IDENTIFIER_REQUEST": {
                    "pb_name": "hodor_pb",
                    "message": "Query"
                },
                "GET_MAPPED_IDENTIFIERS_REQUEST": {
                    "pb_name": "hodor_pb",
                    "message": "Query"
                },
                "REMOVE_MAPPING_REQUEST": {
                    "pb_name": "hodor_pb",
                    "message": "RemoveMappingRequest"
                },
                "GET_ALL_MASTER_IDENTIFIERS_REQUEST": {
                    "pb_name": "hodor_pb",
                    "message": "Query"
                },
                "GET_ALL_MAPPED_IDENTIFIERS_REQUEST": {
                    "pb_name": "hodor_pb",
                    "message": "Query"
                },
                "GET_MASTER_IDENTIFIER_BATCH_REQUEST": {
                    "pb_name": "hodor_pb",
                    "message": "BatchQuery"
                },
                "GET_MAPPED_IDENTIFIERS_BATCH_REQUEST": {
                    "pb_name": "hodor_pb",
                    "message": "BatchQuery"
                },
                "GET_OR_CREATE_MASTER_IDENTIFIER_REQUEST": {
                    "pb_name": "hodor_pb",
                    "message": "GetOrCreateMasterIdentifierRequest"
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "hodor_pb",
            "enum_type": "ResponseType",
            "message_map": {
                "GET_MASTER_IDENTIFIER_RESPONSE": {
                    "pb_name": "hodor_pb",
                    "message": "GetMasterIdentifierResponse"
                },
                "GET_MAPPED_IDENTIFIERS_RESPONSE": {
                    "pb_name": "hodor_pb",
                    "message": "GetMappedIdentifiersResponse"
                },
                "HISTORICAL_RELATIONSHIPS_RESPONSE": {
                    "pb_name": "hodor_pb",
                    "message": "HistoricalRelationshipsResponse"
                },
                "GET_MASTER_IDENTIFIER_BATCH_RESPONSE": {
                    "pb_name": "hodor_pb",
                    "message": "GetMasterIdentifierBatchResponse"
                },
                "GET_MAPPED_IDENTIFIERS_BATCH_RESPONSE": {
                    "pb_name": "hodor_pb",
                    "message": "GetMappedIdentifiersBatchResponse"
                }
            }
        }
    },
    "gooeybuttercake": {
        "display_name": "GooeyButterCake",
        "listen_ports": [7331],
        "protobufs": {
            "gooeybuttercake_pb": {
                "package": "com.urbanairship.gooeybuttercake.pb"
            },
            "push_pb": {
                "package": "com.urbanairship.push"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "gooeybuttercake_pb",
            "enum_type": "GooeyRequestType",
            "message_map": {
                "ECHO": null,
                "PUSH": {
                    "pb_name": "gooeybuttercake_pb",
                    "message": "PushRequest",
                    "handlers": {
                        "push_envelope": {
                            "handler_type": "static",
                            "pb_name": "push_pb",
                            "message": "PushEnvelope"
                        }
                    }
                },
                "COUNT": {
                    "pb_name": "gooeybuttercake_pb",
                    "message": "CountRequest"
                },
                "LIST": {
                    "pb_name": "gooeybuttercake_pb",
                    "message": "ListRequest"
                },
                "BROADCAST": {
                    "pb_name": "gooeybuttercake_pb",
                    "message": "BroadcastRequest",
                    "handlers": {
                        "push_envelope": {
                            "handler_type": "static",
                            "pb_name": "push_pb",
                            "message": "PushEnvelope"
                        }
                    }
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "gooeybuttercake_pb",
            "enum_type": "GooeyRequestType",
            "message_map": {
                "ECHO": null,
                "PUSH": {
                    "pb_name": "gooeybuttercake_pb",
                    "message": "PushResponse"
                },
                "COUNT": {
                    "pb_name": "gooeybuttercake_pb",
                    "message": "CountResponse"
                },
                "LIST": {
                    "pb_name": "gooeybuttercake_pb",
                    "message": "ListResponse"
                },
                "BROADCAST": {
                    "pb_name": "gooeybuttercake_pb",
                    "message": "BroadcastResponse"
                }
            }
        }
    },
    "venkman": {
        "display_name": "Venkman",
        "listen_ports": [8160],
        "protobufs": {
            "venkman_pb": {
                "package": "com.urbanairship.venkman"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "venkman_pb",
            "enum_type": "RequestType",
            "message_map": {
                "ORDERED_DEVICES_FOR_TAG_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "OrderedDevicesForTagRequest"
                },
                "TAGS_FOR_DEVICE_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagsForDeviceRequest"
                },
                "TAG_DEVICE_COUNT_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagDeviceCountRequest"
                },
                "ORDERED_TAGS_FOR_APP_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "OrderedTagsForAppRequest"
                },
                "ORDERED_DEVICES_FOR_ALIAS_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "OrderedDevicesForAliasRequest"
                },
                "ORDERED_DEVICES_FOR_APP_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "OrderedDevicesForAppRequest"
                },
                "UPDATE_DEVICES_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "UpdateDevicesRequest"
                },
                "APP_TAGS_LISTING_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "AppTagsListingRequest"
                },
                "ORDERED_DEVICES_FOR_CLASS_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "OrderedDevicesForClassRequest"
                },
                "TAG_DEVICE_COUNT_FOR_TAG_CLASS_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagDeviceCountForTagClassRequest"
                },
                "APP_TAG_CLASSES_LISTING_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "AppTagClassesListingRequest"
                },
                "TAG_CLASS_CREATE_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagClassCreateRequest"
                },
                "TAG_CLASS_LIMIT_SET_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagClassSetLimitForAppKeyRequest"
                },
                "TAG_CLASS_LIMIT_GET_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagClassGetLimitForAppKeyRequest"
                },
                "TAG_CLASS_ID_FOR_NAME_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagClassIDForNameRequest"
                },
                "TAG_CLASS_FOR_ID_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagClassForIDRequest"
                },
                "TAG_CLASS_UPDATE_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagClassUpdateRequest"
                },
                "TAG_CLASS_DELETE_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagClassDeleteRequest"
                },
                "APP_TAG_CLASSES_FOR_NAMES_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "AppTagClassesForNamesRequest"
                },
                "TAGS_FOR_DEVICES_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "TagsForDevicesRequest"
                },
                "APP_TAG_CLASSES_FOR_IDS_REQUEST": {
                    "pb_name": "venkman_pb",
                    "message": "AppTagClassesForIDsRequest"
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "static",
            "pb_name": "venkman_pb",
            "message": "Response",
            "handlers": {
                "payload": {
                    "handler_type": "enum",
                    "enum_field": "type",
                    "pb_name": "venkman_pb",
                    "enum_type": "ResponseType",
                    "message_map": {
                        "OK": null,
                        "ERROR": null,
                        "INVALID": null,
                        "ORDERED_DEVICES_FOR_TAG_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "OrderedDevicesForTagResponse"
                        },
                        "TAGS_FOR_DEVICE_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "TagsForDeviceResponse"
                        },
                        "TAG_DEVICE_COUNT_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "TagDeviceCountResponse"
                        },
                        "ORDERED_TAGS_FOR_APP_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "OrderedTagsForAppResponse"
                        },
                        "ORDERED_DEVICES_FOR_ALIAS_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "OrderedDevicesForAliasResponse"
                        },
                        "ORDERED_DEVICES_FOR_APP_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "OrderedDevicesForAppResponse"
                        },
                        "UPDATE_DEVICES_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "UpdateDevicesResponse"
                        },
                        "APP_TAGS_LISTING_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "AppTagsListingResponse"
                        },
                        "ORDERED_DEVICES_FOR_CLASS_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "OrderedDevicesForClassResponse"
                        },
                        "TAG_DEVICE_COUNT_FOR_TAG_CLASS_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "TagDeviceCountForTagClassResponse"
                        },
                        "APP_TAG_CLASSES_LISTING_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "AppTagClassesListingResponse"
                        },
                        "TAG_CLASS_CREATE_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "TagClassCreateResponse"
                        },
                        "TAG_CLASS_LIMIT_SET_RESPONSE": null,
                        "TAG_CLASS_LIMIT_GET_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "TagClassGetLimitForAppKeyResponse"
                        },
                        "TAG_CLASS_ID_FOR_NAME_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "TagClassIDForNameResponse"
                        },
                        "TAG_CLASS_FOR_ID_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "TagClassForIDResponse"
                        },
                        "TAG_CLASS_UPDATE_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "TagClassUpdateResponse"
                        },
                        "APP_TAG_CLASSES_FOR_NAMES_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "AppTagClassesForNamesResponse"
                        },
                        "TAGS_FOR_DEVICES_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "TagsForDevicesResponse"
                        },
                        "APP_TAG_CLASSES_FOR_IDS_RESPONSE": {
                            "pb_name": "venkman_pb",
                            "message": "AppTagClassesForIDsResponse"
                        }
                    }
                }
            }
        }
    },
    "cartographer": {
        "display_name": "Cartographer",
        "listen_ports": [7810, 7910],
        "protobufs": {
            "cartographer_pb": {
                "package": "com.urbanairship.cartographer.pb"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "cartographer_pb",
            "enum_type": "RequestType",
            "message_map": {
                "BUCKETED_LOCATION_REQUEST": {
                    "pb_name": "cartographer_pb",
                    "message": "BucketedLocationRequest"
                },
                "LAST_SEEN_LOCATION_REQUEST": {
                    "pb_name": "cartographer_pb",
                    "message": "LastSeenLocationRequest"
                },
                "TIME_PARTITIONED_BUCKETED_LOCATION_REQUEST": {
                    "pb_name": "cartographer_pb",
                    "message": "TimePartitionBucketRequest"
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "static",
            "pb_name": "cartographer_pb",
            "message": "DevicesResponse"
        }
    },
    "slimer": {
        "display_name": "Slimer",
        "listen_ports": [8150],
        "protobufs": {
            "slimer_pb": {
                "package": "com.urbanairship.slimer.pb"
            },
            "push_pb": {
                "package": "com.urbanairship.push"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "slimer_pb",
            "enum_type": "RequestType",
            "message_map": {
                "BROADCAST_REQUEST": {
                    "pb_name": "slimer_pb",
                    "message": "BroadcastRequest"
                },
                "DEVICE_LIST_REQUEST": {
                    "pb_name": "push_pb",
                    "message": "PushEnvelope"
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "static",
            "pb_name": "slimer_pb",
            "message": "Response"
        }
    },
    "dangerzone": {
        "display_name": "dangerzone",
        "listen_ports": [8500],
        "protobufs": {
            "dangerzone_pb": {
                "package": "com.urbanairship.dangerzone.pb"
            }
        },
        "request_payload_handler": {
            "handler_type": "static",
            "pb_name": "dangerzone_pb",
            "message": "SubmitCommand"
        },
        "response_payload_handler": null
    },
    "nogra": {
        "display_name": "nogra",
        "listen_ports": [8210],
        "protobufs": {
            "nogra_pb": {
                "package": "com.urbanairship.nogra.pb"
            },
            "data_pb": {
                "package": "com.urbanairship.pb.data"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "nogra_pb",
            "enum_type": "RequestType",
            "message_map": {
                "GET_DEVICE_REQUEST": {
                    "pb_name": "nogra_pb",
                    "message": "GetDeviceRequest"
                },
                "GET_DEVICE_LISTING_REQUEST": {
                    "pb_name": "nogra_pb",
                    "message": "GetDeviceListingRequest"
                },
                "GET_DEVICE_SANS_PLATFORM_REQUEST": {
                    "pb_name": "nogra_pb",
                    "message": "GetDeviceSansPlatformRequest"
                },
                "GET_UNINSTALLED_DEVICE_LISTING_REQUEST": {
                    "pb_name": "nogra_pb",
                    "message": "GetUninstalledDeviceListingRequest"
                },
                "GET_DEVICES_REQUEST": {
                    "pb_name": "nogra_pb",
                    "message": "GetDevicesRequest"
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "nogra_pb",
            "enum_type": "ResponseType",
            "message_map": {
                "GET_DEVICE_RESPONSE": {
                    "pb_name": "nogra_pb",
                    "message": "GetDeviceResponse",
                    "handlers": {
                        "device": {
                            "handler_type": "static",
                            "pb_name": "data_pb",
                            "message": "DeviceReg"
                        }
                    }
                },
                "GET_DEVICE_LISTING_RESPONSE": {
                    "pb_name": "nogra_pb",
                    "message": "GetDeviceListingResponse",
                    "handlers": {
                        "device": {
                            "handler_type": "static",
                            "pb_name": "data_pb",
                            "message": "DeviceReg"
                        }
                    }
                },
                "GET_UNINSTALLED_DEVICE_RESPONSE": {
                    "pb_name": "nogra_pb",
                    "message": "GetUninstalledDeviceListingResponse"
                },
                "GET_DEVICES_RESPONSE": {
                    "pb_name": "nogra_pb",
                    "message": "GetDevicesResponse",
                    "handlers": {
                        "device": {
                            "handler_type": "static",
                            "pb_name": "data_pb",
                            "message": "DeviceReg"
                        }
                    }
                }
            }
        }
    },
    "winston": {
        "display_name": "winston",
        "listen_ports": [8275],
        "protobufs": {
            "winston_pb": {
                "package": "com.urbanairship.winston.pb"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "winston_pb",
            "enum_type": "RequestType",
            "message_map": {
                "ASSOCIATE_CHANNEL_REQUEST": {
                    "pb_name": "winston_pb",
                    "message": "AssociateChannelRequest"
                },
                "DISASSOCIATE_CHANNEL_REQUEST": {
                    "pb_name": "winston_pb",
                    "message": "DisassociateChannelRequest"
                },
                "MUTATE_TAGS_REQUEST": {
                    "pb_name": "winston_pb",
                    "message": "MutateTagsRequest"
                },
                "GET_NAMED_USER_REQUEST": {
                    "pb_name": "winston_pb",
                    "message": "GetNamedUserRequest"
                },
                "GET_NAMED_USER_LISTING_REQUEST": {
                    "pb_name": "winston_pb",
                    "message": "GetNamedUserListingRequest"
                },
                "GET_NAMED_USER_COUNT_REQUEST": {
                    "pb_name": "winston_pb",
                    "message": "GetCountRequest"
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "winston_pb",
            "enum_type": "ResponseType",
            "message_map": {
                "ASSOCIATE_CHANNEL_RESPONSE": null,
                "DISASSOCIATE_CHANNEL_RESPONSE": null,
                "MUTATE_TAGS_RESPONSE": null,
                "GET_NAMED_USER_RESPONSE": {
                    "pb_name": "winston_pb",
                    "message": "GetNamedUserResponse"
                },
                "GET_NAMED_USER_LISTING_RESPONSE": {
                    "pb_name": "winston_pb",
                    "message": "GetNamedUserListingResponse"
                },
                "GET_NAMED_USER_COUNT_RESPONSE": {
                    "pb_name": "winston_pb",
                    "message": "GetCountResponse"
                }
            }
        }
    },
    "shennendoah": {
        "display_name": "Reports Ingress",
        "listen_ports": [8899],
        "protobufs": {
            "shennendoah_pb": {
                "package": "com.urbanairship.shennendoah.event"
            }
        },
        "request_payload_handler": {
            "handler_type": "static",
            "pb_name": "shennendoah_pb",
            "message": "ExternalAnalyticsRequest"
        },
        "response_payload_handler": null
    },
    "yaw": {
        "display_name": "Yaw",
        "listen_ports": [6500],
        "protobufs": {
            "push_rpc_pb": {
                "package": "com.urbanairship.push.rpc"
            },
            "push_pb": {
                "package": "com.urbanairship.push"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "push_rpc_pb",
            "enum_type": "RequestType",
            "message_map": {
                "PUSH": {
                    "pb_name": "push_rpc_pb",
                    "message": "PushRequest",
                    "handlers": {
                        "push": {
                            "handler_type": "static",
                            "pb_name": "push_pb",
                            "message": "PushEnvelope"
                        }
                    }
                },
                "PURGE_CRYPTO": {
                    "pb_name": "push_rpc_pb",
                    "message": "PurgeAppCryptoRequest"
                },
                "GET_BANNED_APPS": {
                    "pb_name": "push_rpc_pb",
                    "message": "GetBannedAppsRequest"
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "push_rpc_pb",
            "enum_type": "ResponseType",
            "message_map": {
                "PUSH_RESPONSE": {
                    "pb_name": "push_rpc_pb",
                    "message": "PushResponse"
                },
                "PURGE_CRYPTO_RESPONSE": {
                    "pb_name": "push_rpc_pb",
                    "message": "PurgeAppCryptoResponse"
                },
                "GET_BANNED_APPS_RESPONSE": {
                    "pb_name": "push_rpc_pb",
                    "message": "GetBannedAppsResponse"
                }
            }
        }
    },
    "bonestorm": {
        "display_name": "Bonestorm",
        "listen_ports": [6643],
        "protobufs": {
            "push_rpc_pb": {
                "package": "com.urbanairship.push.rpc"
            },
            "push_pb": {
                "package": "com.urbanairship.push"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "push_rpc_pb",
            "enum_type": "RequestType",
            "message_map": {
                "PUSH": {
                    "pb_name": "push_rpc_pb",
                    "message": "PushRequest",
                    "handlers": {
                        "push": {
                            "handler_type": "static",
                            "pb_name": "push_pb",
                            "message": "PushEnvelope"
                        }
                    }
                },
                "PURGE_CRYPTO": {
                    "pb_name": "push_rpc_pb",
                    "message": "PurgeAppCryptoRequest"
                },
                "GET_BANNED_APPS": {
                    "pb_name": "push_rpc_pb",
                    "message": "GetBannedAppsRequest"
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "push_rpc_pb",
            "enum_type": "ResponseType",
            "message_map": {
                "PUSH_RESPONSE": {
                    "pb_name": "push_rpc_pb",
                    "message": "PushResponse"
                },
                "PURGE_CRYPTO_RESPONSE": {
                    "pb_name": "push_rpc_pb",
                    "message": "PurgeAppCryptoResponse"
                },
                "GET_BANNED_APPS_RESPONSE": {
                    "pb_name": "push_rpc_pb",
                    "message": "GetBannedAppsResponse"
                }
            }
        }
    }
}
''')

bonestorm_spec = {
      "bonestorm": {
        "display_name": "Bonestorm",
        "listen_ports": [6643],
        "protobufs": {
            "push_rpc_pb": {
                "package": "com.urbanairship.push.rpc"
            },
            "push_pb": {
                "package": "com.urbanairship.push"
            }
        },
        "request_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "push_rpc_pb",
            "enum_type": "RequestType",
            "message_map": {
                "PUSH": {
                    "pb_name": "push_rpc_pb",
                    "message": "PushRequest",
                    "handlers": {
                        "push": {
                            "handler_type": "static",
                            "pb_name": "push_pb",
                            "message": "PushEnvelope"
                        }
                    }
                },
                "PURGE_CRYPTO": {
                    "pb_name": "push_rpc_pb",
                    "message": "PurgeAppCryptoRequest"
                },
                "GET_BANNED_APPS": {
                    "pb_name": "push_rpc_pb",
                    "message": "GetBannedAppsRequest"
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "enum",
            "enum_field": "applicationType",
            "pb_name": "push_rpc_pb",
            "enum_type": "ResponseType",
            "message_map": {
                "PUSH_RESPONSE": {
                    "pb_name": "push_rpc_pb",
                    "message": "PushResponse"
                },
                "PURGE_CRYPTO_RESPONSE": {
                    "pb_name": "push_rpc_pb",
                    "message": "PurgeAppCryptoResponse"
                },
                "GET_BANNED_APPS_RESPONSE": {
                    "pb_name": "push_rpc_pb",
                    "message": "GetBannedAppsResponse"
                }
            }
        }
    }
}

argon_example = """
{
    "argon": {
        "display_name": "Argon",
        "listen_ports": [6300],
        "protobufs": {
            "argon_pb": {
                "package": "com.urbanairship.argon.pb.argon"
            },
            "models_pb": {
                "package": "com.urbanairship.argon.pb.models"
            },
            "data_pb": {
                "package": "com.urbanairship.pb.data"
            }
        },
        "request_payload_handler": {
            "handler_type": "static",
            "pb_name": "argon_pb",
            "message": "ArgonRequest",
            "handlers": {
                "payload": {
                    "handler_type": "enum",
                    "enum_field": "type",
                    "pb_name": "argon_pb",
                    "enum_type": "ArgonMessageType",
                    "message_map": {
                        "RETRIEVE_APP": {
                            "pb_name": "argon_pb",
                            "message": "RetrieveApplicationRequest"
                        },
                        "RETRIEVE_LOCATION_APP_KEYS": {
                            "pb_name": "argon_pb",
                            "message": "RetrieveLocationAppKeysRequest"
                        },
                        "REFRESH_APP": {
                            "pb_name": "argon_pb",
                            "message": "RefreshApplicationRequest"
                        },
                        "DISABLE_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "DisableDeviceRegRequest"
                        },
                        "DESTROY_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "DestroyDeviceRegRequest"
                        },
                        "UNINSTALL_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "UninstallDeviceRegRequest"
                        },
                        "UPDATE_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "UpdateDeviceRegRequest",
                            "handlers": {
                                "device_reg": {
                                    "handler_type": "static",
                                    "pb_name": "data_pb",
                                    "message": "DeviceReg"
                                }
                            }
                        },
                        "DISABLE_INACTIVE_APID_DEVICE": {
                            "pb_name": "argon_pb",
                            "message": "DisableInactiveAPIDDeviceRequest"
                        },
                        "UPDATE_PUSH_ADDRESS": {
                            "pb_name": "argon_pb",
                            "message": "UpdatePushAddressRequest"
                        },
                        "IMPORT_PUSH_ADDRESS": {
                            "pb_name": "argon_pb",
                            "message": "ImportPushAddressRequest"
                        },
                        "DECAY_DEVICE_REG": {
                            "pb_name": "argon_pb",
                            "message": "DecayDeviceRegRequest"
                        },
                        "DEVICE_REG_ADD_TAGS": {
                            "pb_name": "argon_pb",
                            "message": "DeviceRegTagManipulation"
                        },
                        "DEVICE_REG_REMOVE_TAGS": {
                            "pb_name": "argon_pb",
                            "message": "DeviceRegTagManipulation"
                        },
                        "DEVICE_REG_REPLACE_TAGS": {
                            "pb_name": "argon_pb",
                            "message": "DeviceRegTagManipulation"
                        },
                        "DEVICE_UPDATE_TIMEZONE": {
                            "pb_name": "argon_pb",
                            "message": "UpdateDeviceTimeZoneRequest"
                        },
                        "DEVICE_UPDATE_LOCATION": {
                            "pb_name": "argon_pb",
                            "message": "UpdateDeviceLocationRequest"
                        },
                        "DEVICE_OPEN": {
                            "pb_name": "argon_pb",
                            "message": "DeviceOpenRequest"
                        },
                        "DEVICE_LOCATION_TRANSITION": {
                            "pb_name": "argon_pb",
                            "message": "DeviceLocationTransitionRequest"
                        }
                    }
                }
            }
        },
        "response_payload_handler": {
            "handler_type": "static",
            "pb_name": "argon_pb",
            "message": "ArgonResponse",
            "handlers": {
                "payload": {
                    "handler_type": "enum",
                    "enum_field": "type",
                    "pb_name": "argon_pb",
                    "enum_type": "ArgonMessageType",
                    "message_map": {
                        "RETRIEVE_APP": {
                            "pb_name": "argon_pb",
                            "message": "RetrieveApplicationResponse",
                            "handlers": {
                                "app": {
                                    "handler_type": "static",
                                    "pb_name": "models_pb",
                                    "message": "Application"
                                }
                            }
                        },
                        "RETRIEVE_LOCATION_APP_KEYS": {
                            "pb_name": "argon_pb",
                            "message": "RetrieveLocationAppKeysResponse"
                        },
                        "REFRESH_APP": null,
                        "DISABLE_DEVICE_REG": null,
                        "DESTROY_DEVICE_REG": null,
                        "UNINSTALL_DEVICE_REG": null,
                        "UPDATE_DEVICE_REG": null,
                        "DISABLE_INACTIVE_APID_DEVICE": null,
                        "UPDATE_PUSH_ADDRESS": null,
                        "IMPORT_PUSH_ADDRESS": null,
                        "DECAY_DEVICE_REG": null,
                        "DEVICE_REG_ADD_TAGS": null,
                        "DEVICE_REG_REMOVE_TAGS": null,
                        "DEVICE_REG_REPLACE_TAGS": null,
                        "DEVICE_UPDATE_TIMEZONE": null,
                        "DEVICE_UPDATE_LOCATION": null,
                        "DEVICE_OPEN": null,
                        "DEVICE_LOCATION_TRANSITION": null
                    }
                }
            }
        }
    }
}
"""


