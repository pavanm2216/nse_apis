# NSE backend audit and rearrangement plan

Audit date: 19 October 2026. Authority: `NSEMF_API_Details_V1.9.8.pdf`, August 2026, 238 pages. See [the coverage map](NSE_API_V1_9_8_COVERAGE.md) for public routes, upstream paths, source modules, and PDF pages.

## Result and scope

The backend already exposes most of the documented operations. Adding more route files is not the first priority: contract validation, successful-result persistence, version retirement, and mixed feature ownership need attention first.

This audit changes documentation only. It is a static inspection of route registration, upstream URL constants, shared authentication/transport code, selected schemas, persistence paths, and test entry points. It is not a complete field-by-field certification of all 183 UCC columns, every NFT field, or every report. No NSE calls, credential changes, database connections, or registrations were performed.

The map contains 84 local route/upstream pairs and 83 distinct configured upstream URLs, compared with 82 distinct URL strings found in the PDF. This is not a count of supported current operations: the PDF retains a removed operation and repeats COA for single-bank changes. Two local KYC routes also share one upstream API. No documented URL lacked a case-insensitive code match; that does not establish functional completeness.

## Findings to address before moving code

| Priority | Finding and evidence | Required action |
|---|---|---|
| High | `routers/order.py` accepts only `NEW` and `VALID` in `_SUCCESS_STATUSES`. The order-entry contract on PDF pp. 9-10 returns `TRXN SUCCESS` or `TRXN FAILED`. A documented successful response is returned to the caller but skipped in database persistence. | Add the documented success status and a mocked response/persistence regression test. Preserve additional statuses only when supported by actual NSE evidence. |
| High | `/registration/kyc-fresh-register` uses `KycFreshRegisterRequest` in `schemas/misc_services.py`, forwarding `pan_no`, `client_code`, etc. PDF p. 165 requires `amcCode`, `panNo`, `mobileNo`, `invEmail` and returns `link`/`message`. The existing `/ekyc/register` uses the documented key names. | Make both entry points use a single documented KYC contract. Decide compatibility for existing callers explicitly; the snake-case model lacks required AMC data. Reuse the link/message response model. |
| High | `schemas/sip.py` and `schemas/stp.py` make every detail field optional. For example, `reg_data: [{}]` satisfies these schemas despite mandatory client, scheme, dates and amount/unit rules in PDF pp. 21-24 and 26-28. | Separate request and response models, require documented fields, and implement conditional validations. Start with SIP/STP and extend the same audit to XSIP/SWP, mandates, UCC, and NFT. |
| Medium | `routers/misc_reports.py` sends lowercase `2fa`, `client_authorization`, and `order_lifecycle`; PDF pp. 118, 119 and 126 specifies `2FA`, `CLIENT_AUTHORIZATION`, and `ORDER_LIFECYCLE`. | Match documented URL case. Whether NSE currently tolerates case differences remains unverified. Public backend paths can stay unchanged. |
| Medium | `main.py` still mounts `routers/elog_upload.py`, calling `/registration/eLOG`. The v1.9.8 changelog on p. 238 removes Bank ELog Upload even though its older section remains on p. 96. | Treat upload as retired for the v1.9.8 target. Plan compatibility/deprecation before removal. Do not infer that the separate ELog Upload Report is retired. |
| Medium | `OrderRequest` requires `order_amount` and `buy_sell_type` for every transaction while p. 7 makes buy/sell type purchase-specific and p. 8 allows redemption units or all units. Mandatory flags such as `dpc_flag` are optional locally. | Model purchase, redemption and all-units conditions explicitly; validate identifiers, flags, lengths and numeric precision. An explicit blank currently works around some required string fields, but omission is rejected. |
| Medium | `routers/sip.py` persists every returned `reg_data` record, without checking `reg_status`; `routers/switch.py` likewise persists every transaction record. Their response contracts distinguish success from failure. | Define whether these tables represent attempts or accepted transactions. If accepted transactions, filter by documented success; otherwise record explicit attempt/outcome semantics and ensure consumers do not treat failures as accepted. |
| Medium | Shared `get_nse_client()` and authentication already exist, but most routers duplicate HTTP/JSON error handling. `raise_for_nse_error()` and `handle_nse_request_error()` are used by only part of the code. | Introduce a shared JSON transport function and a separate download function. Preserve response envelopes, timeouts and status behavior; do not automatically retry financial mutations. |
| Medium | Several routers log full NSE response bodies, including SIP and switch responses, and shared misc helpers log body excerpts. Responses contain client and transaction data. | Log operation, status, counts and redacted identifiers rather than response bodies. |
| Low | `main.custom_openapi()` applies Bearer security to every documented operation, including login and health, and labels JWT bearer format as `BASIC`. Runtime authentication is JWT via `require_auth`; NSE Basic authorization is internal. | Document local JWT security accurately and keep public login/health operations public in OpenAPI. |

## Items requiring external confirmation or deeper contract review

