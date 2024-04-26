terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 3.5"
    }
  }

  required_version = ">= 0.12"
}

data "google_project" "current" {}

variable "BQ_DATASET" {
  type        = string
  description = "BigQuery dataset name"
}

variable "BQ_TABLE" {
  type        = string
  description = "BigQuery table name"
}

resource "google_project_service" "services" {
  for_each = toset([
    "cloudbuild.googleapis.com",
    "containerregistry.googleapis.com",
    "run.googleapis.com",
    "bigquery.googleapis.com",
    "aiplatform.googleapis.com",
    "storage-component.googleapis.com",
    "iamcredentials.googleapis.com"
  ])

  service = each.key
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "google_storage_bucket" "latam_demo_app_bucket" {
  name     = "latam-demo-app-${random_string.suffix.result}"
  location = "US"
  uniform_bucket_level_access = true 
}

resource "google_service_account" "latam_demo_app" {
  account_id   = "latam-demo-app"
  display_name = "Latam Demo App Service Account"
}

resource "google_project_iam_member" "latam_demo_app_storage_access" {
  project = data.google_project.current.project_id
  role    = "roles/storage.objectAdmin"  
  member  = "serviceAccount:${google_service_account.latam_demo_app.email}"
}

resource "google_service_account_iam_member" "latam_demo_app_token_creator" {
  service_account_id = google_service_account.latam_demo_app.name 
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:${google_service_account.latam_demo_app.email}"
}

resource "google_project_iam_member" "latam_demo_app_vertexai" {
  project = data.google_project.current.project_id
  role    = "roles/aiplatform.admin"
  member  = "serviceAccount:${google_service_account.latam_demo_app.email}"
}

resource "google_project_iam_member" "latam_demo_app_bigquery" {
  project = data.google_project.current.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.latam_demo_app.email}"
}

resource "null_resource" "build_and_push_image" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "gcloud builds submit --tag gcr.io/${data.google_project.current.project_id}/latam-demo-app:latest ."
  }
}

resource "google_cloud_run_service" "latam_demo_app" {
  depends_on = [null_resource.build_and_push_image]

  name     = "latam-demo-app"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/${data.google_project.current.project_id}/latam-demo-app:latest"

        env {
          name  = "PROJECT_ID"
          value = data.google_project.current.project_id
        }
        env {
          name  = "BQ_DATASET"
          value = var.BQ_DATASET
        }
        env {
          name  = "BQ_TABLE"
          value = var.BQ_TABLE
        }
        env { 
          name  = "BUCKET_NAME"
          value = google_storage_bucket.latam_demo_app_bucket.name  
        }
      }

      service_account_name = google_service_account.latam_demo_app.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true
}

resource "google_cloud_run_service_iam_policy" "latam_demo_app_invoker" {
  location    = google_cloud_run_service.latam_demo_app.location
  project     = data.google_project.current.project_id
  service     = google_cloud_run_service.latam_demo_app.name

  policy_data = jsonencode({
    bindings = [
      {
        role    = "roles/run.invoker"
        members = [
          "allUsers",
        ]
      },
    ]
  })
}

output "cloud_run_url" {
  value = google_cloud_run_service.latam_demo_app.status[0].url
}