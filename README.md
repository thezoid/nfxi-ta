<img src="/img/nfxi-ta-logo.png" alt="a logo featuring a bear on a red and gray landscape" width="200" height="200/>

# nfxi-ta

In this repository, you will see my practice solution that accomplishes 3 main tasks. The goal was to integrate with GCP (specifically the consumer Drive APIs) to evalute a source directory and copy the content to a destination.

## Setup

```shell
     pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Future improvements

1. Offload secrets into .env from JSON
2. Offload secrets to a key vault

## Customization

| Key                 | Description                                                                                                                                      | Default                               |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------- |
| loggingLevel        | Set the level of logging in the script such that <br><ul><li>`0 = SILENT`</li><li>`1 = ERROR`</li><li>`2 = WARNING`</li><li>`3 = INFO`</li></ul> | 1                                     |
| sourceFolderID      | The folder ID for the source directory                                                                                                           | Null                                  |
| destinationFolderID | The folder ID for the destination directory                                                                                                      | Null                                  |
| scopes              | An array of Google API scopes                                                                                                                    | https://www.googleapis.com/auth/drive |
| clientID            |                                                                                                                                                  |                                       |
| clientSecret        |                                                                                                                                                  |                                       |
