---
id: app-bundle
title: App bundles
summary: >
  An app bundle is a directory of YAML plus optional Python that turns an empty
  channel into an application — tables for state, flows for work, schedules and
  webhooks to start them. The manifest is the only file meaningful on its own.
concepts: [bundle-version, manifest-keys, flow-identity]
applies_to: [cli, mcp, human]
source: [ParsedTemplateConfig, bundle_file_tree]
---

<!-- BODY TODO: what the directory holds; which four filenames are reserved;
     why fixtures must be .json; what the tree reader descends and what it
     silently skips. -->
