# Insurance-Defense Budget Template Row Map

## Purpose

Capture the exact task-row inventory and output order from the sanitized budget
template so the runtime can emit a template-shaped JSON draft without checking
the workbook itself into the repository.

The workbook file remains outside this repository. This document is the
contract-side transcription of its row shape.

## Workbook Header Fields

Preserve these header fields in the JSON draft:

- `Client Name`
- `Client/Matter Number`
- `Matter Name`
- `Claim Number`
- `Total Budgeted ($)`

## Budget Column Order

Preserve these amount columns in this order:

1. `Original Budgeted Amount`
2. `Amount Billed to Date`
3. `Original Budget Amount Remaining`
4. `New Budgeted Amount`

## Summary Labels

Preserve these summary labels:

- `Original Budget:`
- `Updated budget:`

## Title And Notes

Preserve these workbook-level text surfaces in the JSON draft:

- title: `BUDGET FORM`
- instruction note: `Attorneys are only responsible for filling out the "Original Budgeted Amount" for initial budgets or "New Budgeted Amount for supplemental budgets."`
- footer note: `The accepted by carrier amounts are only accurate as of the date viewed in the ebilling portal.`

## Exact Phase And Task Inventory

### `L100` Case Assessment, Development and Administration

| Code | Label |
|---|---|
| `L110` | Fact Investigation / Development |
| `L120` | Analysis / Strategy |
| `L130` | Experts / Consultants |
| `L140` | Document / File Management |
| `L150` | Budgeting |
| `L160` | Settlement / Non-Binding ADR |
| `L190` | Other Case Assessment, Development and Administration |

### `L200` Pre-Trial Pleading and Motions

| Code | Label |
|---|---|
| `L210` | Pleading |
| `L220` | Preliminary Injunctions / Provisional Remedies |
| `L230` | Court Mandated Conferences |
| `L240` | Dispositive Motions |
| `L250` | Other Written Motions and Sanctions |
| `L260` | Class Action Certification and Notice |

### `L300` Discovery

| Code | Label |
|---|---|
| `L310` | Written Discovery |
| `L320` | Document Production |
| `L330` | Depositions |
| `L340` | Expert Discovery |
| `L350` | Discovery Motions |
| `L390` | Other Discovery |

### `L400` Trial Preparation and Trial

| Code | Label |
|---|---|
| `L410` | Fact Witnesses |
| `L420` | Expert Witnesses |
| `L430` | Written Motions and Submissions |
| `L440` | Other Trial Preparation and Support |
| `L450` | Trial and Hearing Attendance |
| `L460` | Post-Trial Motions and Submissions |
| `L470` | Enforcement |

### `L500` Appeal

| Code | Label |
|---|---|
| `L510` | Appellate Motions and Submissions |
| `L520` | Appellate Briefs |
| `L530` | Oral Argument |

### `E100` Expenses

| Code | Label |
|---|---|
| `E101` | Copying |
| `E102` | Outside Printing |
| `E103` | Word Processing |
| `E104` | Facsimile |
| `E105` | Telephone |
| `E106` | Online Research |
| `E107` | Messengers / Overnite |
| `E108` | Postage |
| `E109` | Local Travel |
| `E110` | Out-of-Town Travel |
| `E111` | Meals |
| `E112` | Court Fees |
| `E113` | Subpoena Fees |
| `E114` | Witness Fees |
| `E115` | Court Reporting & Transcripts |
| `E116` | Trial Transcripts |
| `E117` | Trial Exhibits |
| `E118` | Litigation, Support Vendors |
| `E119` | Experts |
| `E120` | Private Investigators |
| `E121` | Arbitrators / Mediators |
| `E122` | Local Counsel |
| `E123` | Other Professionals |
| `E124` | Other |

## Review Mapping Notes

For the first synthetic runtime implementation:

- every listed row must appear in the draft JSON even if its values are `0.0`
- unsupported or blocked cases may return a refusal or preflight packet instead
  of a final workbook-shaped draft
- no row or label in this map authorizes production budget assumptions
