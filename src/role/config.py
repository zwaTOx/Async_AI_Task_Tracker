ACCESS_CONFIG_JSON = {
    "project": {
        "view": ["READER", "USER", "ADMINISTRATOR", "OWNER"],
        "edit": ["ADMINISTRATOR", "OWNER"],
        "delete": ["OWNER"],
        "manage": ["ADMINISTRATOR", "OWNER"]
    },
    "task": {
        "view": ["READER", "USER", "ADMINISTRATOR", "OWNER"],
        "create": ["USER", "ADMINISTRATOR", "OWNER"],
        "manage": ["ADMINISTRATOR", "OWNER"],
    },
    "comment": {
        "view": ["READER", "USER", "ADMINISTRATOR", "OWNER"],
        "create": ["READER", "USER", "ADMINISTRATOR", "OWNER"],
        "edit": ["USER", "ADMINISTRATOR", "OWNER"],
        "delete": ["ADMINISTRATOR", "OWNER"]
    }
}