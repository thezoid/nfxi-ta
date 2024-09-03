# nfxi-ta

In this repository, you will see my practice solution that accomplishes 3 main tasks. The goal was to integrate with GCP (specifically the consumer Drive APIs) to evalute a source directory and copy the content to a destination.

## Setup

```shell
     pip3 install virtualenv
     virtualenv nfxi-ta
     source nfxi-ta/bin/activate
     nfxi-ta/bin/pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Follow the steps on [this](https://developers.google.com/workspace/guides/create-credentials) page to setup your authentication.

You will need to setup the below scopes at a minimum (least privileged revision to come).
![a picture showing the scopes needed to be defined on the google project oauth consent screen](/img/appScopes.png)

Rename your project OAuth credential file to `credentials.json` and place it inside of the `local` directory.

## Future improvements

1. Offload secrets into env vars from JSON or offload secrets to a key vault

## Customization

| Key                 | Description                                                                                                                                                                       | Default                               |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| loggingLevel        | Set the level of logging in the script such that <br><ul><li>`0 = SILENT`</li><li>`1 = ERROR`</li><li>`2 = WARNING and SUCCESS` </li><li>`3 = INFO`</li><li>`4 = DEBUG`</li></ul> | 1                                     |
| sourceFolderID      | The folder ID for the source directory                                                                                                                                            | Null                                  |
| destinationFolderID | The folder ID for the destination directory                                                                                                                                       | Null                                  |
| scopes              | An array of Google API scopes                                                                                                                                                     | https://www.googleapis.com/auth/drive |
