#!/bin/bash
source virtual/bin/activate
gcloud iam service-accounts list --project  neon-bank-181705  --format="value(reinaldomaslim)"
gcloud app deploy --quiet --project neon-bank-181705
