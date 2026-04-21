module "devops_api" {
  source       = "../../modules/devops_api"
  namespace    = var.namespace
  release_name = var.release_name
}
