output "bucket_raw" {
  value = "gs://${google_storage_bucket.raw.name}"
}

output "bucket_processed" {
  value = "gs://${google_storage_bucket.processed.name}"
}

output "bucket_curated" {
  value = "gs://${google_storage_bucket.curated.name}"
}

output "bigquery_dataset" {
  value = google_bigquery_dataset.data_mart.dataset_id
}

output "dataflow_sa" {
  value = google_service_account.dataflow.email
}

output "trigger_plan" {
  value = google_cloudbuild_trigger.plan.trigger_id
}

output "trigger_apply" {
  value = google_cloudbuild_trigger.apply.trigger_id
}
