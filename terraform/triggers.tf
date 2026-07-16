# ══════════════════════════════════════════════════════════
#  CLOUD BUILD TRIGGERS — Plan (automático) + Apply (con aprobación)
#
#  Requiere que la app de GitHub de Cloud Build ya esté conectada
#  al repositorio (paso único que se hace una vez desde la consola
#  de GCP: Cloud Build > Repositorios > Conectar repositorio).
# ══════════════════════════════════════════════════════════

resource "google_cloudbuild_trigger" "plan" {
  name        = "pipeline-plan-${var.environment}"
  description = "Valida, escanea con tfsec y genera el plan de Terraform"
  filename    = "cloudbuild-plan.yaml"

  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = "^main$"
    }
  }

  substitutions = {
    _ENV   = var.environment
    _EMAIL = var.alert_email
  }
}

resource "google_cloudbuild_trigger" "apply" {
  name        = "pipeline-apply-${var.environment}"
  description = "Aplica el plan ya generado, requiere aprobación manual"
  filename    = "cloudbuild-apply.yaml"

  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = "^main$"
    }
  }

  approval_config {
    approval_required = true
  }

  substitutions = {
    _ENV   = var.environment
    _EMAIL = var.alert_email
  }
}
