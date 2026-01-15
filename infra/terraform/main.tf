terraform {
  required_version = ">= 1.5.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = ">= 3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_network" "devops_task" {
  name = "devops_task_network"
}

resource "docker_volume" "db_data" {
  name = "devops_task_db_data"
}

resource "docker_volume" "grafana_data" {
  name = "devops_task_grafana_data"
}

output "network" { value = docker_network.devops_task.name }
output "db_volume" { value = docker_volume.db_data.name }
output "grafana_volume" { value = docker_volume.grafana_data.name }
