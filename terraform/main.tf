# ══════════════════════════════════════════════════════════
#  VERSIONES Y BACKEND
# ══════════════════════════════════════════════════════════
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "tf-state-datalake"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ══════════════════════════════════════════════════════════
#  CLOUD STORAGE — Data Lake (raw / processed / curated)
# ══════════════════════════════════════════════════════════
resource "google_storage_bucket" "raw" {
  name                        = "datalake-raw-${var.environment}"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true

  versioning { enabled = true }

  lifecycle_rule {
    condition { age = 365 }
    action    { type = "Delete" }
  }
}

resource "google_storage_bucket" "processed" {
  name                        = "datalake-processed-${var.environment}"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true

  versioning { enabled = true }
}

resource "google_storage_bucket" "curated" {
  name                        = "datalake-curated-${var.environment}"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true

  versioning { enabled = true }
}

# ══════════════════════════════════════════════════════════
#  BIGQUERY — Dataset para análisis
# ══════════════════════════════════════════════════════════
resource "google_bigquery_dataset" "data_mart" {
  dataset_id    = "data_mart_${var.environment}"
  friendly_name = "Data Mart [${var.environment}]"
  description   = "Datos curados listos para análisis"
  location      = "US"
  delete_contents_on_destroy = true
}
