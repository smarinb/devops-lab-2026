resource "kubernetes_namespace" "this" {
  metadata {
    name = var.namespace
  }
}

resource "helm_release" "this" {
  name      = var.release_name
  namespace = kubernetes_namespace.this.metadata[0].name
  chart     = abspath("${path.root}/../../helm/devops-api")

  depends_on = [kubernetes_namespace.this]
}
