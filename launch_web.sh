#!/bin/bash
source virtual/bin/activate
gsutil rm -r gs://staging.neon-bank-181705.appspot.com 
gcloud app deploy --quiet --project neon-bank-181705 