- **NFT single-bank endpoint:** the NFT master on p. 179 assigns `COM` to Change of Bank and `COA` to Change of Multiple Banks. The single-bank section on p. 217 instead prints `/NFT/COA`. Code uses `/NFT/COM`. This is an internal specification conflict, not a confirmed missing implementation. Obtain NSE clarification or retain verified UAT evidence before changing it.
- **Encryption interoperability:** pp. 5-6 specify AES-128 and `base64(iv::salt::aes_encrypted_val)` but do not define the complete cipher/padding/key derivation procedure. Code uses AES-CBC/PKCS7, a hex-decoded license key, and a generated salt that does not affect encryption. Confirm against an NSE reference implementation; do not invent a key derivation change from the PDF alone.
- **PDF inconsistencies:** examples contain malformed JSON, inconsistent whitespace and some contradictory conditional rules (for example KYC report filters on p. 164). Preserve exact wire keys where evidenced, and record unresolved conflicts rather than treating every sample as executable JSON.
- **Version changes:** fully compare v1.9.8 UCC, STP, provisional/order-status and member fund allocation fields listed on p. 238. Some recent fields already exist (`member_unique_id`, goal-based SIP fields, report filters); their presence alone does not verify behavior.
- **Reports:** many responses use generic dictionaries or `Any`. Validate actual envelope types, failure envelopes, totals and date/filter precedence. Master download is a file response on success and JSON on failure (p. 163).
- **Database failure after NSE acceptance:** orders explicitly warn against retry after persistence failure, while other mutation routes return generic save errors. Define reconciliation consistently and use member unique IDs where documented. A database upsert does not by itself prevent a second NSE submission.

## Proposed organization

Keep existing `/api/v1` paths stable during the refactor. Feature ownership and internal modules can change independently of public URLs and database table names.

| Feature package | Existing modules to organize there |
|---|---|
| `clients` | UCC, bank details, KYC, FATCA, AOF, cheque, POA, NFT, communication |
| `orders` | Purchase/redemption, switch, order cancellation |
| `systematic` | SIP, XSIP, STP, SWP registrations, cancellations, top-ups, UMRN mapping, modifications and pause operations |
| `mandates` | Mandate registration and image upload |
| `payments` | Purchase payment, UPI status and UTR update |
| `reports` | Status, client, transaction, statements, fund allocation and systematic reports, including pause reports |
| `masters` | Scheme, NAV and settlement calendar download |
| `auth` / shared NSE integration | Local JWT login/security; separately, NSE credentials, header generation, upstream configuration and HTTP transport |

Suggested internal layout:

```text
features/
  clients/       # router.py, schemas.py, service.py as needed
  orders/
  systematic/
  mandates/
  payments/
  reports/
  masters/
integrations/nse/ # authentication, transport, endpoint constants
auth/            # local application authentication
models/          # preserve current tables during initial refactor
main.py          # middleware, lifecycle, feature router mounting
```

Split the mixed `routers/misc_services.py` and `schemas/misc_services.py` across feature owners. Move master download out of miscellaneous reports. Initially retain existing model import paths and database table names; moving code does not require a database schema migration.

## Implementation sequence and acceptance checks

1. Capture the current mounted method/path list, authentication requirements and response models as a compatibility baseline. Add an offline test harness with fake settings and mocked NSE/database dependencies; avoid importing startup into tests that create real tables.
2. Fix order persistence, the KYC contract and report URL casing with targeted mocked tests. Cover both successful and failed NSE envelopes, and database failure after upstream acceptance.
3. Add request validation per operation: required/conditional fields, allowed values, batch limits, date formats and ranges, identifiers and precision. Test valid and invalid cases from documented rules; master-dependent checks require downloaded scheme data.
4. Extract shared JSON and file transport behavior. Verify 403, timeout, connection failure, malformed JSON, JSON business failure and binary/text file download separately. Avoid automatic retries of mutations.
5. Move routes and schemas by feature, then slim `main.py` to a router registry. Compare the resulting mounted routes against the baseline, including hidden diagnostics and authentication dependencies.
6. Retire ELog upload under an explicit compatibility policy and resolve the NFT/encryption ambiguities using NSE evidence. Run read-only UAT checks first; run transaction acceptance checks with dedicated test data in the configured UAT environment.

## Verification performed

- Compared the mounted router list in `main.py` with existing modules; inspected route decorators and upstream constants across the router directory.
- Matched upstream URL strings to API PDF pages, manually checked wrapped securities-delivery URL and spaced KYC/NFT URLs, and identified the COA/COM conflict.
- Inspected request schemas, response handling, shared authentication/transport, representative database persistence, and the latest changelog.
- Existing `test_api.py` calls an external server and includes mutating operations; it was not executed as an offline audit test. Existing smoke checks also contact external services.
- At the initial audit, sandboxed Python launchers could not start. A subsequent test run used Python outside the sandbox: see [test results](NSE_API_TEST_RESULTS.md) for the offline failures and the skipped live UAT check.

## Webfile reference boundary

Use the API PDF as the contract and scope authority. No Member Desk bulk-upload workflow is required for this backend. Keep `NSE_MF_WebfileStructure.pdf` available as a supporting reference for master codes or pipe-delimited download layouts when needed; API delivery can still return files, especially MASTER_DOWNLOAD on p. 163. Removing webfile workflows does not mean removing API-based master downloads.
