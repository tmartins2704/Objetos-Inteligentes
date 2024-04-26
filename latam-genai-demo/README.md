## GenAI demos

#### Summary
A set of demos to help presenting common GenAI usecases.

#### Instructions to deploy it
Befor you start, make sure to configure the Organization Policies so it allows open the cloud run app to all users. (constraints/iam.allowedPolicyMemberDomains)

1. ```cd /app```
2. ```terraform init```
3. ```terraform apply```

You will be asked to provide a dataset and table name. This is the table you want to add to the "Chat with Data" demo.

#### (optional) Edit the code and redeploy the app
1. cd /app
2. run ```gcloud builds submit --tag gcr.io/project_id/latam-demo-app --project=project_id```
3. run ```gcloud run deploy app_name --image gcr.io/project/latam-demo-app --project=project_id```
