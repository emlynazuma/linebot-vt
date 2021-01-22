#!/usr/bin/env bash
GREEN='\033[0;31m'
RED='\033[0;31m'
NC='\033[0m' # No Color

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

echo -e "${GREEN}* - Decrypting${NC}"
gcloud beta secrets versions access latest --project=voicetube-test --secret=linebot-dev-env --project=voicetube-test > $DIR/.env
gcloud beta secrets versions access latest --project=voicetube-test --secret=cloud-run-test-gcp-service-account-credential --project=voicetube-test > $DIR/.voicetube-test-service-account.json
