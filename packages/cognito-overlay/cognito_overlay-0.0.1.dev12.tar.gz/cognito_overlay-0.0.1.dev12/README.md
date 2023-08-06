# Cognito Overlay

AWS Cognito is AWS's authentication framework.

This overlay is intended to leverage a Cognito User Pool and provide authorizers and a simplified API (via Flask App) that can be mounted into an existing API Gateway (rather than communicating with the Cognito service from the front-end directly).

A Terraform Module is also provided that will stand up the IAM roles and Cognito User Pool and groups. This can be referenced directly, or used as a basis for a different implementation.