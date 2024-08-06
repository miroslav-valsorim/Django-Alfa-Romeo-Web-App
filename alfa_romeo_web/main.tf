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
  name     = "alfaromeoresourcegrp"
  location = "Italy North"
}

resource "azurerm_virtual_network" "avn" {
  name                = "AlfaVirtualNetwork"
  location            = azurerm_resource_group.arg.location
  resource_group_name = azurerm_resource_group.arg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "as" {
  name                 = "AlfaSubnet"
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
  name                 = "WebAppSubnet"
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
  name                = "alfaprivatelink.redis.cache.windows.net"
  resource_group_name = azurerm_resource_group.arg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "redis_dns_zone_vnl" {
  name                  = "alfaredisVnetZoneLink"
  private_dns_zone_name = azurerm_private_dns_zone.redis_dns_zone.name
  virtual_network_id    = azurerm_virtual_network.avn.id
  resource_group_name   = azurerm_resource_group.arg.name
  depends_on            = [azurerm_subnet.webapp_subnet]
}

resource "azurerm_private_dns_zone" "postgres_dns_zone" {
  name                = "alfaprivatelink.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.arg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgres_dns_zone_vnl" {
  name                  = "alfapostgresVnetZoneLink"
  private_dns_zone_name = azurerm_private_dns_zone.postgres_dns_zone.name
  virtual_network_id    = azurerm_virtual_network.avn.id
  resource_group_name   = azurerm_resource_group.arg.name
  depends_on            = [azurerm_subnet.webapp_subnet]
}

resource "azurerm_postgresql_flexible_server" "apfs" {
  name                          = "postgreserver-unique-alfa"
  resource_group_name           = azurerm_resource_group.arg.name
  location                      = azurerm_resource_group.arg.location
  version                       = "14"
  administrator_login           = ""
  administrator_password        = ""
  storage_mb                    = 32768
  sku_name                      = "GP_Standard_D4s_v3"
  zone                          = "1"
  delegated_subnet_id           = azurerm_subnet.as.id
  private_dns_zone_id           = azurerm_private_dns_zone.postgres_dns_zone.id
  public_network_access_enabled = false

  #   depends_on = [azurerm_private_dns_zone_virtual_network_link.apdzvnl]
}

resource "azurerm_postgresql_flexible_server_database" "apfsd" {
  name      = "exampledb"
  server_id = azurerm_postgresql_flexible_server.apfs.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "apfr" {
  name             = "postgrefw"
  server_id        = azurerm_postgresql_flexible_server.apfs.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "azurerm_service_plan" "asp" {
  name                = "DjangoServicePlan"
  location            = azurerm_resource_group.arg.location
  resource_group_name = azurerm_resource_group.arg.name
  sku_name            = "B1"
  os_type             = "Linux"

  depends_on = [azurerm_resource_group.arg]
}

resource "azurerm_linux_web_app" "alwa" {
  name                = "AlfaRomeoWebApp"
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
    "DEBUG"                          = "False"
    "ALLOWED_HOSTS"                  = ""
    "CLOUDINARY_API_KEY"             = ""
    "CLOUDINARY_API_SECRET"          = ""
    "CLOUDINARY_NAME"                = ""
    "CSRF_TRUSTED_ORIGINS"           = ""
    "EMAIL_HOST"                     = ""
    "EMAIL_HOST_PASSWORD"            = ""
    "EMAIL_HOST_USER"                = ""
    "EMAIL_PORT"                     = "587"
    "PAYPAL_RECEIVER_EMAIL"          = ""
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "1"
    "SECRET_KEY"                     = ""
  }
}

resource "azurerm_app_service_virtual_network_swift_connection" "vnet_integration" {
  app_service_id = azurerm_linux_web_app.alwa.id
  subnet_id      = azurerm_subnet.webapp_subnet.id

  depends_on = [azurerm_linux_web_app.alwa]
}

resource "azurerm_app_service_source_control" "source_control" {
  app_id                 = azurerm_linux_web_app.alwa.id
  repo_url               = ""
  branch                 = "main"
  use_manual_integration = true

  depends_on = [azurerm_linux_web_app.alwa]
}
