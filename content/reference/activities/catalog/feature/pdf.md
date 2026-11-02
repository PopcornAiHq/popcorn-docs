---
id: activities/catalog/feature/pdf
title: feature.pdf
order: 137
group: Activities
parent: activities/catalog/feature
layout: lookup
updated: 2026-10-31
summary: >
  One domain's activities, each with the Step that calls it, its arguments and
  what it returns.
lede: >
  The feature.pdf activities, with how a Step calls each and its arguments.
concepts: [activities, flow-grammar]
---

The `feature.pdf` activities at `release` or `beta` status; `beta` ones are
marked. Each also takes the optional `integration_id` and
`integration_name` arguments, which the
[Activities](https://docs.popcorn.ai/activities.md) page explains.

### `feature.pdf.extract_page_rows`

*Beta.*

Extract structured rows from rendered PDF page images with a vision LLM.

Reads the `pages` (rendered by `pdf.render_pages`) up to `max_pages`,
applies `instructions` to pull generic rows from each page, and stages the
result to an agent-store file (`rows_file_key`). Run in batches and
combined by `pdf.merge_page_rows`.

```yaml
- id: <step>
  activity: feature.pdf.extract_page_rows
  args:
    conversation_id: <string>
    source: ...
    pages: <array>
    instructions: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of this activity. Normally injected by the interpreter from the manifest band. Default `0.0`. |
| `progress_pct_end` | number | no | Overall completion % when this activity finishes. Normally injected by the interpreter from the manifest band. Default `100.0`. |
| `conversation_id` | string | yes | Conversation UUID that owns the page image uploads (must be the flow's own conversation). |
| `source` | PdfRenderSource | yes | Source PDF metadata. |
| `pages` | list of PdfPageImage | yes | Rendered page image refs from pdf.render_pages. |
| `max_pages` | integer, optional | no | Maximum number of page refs to inspect serially. Default `3`. |
| `instructions` | string | yes | Extraction instructions for the visible PDF page content. |
| `model` | string | no | Claude model id or Bedrock inference profile id. Default `"claude-sonnet-4-6"`. |
| `max_tokens` | integer | no | Maximum model output tokens per page. Default `4096`. |
| `progress_total_pages` | integer, optional | no | Total pages across all batches — the denominator for the overall completion percentage shown during extraction. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `page_count` | integer |  |
| `row_count` | integer |  |
| `pages` | list of PdfExtractedPage |  |
| `rows` | list of PdfExtractedRow |  |
| `rows_file_key` | string, optional |  |
| `model` | string |  |

`PdfExtractedPage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `file_key` | string |  |
| `storage` | string |  |
| `row_count` | integer |  |

`PdfExtractedRow`:

| Field | Type | Notes |
|---|---|---|
| `source_file_key` | string |  |
| `source_filename` | string, optional |  |
| `page_number` | integer |  |
| `page_image_file_key` | string |  |
| `page_image_storage` | string |  |
| `row_index` | integer |  |
| `extracted_text` | string |  |
| `summary` | string |  |
| `fields` | object |  |
| `row_data` | object |  |
| `confidence` | number, optional |  |
| `model` | string |  |

`PdfPageImage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `file_key` | string |  |
| `storage` | string |  |
| `filename` | string |  |
| `mime_type` | string |  |
| `width_px` | integer |  |
| `height_px` | integer |  |
| `dpi` | integer |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

`PdfRenderSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string, optional |  |
| `agent_store_file_key` | string, optional |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

### `feature.pdf.extract_row_images`

*Beta.*

Crop per-row cell images from the source PDF and attach them to rows.

Loads the merged rows from `rows_file_key`, pulls each row's native or
raster-cropped image from the source PDF, uploads it, and writes the image
refs back onto the rows (re-staged as a new blob). Returns the new
`rows_file_key` plus the image list.

```yaml
- id: <step>
  activity: feature.pdf.extract_row_images
  args:
    conversation_id: <string>
    source: ...
    rows_file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `progress_kind` | string, optional | no | Status-widget kind slug (e.g. file_upsert_progress) to emit in-activity progress under. Unset: no progress is emitted. |
| `progress_state` | string, optional | no | The phase this activity climbs (e.g. 'reading'). The interpreter resolves its pct band + default label from the channel's status_kinds manifest; emitted as the envelope state. |
| `progress_label` | string, optional | no | Human-readable widget label. Normally filled by the interpreter from the manifest phase; a flow can set it explicitly to override the phase default. |
| `progress_pct_start` | number | no | Overall completion % at the start of image attachment. Default `70.0`. |
| `progress_pct_end` | number | no | Overall completion % when image attachment finishes. Default `90.0`. |
| `conversation_id` | string | yes | Conversation UUID that owns the source PDF and rows (must be the flow's own conversation). |
| `source` | PdfRenderSource | yes | Source PDF metadata. |
| `rows_file_key` | string | yes | Agent-store file of rows from pdf.merge_page_rows. |
| `max_pages` | integer, optional | no | Optional cap for attaching row images. |
| `dpi` | integer | no | DPI used when raster-cropping row images from PDF pages. Default `300`. |
| `progress_after_seconds` | number | no | Minimum elapsed time before the first progress update. Default `2.0`. |
| `progress_every_seconds` | number | no | Minimum elapsed time between progress updates. Default `2.0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `image_count` | integer |  |
| `rows_file_key` | string |  |
| `images` | list of PdfExtractedRowImage |  |
| `warnings` | list of string |  |

`PdfExtractedRowImage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `row_index` | integer |  |
| `file_key` | string |  |
| `filename` | string |  |
| `storage` | string |  |
| `mime_type` | string |  |
| `width_px` | integer, optional |  |
| `height_px` | integer, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string |  |
| `bbox` | PdfRowImageBBox |  |

`PdfRenderSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string, optional |  |
| `agent_store_file_key` | string, optional |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

`PdfRowImageBBox`:

| Field | Type | Notes |
|---|---|---|
| `x0` | number |  |
| `y0` | number |  |
| `x1` | number |  |
| `y1` | number |  |
| `units` | string |  |

### `feature.pdf.inspect_fields`

List the placeholders and signature tags in an agent-store PDF.

```yaml
- id: <step>
  activity: feature.pdf.inspect_fields
  args:
    conversation_id: <string>
    file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file_key` | string | yes | Agent-store file key of the template PDF, e.g. 'templates/retainer.pdf' (the file_key that foundation.file.copy_to_store or feature.gdrive.download_to_store returned). Any text-layer PDF works, whatever produced it. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string |  |
| `sha256` | string | Digest of the template as read. |
| `page_count` | integer |  |
| `has_text_layer` | boolean |  |
| `keys` | list of string | Distinct placeholder keys, sorted — the values map merge_fields expects. |
| `placeholders` | list of PdfPlaceholder |  |
| `placeholder_count` | integer |  |
| `signature_tags` | list of PdfSignatureTag |  |
| `signer_roles` | list of string | Distinct roles across the signature tags, in the order the template means them (signer 2 before signer 10) — what feature.signing.send_document's signers must cover. A simple [[signer N date]] tag adds no role: it belongs to the signer it names. |
| `unknown_tokens` | list of PdfUnknownToken | [[...]] / «...» tokens that are neither a placeholder key nor a signer tag. The merge leaves them as written and counts them unresolved; fix the template. |
| `tag_formats` | list of string | The signature-tag spellings this template uses: 'tag', 'simple', or both — which is a template mixing them. |
| `split_placeholders` | list of PdfSplitPlaceholder | Placeholders that wrap across a line; the merge cannot fill these and the template should be fixed. |
| `fonts` | list of string | Font families the PDF uses. |
| `warnings` | list of string |  |

`PdfPlaceholder`:

| Field | Type | Notes |
|---|---|---|
| `key` | string | The name inside [[...]]. |
| `page` | integer | 1-based page number. |
| `bbox` | list of number | [x0, y0, x1, y1] in PDF points, origin top-left. |

`PdfSignatureTag`:

| Field | Type | Notes |
|---|---|---|
| `name` | string | Field name: the text before the first ';' of a {{...}} tag; the role for [[signer N]]; '<role> date' for [[signer N date]]. |
| `role` | string | The role= attribute. |
| `type` | string | The type= attribute of a {{...}} tag; 'signature' for [[signer N]]; 'datenow' (the provider's read-only, stamped-on-completion date) for [[signer N date]]. |
| `page` | integer |  |
| `bbox` | list of number, optional |  |
| `format` | string | Which spelling the author used: 'tag' for {{Name;role=Role;type=signature}}, which the provider reads out of the PDF itself, or 'simple' for [[signer 1]] / «Signer_1», whose box merge_fields measures and reports instead. |

`PdfSplitPlaceholder`:

| Field | Type | Notes |
|---|---|---|
| `fragment` | string | The text after '[[' (or '«') on the line where it opened. |
| `page` | integer |  |
| `bbox` | list of number |  |

`PdfUnknownToken`:

| Field | Type | Notes |
|---|---|---|
| `text` | string |  |
| `page` | integer |  |
| `bbox` | list of number, optional |  |

### `feature.pdf.merge_fields`

Fill [[key]] placeholders in an agent-store PDF and store the result.

Template-source-agnostic: any PDF with a text layer works, whether a
Google Docs export, a copied conversation upload or a vendor form.

```yaml
- id: <step>
  activity: feature.pdf.merge_fields
  args:
    conversation_id: <string>
    template_file_key: <string>
    store_file_key_stem: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `template_file_key` | string | yes | Agent-store file key of the immutable template PDF, e.g. 'templates/retainer.pdf'. Never modified. |
| `values` | map of string | no | Placeholder key -> text. Keys absent here are left as [[key]] in the output and counted in unresolved_count, and so is a key whose value is blank or whitespace. Values may not contain '{{' or the placeholder syntax '[[' / ']]'. |
| `store_file_key_stem` | string | yes | Target agent-store file key WITHOUT extension, e.g. 'documents/retainer-42'. The merged PDF lands at '<stem>.pdf' and previews at '<stem>-p<N>.png'; any prior '<stem>.*' is replaced. |
| `placeholder_syntax` | string | no | Placeholder form. Only [[key]] is supported; it is named so a second syntax can be added without a rename. Default `"double_square"`. |
| `overflow_policy` | `shrink` / `flag` | no | When a merged line is wider than its column: 'shrink' reduces the font size down to min_font_size and reports 'overflowed'; 'flag' leaves the line unmerged and reports it. Default `"shrink"`. |
| `min_font_size` | number | no | Smallest font size shrink-to-fit may use. Default `8.0`. |
| `preview_dpi` | integer | no | Resolution of the per-page PNG previews rendered here from the merged bytes and uploaded concurrently; 0 renders none and leaves them to a fan-out of feature.pdf.render_preview_pages over preview_page_batches. Default `100`. |
| `preview_batch_size` | integer | no | Pages per entry of the reported preview_page_batches — how coarse a flow's render fan-out is. Does not affect the inline previews. Default `2`. |
| `inline_preview_pages` | integer, optional | no | How many pages to render and store INLINE, from page 1; the rest are reported under deferred_page_batches for a feature.pdf.render_preview_pages step (publish: true) to land after the row has published — so a reader sees page 1 the moment the document exists and the rest as each arrives. None (the default) renders every page inline, as before. Only with a non-zero preview_dpi. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | Agent-store file key of the merged PDF. |
| `sha256` | string | Digest of the merged bytes. Deterministic for the same template, values and options. |
| `size_bytes` | integer |  |
| `page_count` | integer |  |
| `page_numbers` | list of integer | Ordered 1-based page numbers for workflow preview fan-out. |
| `template_sha256` | string | Digest of the template as read. |
| `preview_file_keys` | list of string | One PNG per page, in page order; empty when preview_dpi is 0. |
| `preview_page_batches` | list of PreviewPageBatch | Consecutive 1-based page ranges of at most preview_batch_size pages covering the whole merged PDF — what a flow hands a foreach over feature.pdf.render_preview_pages so the previews render concurrently instead of inline. Always reported; meaningful with preview_dpi 0. |
| `planned_preview_file_keys` | list of string | Every page's durable preview key, in page order, whether or not this call wrote it — what a row's Preview Keys should read when the pages beyond inline_preview_pages are still on their way. |
| `deferred_page_batches` | list of PreviewPageBatch | The pages NOT rendered inline (after inline_preview_pages), in ranges of at most preview_batch_size — for a feature.pdf.render_preview_pages step with publish: true. Empty when every page was rendered here. |
| `placements` | list of PdfMergePlacement |  |
| `resolved_count` | integer |  |
| `overflowed_count` | integer |  |
| `unresolved_count` | integer | Placeholders still in the document, counted by RESCANNING the merged PDF (no value, split across lines, or left unmerged under overflow_policy flag). Gate a signature send on this being 0. |
| `keys_without_value` | list of string |  |
| `unused_values` | list of string | Keys in `values` that the template does not carry. |
| `signature_fields` | list of PdfSignatureField | One per [[signer N]] tag, measured on the MERGED page and ordered by signer: pass these to feature.signing.send_document's `fields` so each signer's box lands on the line the tag marks — the underscores or rule beside the tag, or the one directly below it. Empty for a template that uses the {{...}} tags the provider reads itself. |
| `signer_roles` | list of string | Distinct roles across `signature_fields`, in order. |

`PdfMergePlacement`:

| Field | Type | Notes |
|---|---|---|
| `key` | string |  |
| `page` | integer | 1-based page number. |
| `bbox` | list of number | [x0, y0, x1, y1] of the placeholder in PDF points. |
| `status` | string | resolved / overflowed (written, shrunk to fit) / unresolved_no_value / unresolved_split / unresolved_overflow (policy flag: did not fit, placeholder left in the document) / unresolved_unknown_token (a [[...]] / «...» that is neither a placeholder key nor a signer tag; left as written). |
| `fitted_size` | number | Font size the value was set at. |
| `note` | string |  |

`PdfSignatureField`:

| Field | Type | Notes |
|---|---|---|
| `name` | string | Field label the signer sees: the role for a signature box, '<role> date' for its date box. |
| `role` | string | Which signer fills it, e.g. 'signer 1'. |
| `type` | string | 'signature', or 'datenow' for a [[signer N date]] box — read-only, stamped by the provider with the date that signer completed. |
| `required` | boolean | True for a signature box. False for a date box: the provider fills it, there is nothing for the signer to do. |
| `page` | integer | 1-based page number. |
| `area` | PdfSignatureFieldArea |  |

`PdfSignatureFieldArea`:

| Field | Type | Notes |
|---|---|---|
| `x` | number | Left edge, 0.0-1.0 of page width. |
| `y` | number | Top edge, 0.0-1.0 of page height. |
| `w` | number | Width, 0.0-1.0 of page width. |
| `h` | number | Height, 0.0-1.0 of page height. |

`PreviewPageBatch`:

| Field | Type | Notes |
|---|---|---|
| `first_page` | integer |  |
| `last_page` | integer |  |

### `feature.pdf.merge_page_rows`

*Beta.*

Combine the per-batch outputs of `pdf.extract_page_rows` into one set.

Materializes every batch's staged rows, sorts them by page/row, and
re-stages the merged set as a single `rows_file_key`. `min_rows` turns
"the document had no extractable rows at all" into a hard failure instead
of a silent empty import. (Whether the rows look like a particular schema's
data is a downstream/channel concern, not this generic merge step's.)

```yaml
- id: <step>
  activity: feature.pdf.merge_page_rows
  args:
    batches: <array>
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `batches` | list of PdfExtractPageRowsOutput | yes | Outputs returned by batched pdf.extract_page_rows calls. |
| `conversation_id` | string | yes | Conversation UUID that owns the staged rows blobs. |
| `source` | PdfRenderSource, optional | no | Fallback source metadata when batches is empty. |
| `model` | string, optional | no | Fallback model name when batches is empty. |
| `min_rows` | integer | no | Fail (non-retryable, type PdfNoRowsExtracted) when the merged row count is below this. Lets a flow turn 'the document had no extractable data' into a hard failure instead of an empty silent-success import. 0 (default) keeps the legacy behavior. Default `0`. |
| `cleanup_file_keys` | list of string | no | Deprecated no-op. Scratch blobs are uploaded as workflow-lifetime agent-store files and are owned by the temp-file reaper. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `page_count` | integer |  |
| `row_count` | integer |  |
| `rows_file_key` | string |  |
| `model` | string |  |

`PdfExtractPageRowsOutput`:

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `page_count` | integer |  |
| `row_count` | integer |  |
| `pages` | list of PdfExtractedPage |  |
| `rows` | list of PdfExtractedRow |  |
| `rows_file_key` | string, optional |  |
| `model` | string |  |

`PdfExtractedPage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `file_key` | string |  |
| `storage` | string |  |
| `row_count` | integer |  |

`PdfExtractedRow`:

| Field | Type | Notes |
|---|---|---|
| `source_file_key` | string |  |
| `source_filename` | string, optional |  |
| `page_number` | integer |  |
| `page_image_file_key` | string |  |
| `page_image_storage` | string |  |
| `row_index` | integer |  |
| `extracted_text` | string |  |
| `summary` | string |  |
| `fields` | object |  |
| `row_data` | object |  |
| `confidence` | number, optional |  |
| `model` | string |  |

`PdfRenderSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string, optional |  |
| `agent_store_file_key` | string, optional |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

### `feature.pdf.pin_template`

Preserve a staged PDF as an immutable template in this conversation.

```yaml
- id: <step>
  activity: feature.pdf.pin_template
  args:
    conversation_id: <string>
    file_key: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes |  |
| `file_key` | string | yes | The staged agent-store PDF file key. |
| `preview_dpi` | integer | no | Render one PNG per page of the unfilled template at this resolution beside the pin ('templates/<sha256[:16]>-p<N>.png'), once per content digest; 0 (the default) renders none. Match the merge's preview_dpi so the template page and the first merged page are the same size on screen. Default `0`. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `file_key` | string | templates/<sha256[:16]>.pdf |
| `sha256` | string |  |
| `size_bytes` | integer |  |
| `page_count` | integer | Pages rendered; 0 when preview_dpi was 0. |
| `preview_file_keys` | list of string | templates/<sha256[:16]>-p<N>.png, one per page: the UNFILLED template, for a row to show before its first merge. Empty when preview_dpi was 0. |

### `feature.pdf.render_pages`

*Beta.*

Render conversation uploads, or one stored page for workflow fan-out.

Conversation mode retains its original temporary outputs. Agent-store
mode requires a page, source digest and output stem and stores a durable
preview; callers choose workflow concurrency and publication policy.

```yaml
- id: <step>
  activity: feature.pdf.render_pages
  args:
    conversation_id: <string>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | Conversation UUID that owns the source PDF and generated pages (must be the flow's own conversation). |
| `conversation_file_key` | string, optional | no | Conversation-level source PDF file key (file_uploads). |
| `agent_store_file_key` | string, optional | no | Stored PDF to render in single-page durable mode. |
| `page_number` | integer, optional | no |  |
| `source_sha256` | string, optional | no | Expected PDF digest in durable mode. |
| `store_file_key_stem` | string, optional | no | Durable mode writes <stem>-p<N>.png. |
| `dpi` | integer | no | Render resolution in dots per inch. Default `144`. |
| `max_pages` | integer, optional | no | Optional cap for early tests or previews. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `source` | PdfRenderSource |  |
| `page_count` | integer |  |
| `pages` | list of PdfPageImage |  |
| `page_file_keys` | list of string |  |

`PdfPageImage`:

| Field | Type | Notes |
|---|---|---|
| `page_number` | integer |  |
| `file_key` | string |  |
| `storage` | string |  |
| `filename` | string |  |
| `mime_type` | string |  |
| `width_px` | integer |  |
| `height_px` | integer |  |
| `dpi` | integer |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

`PdfRenderSource`:

| Field | Type | Notes |
|---|---|---|
| `conversation_file_key` | string, optional |  |
| `agent_store_file_key` | string, optional |  |
| `filename` | string, optional |  |
| `mime_type` | string, optional |  |
| `size_bytes` | integer, optional |  |
| `sha256` | string, optional |  |

### `feature.pdf.render_preview_pages`

Render pages first_page..last_page of a stored PDF to scratch PNGs.

```yaml
- id: <step>
  activity: feature.pdf.render_preview_pages
  args:
    conversation_id: <string>
    file_key: <string>
    store_file_key_stem: <string>
    first_page: <integer>
    last_page: <integer>
```

**Arguments**

| Argument | Type | Required | Notes |
|---|---|---|---|
| `conversation_id` | string | yes | The flow's own conversation UUID. |
| `file_key` | string | yes | Agent-store file key of the PDF to render, e.g. the merged 'documents/42/run-1.pdf'. |
| `store_file_key_stem` | string | yes | Key stem the previews will be published under by collect_previews ('<stem>-p<N>.png'); here it only names the scratch keys. |
| `first_page` | integer | yes | 1-based, inclusive. |
| `last_page` | integer | yes | 1-based, inclusive. |
| `dpi` | integer | no | Resolution of the PNGs. 100 matches the inline render and the pinned template's own previews. Default `100`. |
| `publish` | boolean | no | Write each page to its DURABLE key (<stem>-p<N>.png, the one Preview Keys names) instead of workflow scratch — for the pages a merge left to land after the row published. Default `false`. |
| `progress` | PreviewProgress, optional | no | With publish: after each page lands, in page order, patch a row column with the highest contiguous page number now stored, so a reader's pane can promote pages one by one. Guarded: skipped once the row no longer carries guard_value in guard_column (another rebuild published meanwhile). Best effort. |

**Returns**

| Field | Type | Notes |
|---|---|---|
| `first_page` | integer |  |
| `last_page` | integer |  |
| `reported_through` | integer | With progress: the highest page number the row was told is stored; 0 when nothing was reported (no progress asked, or the guard failed before the first page). |
| `lifetime` | string | 'workflow': every key here is scratch the store reaps when the workflow chain closes. |
| `pages` | list of PdfRenderedPreview | One entry per page in the range, in page order. |
| `preview_file_keys` | list of string | The pages' SCRATCH keys, in page order — what collect_previews promotes. Not the row's Preview Keys. |

`PdfRenderedPreview`:

| Field | Type | Notes |
|---|---|---|
| `page` | integer | 1-based page number. |
| `file_key` | string | The SCRATCH key (lifetime=workflow) this page rendered to. Never publish it: collect_previews promotes it to the permanent '<stem>-p<N>.png'. |
| `sha256` | string |  |
| `size_bytes` | integer |  |

`PreviewProgress`:

| Field | Type | Notes |
|---|---|---|
| `table_name` | string |  |
| `record_id` | integer |  |
| `column` | string |  |
| `guard_column` | string |  |
| `guard_value` | string |  |
