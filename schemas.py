from jsonschema import validate


GET_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "shortlinks": {
      "type": "array"
    }
  },
  "required": [
    "shortlinks"
  ]
}

POST_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "slug": {
      "type": "string",
      "description": "shortlink code"
    },
    "ios": {
      "type": "object",
      "properties": {
        "primary": {
          "type": "string"
        },
        "fallback": {
          "type": "string"
        }
      },
      "required": [
        "primary",
        "fallback"
      ],
      "description": "iPhone URLs"
    },
    "android": {
      "type": "object",
      "properties": {
        "primary": {
          "type": "string"
        },
        "fallback": {
          "type": "string"
        }
      },
      "required": [
        "primary",
        "fallback"
      ],
      "description": "Android URLs"
    },
    "web": {
      "type": "string",
      "description": "Other platforms"
    }
  },
  "required": [
    "ios",
    "android",
    "web"
  ]
}

POST_response_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "status": {
      "type": "string"
    },
    "slug": {
      "type": "string"
    },
    "message": {
      "type": "string"
    }
  }
}

PUT_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    
    "ios": {
      "type": "object",
      "properties": {
        "primary": {
          "type": "string"
        },
        "fallback": {
          "type": "string"
        }
      },
      
      "description": "iPhone URLs"
    },
    "android": {
      "type": "object",
      "properties": {
        "primary": {
          "type": "string"
        },
        "fallback": {
          "type": "string"
        }
      },
      
      "description": "Android URLs"
    },
    "web": {
      "type": "string",
      "description": "Other platforms"
    }
  }
  
}

PUT_response_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "status": {
      "type": "string"
    },
    "message": {
      "type": "string"
    }
  }
}

client_side_error_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "status": {
      "type": "string"
    },
    "message": {
      "type": "string"
    }
  }
}

server_side_error_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {}
}




def validate_get_schema(data):
    return validate(data,GET_schema)

def validate_post_schema(data):
    return validate(data,POST_schema)

def validate_post_response_schema(data):
    return validate(data,POST_response_schema)

def validate_put_schema(data):
    return validate(data,PUT_schema)

def validate_put_response_schema(data):
    return validate(data,PUT_response_schema)

def validate_client_error_schema(data):
    return validate(data,client_side_error_schema)

def validate_server_error_schema(data):
    return validate(data,server_side_error_schema)
