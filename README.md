# Adding Operator Inputs into SiteWise
In an Industrial environment, the Operators can be an important source of information, for instance, they can enter the machine status (In maintenance, Stopped, Waiting parts from the productions line, operator in break,...) and it can be used to calculate metrics such as OEE (Overall equipment effectiveness).

## Architecuture
![Architecture](/docs/architecture.png)

** **The Code in this repository covers only the Operator input path (steps 1-4)**

## Files
* **operator_hmi.html** - Operator Input SPA (Single Page Application)
> *Change:*
> ```python
> const ALIAS = "<SITEWISE-ALIAS-CHANGE-IT>";
> const URL = "<API-GATEWAY-ENDPOINT-CHANGE-IT>";
> ````
  
* **read_write_operator_input.py** - Machine status AWS Lambda - Used to read and update status from the DynamoDB
> ```
> Table name:	operator-input
> Primary partition: key	propertyAlias (String)
> Primary sort key: timestamp (Number)
> Additional Field: Comment (String)
> Additional Field: ropertyValue (Number)
> ````
  
* **write_iotcore_from_dynamodb.py** - Read Amazon DynamoDB Streams and push message to IoTCore
> *Sample Topic at AWS IoT Core*
> ```python
> TOPIC = "lambda/operator/input"
> ````
  
* **siteWiseRuleRole.json** - AWS IoT SiteWise to grant AWS IoT Rule Access
> *Change AWS IoT Alias resource or * for tests (DON"T use it in production), then create a new Role*
> ```JSON
> "Resource": "<ARN-AWS-IoT-SiteWise-ALIAS - CHANGE-IT>"
> ````
  
* **operInputToSiteWiseRule.json** - AWS IoT Rule Definition
> *Change the roleARN by the roleARN created basead on the file siteWiseRuleRole.json* 
> ```python
> "roleArn": "<ARN-AWS-IoT-SiteWise-Access-Role - CHANGE-IT>"
> ````
 
> *AWS CLI command to create the AWS Iot Rule*
> ```Bash
> aws iot create-topic-rule --rule-name OperInputToSiteWiseRule --topic-rule-payload file://operInputToSiteWiseRule.json
> ````

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

