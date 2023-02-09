import pulumi
import pulumi_gcp as gcp
import pulumi_docker as docker

# Build Docker Image and Push to GCR
registry = gcp.container.Registry('achilles-registry')
registry_url = registry.id.apply(lambda _: gcp.container.get_registry_repository().repository_url)
image_name = registry_url.apply(lambda url: f'{url}/achilles')
registry_info = None # use gcloud for authentication.
achilles_image = docker.Image('achilles-image',
    build=docker.DockerBuild(context='./app'),
    image_name=image_name,
    registry=registry_info
)

## Storage Bucket for CTF Flag & Default JPG
achilles_bucket = gcp.storage.Bucket(
    'achilles_bucket',
    name="achilles_bucket",
    location="US",
    uniform_bucket_level_access=False
)
achilles_weakness_txtfile = gcp.storage.BucketObject(
    'weakness.txt',
    name='weakness.txt',
    bucket=achilles_bucket.name,
    source=pulumi.FileAsset('weakness.txt'),
)
achilles_face_jpg = gcp.storage.BucketObject(
    'face.jpg',
    name='face.jpg',
    bucket=achilles_bucket.name,
    source=pulumi.FileAsset('face.jpg')   
)
# make face jpg public
public_face_jpg_acl = gcp.storage.ObjectACL('public_face_jpg_acl',
    bucket=achilles_bucket.name,
    object=achilles_face_jpg.name,
    role_entities=["READER:allUsers"]
)

# Achilles Cloud Run Application
achilles_webserver = gcp.cloudrun.Service("achilles-webserver",
    location="us-central1",
    template=gcp.cloudrun.ServiceTemplateArgs(
        spec=gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                image=achilles_image.image_name,
            )],
        ),
    )
)


# Add Cloud Run Service Account 
#achilles_service_account = gcp.service_account.Account("sa",
#    account_id="achilles-sa",
#    display_name="achilles-sa"
#)


# Expose the Cloud Run Service publicly
noauth_iam_policy = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
    role="roles/run.invoker",
    members=["allUsers"],
)])
noauth_iam_policy = gcp.cloudrun.IamPolicy("noauthIamPolicy",
    location=achilles_webserver.location,
    project=achilles_webserver.project,
    service=achilles_webserver.name,
    policy_data=noauth_iam_policy.policy_data
)






# Exports
pulumi.export('bucket_name', achilles_bucket.url)
pulumi.export('webserver_url', achilles_webserver.statuses[0].url)