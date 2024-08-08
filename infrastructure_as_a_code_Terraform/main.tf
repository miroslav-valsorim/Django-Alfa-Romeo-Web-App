terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.114.0"
    }
  }
}

provider "azurerm" {
  skip_provider_registration = true
  features {}
}

resource "azurerm_resource_group" "arg" {
  name     = var.resource_group_name
  location = var.resource_group_location
}

resource "azurerm_virtual_network" "avn" {
  name                = var.azure_virtual_network_name
  location            = azurerm_resource_group.arg.location
  resource_group_name = azurerm_resource_group.arg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "as" {
  name                 = var.azure_subnet_name_one
  resource_group_name  = azurerm_resource_group.arg.name
  virtual_network_name = azurerm_virtual_network.avn.name
  address_prefixes     = ["10.0.2.0/24"]
  service_endpoints    = ["Microsoft.Storage"]
  delegation {
    name = "fs"
    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

resource "azurerm_subnet" "webapp_subnet" {
  name                 = var.azure_subnet_name_two
  resource_group_name  = azurerm_resource_group.arg.name
  virtual_network_name = azurerm_virtual_network.avn.name
  address_prefixes     = ["10.0.3.0/24"]

  delegation {
    name = "webappdelegation"
    service_delegation {
      name = "Microsoft.Web/serverFarms"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

resource "azurerm_private_dns_zone" "redis_dns_zone" {
  name                = var.azurerm_private_dns_zone_redis_name
  resource_group_name = azurerm_resource_group.arg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "redis_dns_zone_vnl" {
  name                  = var.azurerm_private_dns_zone_virtual_network_link_redis
  private_dns_zone_name = azurerm_private_dns_zone.redis_dns_zone.name
  virtual_network_id    = azurerm_virtual_network.avn.id
  resource_group_name   = azurerm_resource_group.arg.name
  depends_on            = [azurerm_subnet.webapp_subnet]
}

resource "azurerm_private_dns_zone" "postgres_dns_zone" {
  name                = var.azurerm_private_dns_zone_postgres_name
  resource_group_name = azurerm_resource_group.arg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgres_dns_zone_vnl" {
  name                  = var.azurerm_private_dns_zone_virtual_network_link_postgres
  private_dns_zone_name = azurerm_private_dns_zone.postgres_dns_zone.name
  virtual_network_id    = azurerm_virtual_network.avn.id
  resource_group_name   = azurerm_resource_group.arg.name
  depends_on            = [azurerm_subnet.webapp_subnet]
}

resource "azurerm_postgresql_flexible_server" "apfs" {
  name                          = var.azurerm_postgresql_flexible_server_name
  resource_group_name           = azurerm_resource_group.arg.name
  location                      = azurerm_resource_group.arg.location
  version                       = "14"
  administrator_login           = var.azurerm_postgresql_flexible_server_admin_login
  administrator_password        = var.azurerm_postgresql_flexible_server_admin_password
  storage_mb                    = 32768
  sku_name                      = "GP_Standard_D4s_v3"
  zone                          = "1"
  delegated_subnet_id           = azurerm_subnet.as.id
  private_dns_zone_id           = azurerm_private_dns_zone.postgres_dns_zone.id
  public_network_access_enabled = false

  #   depends_on = [azurerm_private_dns_zone_virtual_network_link.apdzvnl]
}

resource "azurerm_postgresql_flexible_server_database" "apfsd" {
  name      = var.azurerm_postgresql_flexible_server_database_name
  server_id = azurerm_postgresql_flexible_server.apfs.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "apfr" {
  name             = var.azurerm_postgresql_flexible_server_firewall_rule_name
  server_id        = azurerm_postgresql_flexible_server.apfs.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "azurerm_service_plan" "asp" {
  name                = var.azurerm_service_plan_name
  location            = azurerm_resource_group.arg.location
  resource_group_name = azurerm_resource_group.arg.name
  sku_name            = var.azurerm_service_plan_sku_name
  os_type             = "Linux"

  depends_on = [azurerm_resource_group.arg]
}

resource "azurerm_linux_web_app" "alwa" {
  name                = var.azurerm_linux_web_app_name
  location            = azurerm_resource_group.arg.location
  resource_group_name = azurerm_resource_group.arg.name
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      python_version = "3.10"
    }
    always_on        = false
    app_command_line = "sh azure.sh"
  }

  app_settings = {
    "DATABASE_URL"                   = "postgres://${azurerm_postgresql_flexible_server.apfs.administrator_login}:${azurerm_postgresql_flexible_server.apfs.administrator_password}@${azurerm_postgresql_flexible_server.apfs.fqdn}:5432/${azurerm_postgresql_flexible_server_database.apfsd.name}"
    "DEBUG"                          = var.azurerm_linux_web_app_var_debug
    "ALLOWED_HOSTS"                  = var.azurerm_linux_web_app_var_allowed_hosts
    "CLOUDINARY_API_KEY"             = var.azurerm_linux_web_app_var_cloudinary_api_key
    "CLOUDINARY_API_SECRET"          = var.azurerm_linux_web_app_var_cloudinary_api_secret
    "CLOUDINARY_NAME"                = var.azurerm_linux_web_app_var_cloudinary_name
    "CSRF_TRUSTED_ORIGINS"           = var.azurerm_linux_web_app_var_csrf_truste_origins
    "EMAIL_HOST"                     = var.azurerm_linux_web_app_var_email_host
    "EMAIL_HOST_PASSWORD"            = var.azurerm_linux_web_app_var_email_host_password
    "EMAIL_HOST_USER"                = var.azurerm_linux_web_app_var_email_host_user
    "EMAIL_PORT"                     = var.azurerm_linux_web_app_var_email_port
    "PAYPAL_RECEIVER_EMAIL"          = var.azurerm_linux_web_app_var_paypal_receiver_email
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = var.azurerm_linux_web_app_var_scm_do_build_during_deployment
    "SECRET_KEY"                     = var.azurerm_linux_web_app_var_secret_key
  }
}

resource "azurerm_app_service_virtual_network_swift_connection" "vnet_integration" {
  app_service_id = azurerm_linux_web_app.alwa.id
  subnet_id      = azurerm_subnet.webapp_subnet.id

  depends_on = [azurerm_linux_web_app.alwa]
}

resource "azurerm_app_service_source_control" "source_control" {
  app_id                 = azurerm_linux_web_app.alwa.id
  repo_url               = var.azurerm_app_service_source_control_URL
  branch                 = "main"
  use_manual_integration = true

  depends_on = [azurerm_linux_web_app.alwa]
}