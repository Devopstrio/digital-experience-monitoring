provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "dem" {
  name     = "rg-${var.project_name}-dem-${var.environment}"
  location = var.location
}

# --- Experience Analytics Hub (AKS) ---

resource "azurerm_kubernetes_cluster" "dem_k8s" {
  name                = "aks-dem-iq-${var.environment}"
  location            = azurerm_resource_group.dem.location
  resource_group_name = azurerm_resource_group.dem.name
  dns_prefix          = "dem-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-dem-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.dem.name
  location               = azurerm_resource_group.dem.location
  version                = "13"
  administrator_login    = "demadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Timeseries Store (Multi-Cloud Shared Service - ClickHouse) ---

# Note: Using a simplified representation for ClickHouse cluster
resource "azurerm_container_group" "clickhouse" {
  name                = "aci-dem-timeseries-${var.environment}"
  location            = azurerm_resource_group.dem.location
  resource_group_name = azurerm_resource_group.dem.name
  ip_address_type     = "Public"
  os_type             = "Linux"

  container {
    name   = "clickhouse"
    image  = "clickhouse/clickhouse-server:latest"
    cpu    = "2"
    memory = "4"

    ports {
      port     = 8123
      protocol = "TCP"
    }
  }
}

# --- Multi-Cloud Persistence (AWS S3 Experience Sink) ---

resource "aws_s3_bucket" "experience_sink" {
  bucket = "db-dem-experience-sink-${var.environment}"
}
