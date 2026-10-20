# NSE backend test results

Date: 19 October 2026.

## Offline run

Command from the project root:

```powershell
py -3.11 scripts\run_offline_tests.py
```

Result: **22 passed, 10 failed**, with 3 warnings, in 1.68 seconds (pytest execution time). Python 3.11.9 was accessible outside the sandbox. Application code was not changed.

The runner selects only `test_auth_headers.py` and `tests/test_nse_spec_contract.py`, supplies dummy settings, and blocks external socket connections. Windows event-loop loopback sockets remain permitted. NSE requests and database sessions in route tests are mocked. No live credentials are used by this run, and it does not start the application's database-creating lifespan.

| Suite | Passed | Failed | Meaning |
|---|---:|---:|---|
| Existing mocked authentication/order suite | 22 | 3 | Most existing checks pass; three expectations differ from current behavior. |
| New v1.9.8 contract regressions | 0 | 7 | Reproduces the selected audit findings below. These failures remain open. |

New contract failures:

- Documented `TRXN SUCCESS` order response is not inserted into the mocked database.
- SIP accepts a detail object with no mandatory fields.
- STP accepts a detail object with no mandatory fields.
- `/registration/kyc-fresh-register` rejects documented camel-case KYC input with HTTP 422.
- Three report URL constants differ from the documented capitalization: 2FA, client authorization, order lifecycle. These tests verify specification matching, not whether NSE tolerates alternate casing.

Existing suite failures:

- Expects HTTP 502 for an oversized field in a failed NSE transaction; current behavior returns HTTP 200 with the failed transaction envelope. The desired response policy needs review.
- Expects persistence for `ACCEPTED`, which is not in the code's success-status set and is not the v1.9.8 order-entry sample's `TRXN SUCCESS` value. Update this fixture alongside the implementation fix.
- Expects persistence of failed transactions; current order persistence skips failed results. Decide whether these belong in a separate attempt/audit record rather than the accepted-orders table.

The first experimental run's network guard also blocked Python's internal socket pair. That harness issue was corrected before the reported final run; its setup failures are excluded from these results.

## Live connectivity

A guarded read-only NAV check was prepared for `nseinvestuat.nseindia.com`. It was **skipped because the configured hostname is not NSE UAT**. No NSE request was made and no live connectivity or authentication success is claimed. Credentials, tokens, and response data were not printed.

## Next work

Fix the confirmed contract gaps, review the three legacy test expectations, and rerun the offline command. For live acceptance, explicitly select the intended environment and dedicated test data. Start with a read-only master download before testing registrations, payments or orders.
