terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  credentials = "../keys/gcp_creds.json"
  project     = "promptgen"
  region      = "us-central1"

}