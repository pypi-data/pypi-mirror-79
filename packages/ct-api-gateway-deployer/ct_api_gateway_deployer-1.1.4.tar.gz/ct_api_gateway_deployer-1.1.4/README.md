# ct-api-gateway-deployer

This project aims to automatizate the deployment of an API inside the AWS API Gateway service. 

Also, it provides a helper class to build a Flask API Rest application.

## How it works

The Python package provided in the project will require two configurations files: 
* One file with the AWS configurations to access and deploy the API routes in the API Gateway service;
* Other file with the API routes to be deployed.

When the project executable is executed in the command line, it will read the routes file to build an [OpenAPI](https://www.openapis.org/) JSON object with the [AWS specifications](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-swagger-extensions.html) to be imported in the API Gateway. 

The OpenAPI configuration created in the process is save as an YML file, that can be configured in the command line to be keep and stored in the disk after the process finish to run. 

With the YML file, the process will access the AWS and upload the OpenAPI configuration to the API Gateway. 

Also, this package provides the [_FlaskTools class_](#flaskToolsClass), that allows build an [Flask REST API](https://flask-restful.readthedocs.io/en/latest/) application using the same routes file.

## Installing

The Python package can be installing using the 
[pip](https://pypi.org/project/pip) command:

> pip install ct-api-gateway-deployer

## Usage

### Basic usage

> python ct_api_gateway_deployer [--aws-config=aws.config.json](#awsFile) [--routes=routes.json](#routesFile)

### Command line options

The options can be showed using the console helper:

> python ct_api_gateway_deployer --help


Command option|Required|Description
--------------|--------|-----------
--aws-config=_string_|*True*| Refers to the file's path with the configurations to access the AWS's services and create the API Gateway.
--routes=_string_|*True*| Refers to the file's path with the API's routes configurations to be deployed.
--keep-output-openapifile=_boolean_|False| Boolan flag to keep the OpenAPI file generated during the deployment process. By default, the file is erased in the end of the process.
--output-openapifile-path=_string_|False| Refers the path where will be write the OpenAPI file to be deployed in the API Gateway. By default, will create the file "swagger.yml" in the root path where the command was executed.
-h, --help|False| Show help message.

## <a name="awsFile">Amazon Web Services File Configuration</a>

The _--aws-config_ command option requires a JSON file that specify the configuration object to access the AWS environment. The JSON objects follows the bellow structure: 

```json
{
    "region": "",
    "aws": {
        "access_key_id": "",
        "secret_access_key": ""
    },
    "apiGateway": {
        "name": "",
        "rest_api_id": "",
        "baseEndpointURL": "",
        "stage": "",
        "basePath": ""
    }
}
```

Where:

* Basic object

Attribute|Type|Description
---------|----|-----------
region|string|AWS region identifier where the API Gateway will be deployed.
aws|[_aws_ attribute](#awsAttribute)| AWS access configurations.
apiGateway|[_apiGateway_ attribute](#apiGatewayAttribute)| AWS API Gateway configurations where the API will be deployed.

* <a name="awsAttribute"></a>_aws_ attribute 

Attribute|Type|Description
---------|----|-----------
access_key_id|string|[AWS access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) used to communicate with the API Gateway service.
secret_access_key|string|[AWS secret access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) used to communicate with the API Gateway service.

* <a name="apiGatewayAttribute"></a>_apiGateway_ attribute

Attribute|Type|Description
---------|----|-----------
name|string|AWS API Gateway name.
rest_api_id|string|AWS API Gateway identifier.
stage|string|AWS API Gateway stage where the API will be deployed.
baseEndpointURL|string|Default endpoint for the API resources. Is overwritten by the _url_prefix_; configured in the routes files. 
basePath|string|Default suffix path for the base endpoint. Is overwritten by the stage when the API is deployed by the API Gateway.

## <a name="routesFile">API Routes File Configuration</a>

The _--routes_ command option requires a JSON file that specify the configuration API's routes and configuration. Some attributes of the JSON object will configure directly the API Gateway environment specified in the _--aws-config_; also, other attributes, will be used to configure a Flask REST API through the FlaskTools class provided in the package.
 
The JSON object follows the bellow structure:

```json
{
    "blueprint" : {
        "name": "",
        "url_prefix": "",
        "resources": [{
            "name": "",
            "flask": {
                "resourceModule": "",
                "resourceClass": "",
                "strictSlashes": false
            },
            "methods": [{
                "path": "",
                "cors": {
                  "enable": true, 
                  "removeDefaultResponseTemplates": true,
                  "allowHeaders": [""]
                },
                "queryParams": [{
                   "name": "",
                   "type": ""
                }],
                "actions": [{
                    "type": "",
                    "integration": "",
                    "proxyIntegration": true,
                    "vpcLink": "",
                    "authorization": ""
                }]
            }]
        }]
    }
}
```

Where:

* Basic object

Attribute|Type|Description
---------|----|-----------
blueprint|[_blueprint_ attribute](#blueprintAttribute)| Blueprint configuration. The blueprint concept is explained in: <http://flask.pocoo.org/docs/1.0/blueprints/#blueprints>.

* <a name="blueprintAttribute"></a>_blueprint_ attribute

Attribute|Type|Description
---------|----|-----------
name|string|Blueprint's name.
url_prefix|string|Blueprint's default url prefix for the API resources.
resources| List of [_resource_ attribute](#resourceAttribute)| The list of resources provided by blueprint in the API.

* <a name="resourceAttribute"></a>_resource_ attribute

Attribute|Type|Description
---------|----|-----------
name|string|The resource's name.
flask|[_flask_ attribute](#flaskAttribute)|The Flask's configurations that will be used by the [_FlaskTools class_](#flaskToolsClass).
methods|List of [_method_ attribute](#methodAttribute)|The list of methods that will be allowed for the parent resource.

* <a name="flaskAttribute"></a>_flask_ attribute

Attribute|Type|Description
---------|----|-----------
resourceModule|string|Module where the Flask resource class is available.
resourceClass|string|Nome of the Flask class that implements [_flask_restful.Resource_](https://flask-restful.readthedocs.io/en/latest/api.html#flask_restful.Resource).
strictSlashes|boolean|Boolean flag to ignore the slash character (/) at the end of the in Flask route.

* <a name="methodAttribute"></a>_method_ attribute

Attribute|Type|Description
---------|----|-----------
path|string|Path to the method endpoint.
cors|[_cors_ attribute](#corsAttribute)|Configurations for [CORS](https://enable-cors.org) in the API Gateway.
queryParams|List of [_queryParams_ attribute](#queryParamsAttribute)|Parameters in the routes query.
actions|List of [_action_ attribute](#actionAttribute)|List of HTTP actions allowed in the method. 

* <a name="corsAttribute">_cors_ attribute</a>

Attribute|Type|Description
---------|----|-----------
enable|boolean|Flag to enable the [CORS](https://enable-cors.org) configuration.
removeDefaultResponseTemplates|boolean|Flag to remove the responseTemplate configuration. Used when the default HTTP application/json response is not wanted.
allowHeaders|List of string|List of attributes allowed in the request header.

* <a name="queryParamsAttribute"></a>_queryParams_ attribute

Attribute|Type|Description
---------|----|-----------
name|string|Name of the parameter.
type|string|Type of the parameter. Used in the parse for the route in the Flask REST API resource class.

* <a name="actionAttribute"></a>_action_ attribute

Attribute|Type|Description
---------|----|-----------
type|string|Constant to identify the HTTP request action. Choose one from: GET or POST or PUT or DELETE.
integration|string|[The integration connection type used in the API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-swagger-extensions-integration.html). Choose one from: VPC_LINK or INTERNET.
proxyIntegration|boolean|Flag to enable the integration of the received request on the API Gateway be replicated in the HTTP backend. 
vpcLink|string|AWS VPC identifier. Just use when the _integration_ parameter is configured as VPC_LINK; otherwise, set as _null_. 
authorization|string|Adds verification for authorization headers. Choose from: AWS_IAM or null.

## <a name="flaskToolsClass"></a>FlaskTools class

The FlaskTools Python class can be imported in an Flask REST API project to create an blueprint with the resources routes specified in the _routes_ file.

The method signature is:

```python
from flask import Flask

class FlaskTools:

    @staticmethod
    def add_resources(application: Flask, router_file_path: str) -> None
``` 

Where:

* *application*: is a Flask object where the Blueprint that contains the resources and routes will be appended.
* *router_file_path*: is the path to the JSON file with the routes' configurations.

## Links

* __Pypi repository:__ <https://pypi.org/project/ct-api-gateway-deployer/>
* __Pypi Test repository:__ <https://test.pypi.org/project/ct-api-gateway-deployer/>
* __Source code repository:__ <https://bitbucket.org/cinnecta/ct_api_gateway_deployer>

## Feedback

Every feedback is welcome. Bugs reports, feature request, comments and others can be send directly to the contributors' email.

## Contributors

* Eduardo Manoel ([Business email](eduardo.junior@cinnecta.com)) _[2019]_