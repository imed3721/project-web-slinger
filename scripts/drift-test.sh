#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="friendly-neighborhood"
DEPLOYMENT="friendly-neighborhood-watch"
MANIFEST="k8s/deployment.yaml"

echo "=== Kubernetes Drift Detection Test ==="

echo "1. Check the original desired replica count"
kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE"

ORIGINAL_REPLICAS="$(kubectl get deployment "$DEPLOYMENT" \
  -n "$NAMESPACE" \
  -o jsonpath='{.spec.replicas}')"

if [[ "$ORIGINAL_REPLICAS" != "2" ]]; then
  echo "ERROR: expected 2 replicas before the test, got $ORIGINAL_REPLICAS"
  exit 1
fi

echo "2. Introduce deliberate drift: scale to one replica"
kubectl scale deployment "$DEPLOYMENT" \
  --replicas=1 \
  -n "$NAMESPACE"

echo "3. Confirm the live configuration differs from Git"
set +e
kubectl diff -f "$MANIFEST"
DIFF_EXIT=$?
set -e

if [[ "$DIFF_EXIT" -ne 1 ]]; then
  echo "ERROR: expected kubectl diff to detect drift (exit code 1); got $DIFF_EXIT"
  echo "Restoring the declared configuration before exiting."

  kubectl apply -f "$MANIFEST"
  kubectl rollout status "deployment/$DEPLOYMENT" \
    -n "$NAMESPACE" \
    --timeout=120s || true

  exit 1
fi

echo "SUCCESS: kubectl diff detected the replica-count drift"

echo "4. Restore the declared configuration"
kubectl apply -f "$MANIFEST"

echo "5. Wait for the Deployment rollout"
kubectl rollout status "deployment/$DEPLOYMENT" \
  -n "$NAMESPACE" \
  --timeout=120s

echo "6. Verify the restored desired and ready replica counts"
DESIRED="$(kubectl get deployment "$DEPLOYMENT" \
  -n "$NAMESPACE" \
  -o jsonpath='{.spec.replicas}')"

READY="$(kubectl get deployment "$DEPLOYMENT" \
  -n "$NAMESPACE" \
  -o jsonpath='{.status.readyReplicas}')"

if [[ "$DESIRED" != "2" || "$READY" != "2" ]]; then
  echo "ERROR: expected 2 desired and ready replicas; desired=$DESIRED ready=$READY"
  exit 1
fi

echo "SUCCESS: Kubernetes drift detected and repaired"
