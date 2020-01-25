# hogwarts

Scrape the school's websites for homework and grades.


## Secrets

Secrets are handle using the [SSM Parameter Store](https://serverless.com/framework/docs/providers/aws/guide/variables/#reference-variables-using-the-ssm-parameter-store).

### Set a new secret

```bash
aws ssm put-parameter --name "/hogwarts-api/dev/axios-customer-id" --value "123" --type SecureString  
aws ssm put-parameter --name "/hogwarts-api/dev/axios-username" --value "abc" --type SecureString  
aws ssm put-parameter --name "/hogwarts-api/dev/axios-password" --value "def" --type SecureString  

aws ssm put-parameter --name "/hogwarts-api/dev/telegram-api-token" --value "d3adb33f" --type SecureString  
aws ssm put-parameter --name "/hogwarts-api/dev/telegram-group-chat-id" --value "-123" --type SecureString  
```
