variable "project_id" {
  description = "ID del proyecto en GCP"
  type        = string
}

variable "region" {
  description = "Region de despliegue"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Entorno: dev | staging | prod"
  type        = string
  default     = "dev"
}

variable "alert_email" {
  description = "Email para alertas de monitoreo"
  type        = string
}
