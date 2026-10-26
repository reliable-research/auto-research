# Protocol design

## Purpose

The protocol lets CLI, TUI, IDE, web, and automation clients drive the same research runtime without embedding workflow logic in a client.

Version 1 uses bidirectional JSON-RPC-style messages over newline-delimited JSON. The wire may later use WebSocket or a local socket while preserving method and event semantics.

## Connection lifecycle

Every connection follows:

```text
connect
  → initialize request
  → initialized notification
  → requests, responses, events, and server approval/input requests
  → graceful close
```

`initialize` includes client identity, supported protocol versions, optional event filters, UI form capabilities, and experimental feature opt-in. The response includes server version, supported schemas, platform, environments, and feature flags.

Requests before initialization fail. A second initialization on one connection also fails.

## Primitive mapping

The design adapts Codex's thread/turn/item model as follows:

- `project`: durable research objective, roots, policies, and memory;
- `thread`: interaction and steering history within a project;
- `workflowRun`: execution of one versioned scenario;
- `stage`: one declarative workflow transition;
- `attempt`: one agent invocation for a stage;
- `item`: streamed model, tool, command, patch, artifact, approval, or message event.

Threads remain useful for interaction. Workflow and evidence entities prevent scientific state from being reduced to conversation history.

## Stable methods

### Server and discovery

- `server/diagnostics`
- `schema/list`
- `agents/list`
- `agents/read`
- `agents/trust`
- `agents/disable`
- `skills/list`
- `tools/list`
- `workflows/list`
- `environments/list`

### Projects

- `project/create`
- `project/read`
- `project/list`
- `project/update`
- `project/archive`

Project creation takes an idempotency key. Archiving never deletes project files or run evidence.

### Threads

- `thread/start`
- `thread/resume`
- `thread/fork`
- `thread/read`
- `thread/list`
- `thread/interrupt`
- `thread/subscribe`
- `thread/unsubscribe`

A fork records its parent thread and optional boundary. It does not duplicate immutable artifacts; it references parent evidence and creates new writable state.

### Workflows and stages

- `workflow/start`
- `workflow/read`
- `workflow/list`
- `workflow/pause`
- `workflow/resume`
- `workflow/stop`
- `stage/read`
- `stage/retry`
- `stage/skip`
- `stage/approve`
- `stage/decline`

Skipping requires the workflow contract to mark a stage optional. A required failed gate cannot be bypassed by `stage/skip`.

### Attempts and execution

- `attempt/read`
- `attempt/list`
- `attempt/cancel`
- `command/exec`
- `command/write`
- `command/terminate`
- `job/read`
- `job/cancel`

Direct command execution is a utility and cannot mark a workflow stage complete.

### Evidence, artifacts, and memory

- `artifact/read`
- `artifact/list`
- `claim/read`
- `claim/list`
- `claim/promote`
- `claim/supersede`
- `evaluation/read`
- `evaluation/list`
- `memory/query`
- `memory/propose`
- `memory/review`
- `run/verify`

`claim/promote` and `memory/review` enforce project policy and may become server-initiated approval requests.

## Events

Events are immutable facts with `eventId`, timestamp, project/run scope, causation ID, correlation ID, payload schema version, and previous-event hash for audit-sensitive streams.

Core event families are:

- `project/*`: created, updated, archived;
- `thread/*`: started, resumed, forked, interrupted, closed;
- `workflow/*`: started, paused, resumed, stopped, completed;
- `stage/*`: ready, approvalRequired, started, evaluating, completed, blocked, failed, inconclusive;
- `attempt/*`: created, started, completed, failed, cancelled;
- `item/*`: started, delta, completed;
- `artifact/*`: recorded, verified, corrupt;
- `claim/*`: proposed, evidenceResolved, promoted, rejected, superseded;
- `evaluation/*`: started, completed, gatePassed, gateFailed;
- `memory/*`: proposed, reviewed, linked;
- `budget/*`: updated, warning, exhausted;
- `agent/*`: discovered, trusted, changed, quarantined;
- `approval/*`: requested, resolved, expired.

Clients treat completed item and stage events as authoritative. Streaming deltas are presentation data and are not replayed as scientific evidence unless captured in an artifact.

## Approval flow

A high-impact action follows:

```text
item.started
→ approval/request (server request)
→ client decision with granted subset and scope
→ approval.resolved
→ item.completed as completed, declined, cancelled, or failed
```

The request includes:

- project, run, stage, attempt, and item IDs;
- requesting agent identity and digests;
- action summary and reason;
- environment and working directory;
- requested filesystem, network, process, scheduler, secret, or publication permissions;
- available decisions;
- budget impact;
- whether session/run-scoped persistence is allowed.

The client returns only the granted subset. Anything omitted is denied.

## Structured user input

Agents and workflows may request structured input through a server request containing a JSON Schema and one of three behaviors:

- blocking decision required;
- optional input with a declared safe default;
- URL-based external authorization.

The client owns form rendering and must decline unsupported schemas rather than guessing.

## Example: start literature review

```json
{"method":"initialize","id":1,"params":{"clientInfo":{"name":"arch-cli","version":"0.1.0"},"protocolVersions":["1.0"]}}
{"method":"project/create","id":2,"params":{"idempotencyKey":"project-memory-review","name":"Memory review","roots":["/work/memory-review"]}}
{"method":"thread/start","id":3,"params":{"projectId":"prj_123"}}
{"method":"workflow/start","id":4,"params":{"projectId":"prj_123","threadId":"thr_123","workflowId":"literature-review","objective":"Compare durable memory mechanisms for research agents","controlMode":"copilot","budget":{"maxCostUsd":20,"maxWallSeconds":7200}}}
```

The server responds immediately with identifiers and then streams stage and item events.

## Example: artifact and claim events

```json
{"method":"artifact/recorded","params":{"projectId":"prj_123","runId":"run_123","stageId":"retrieve","artifactId":"art_17","sha256":"...","path":"artifacts/papers.json"}}
{"method":"claim/proposed","params":{"projectId":"prj_123","runId":"run_123","claimId":"clm_9","text":"Typed contradiction edges preserve negative knowledge.","evidence":[{"artifactId":"art_17","locator":"/papers/3/passages/8"}]}}
{"method":"evaluation/gatePassed","params":{"projectId":"prj_123","runId":"run_123","stageId":"citation-audit","evaluationId":"eval_22"}}
```

## Idempotency and recovery

Create and launch methods accept an idempotency key. Repeating the same request returns the original entity rather than starting duplicate jobs; reusing the key with different parameters returns a conflict.

Clients reconnect by:

1. initializing;
2. reading the project and workflow run;
3. subscribing from the last seen event cursor;
4. reconciling pending server requests;
5. resuming the thread or workflow when needed.

External jobs have a launch record before submission and a reconciler after restart. Unknown job state becomes `blocked`, never silently successful.

## Backpressure

Ingress and egress queues are bounded. Overload returns a retryable error with a retry hint. Clients use exponential backoff with jitter and idempotency keys.

Large command output and model deltas may be truncated in live events while the full content is stored as a hashed artifact under declared limits.

## Error model

Errors distinguish:

- invalid request or schema;
- not initialized or unsupported version;
- entity not found or conflict;
- policy or permission denied;
- approval declined or expired;
- budget exhausted;
- agent unavailable or changed;
- evaluator gate failed;
- adapter or environment failure;
- artifact integrity failure;
- server overload or transient transport failure.

Scientific negative results are not protocol errors. They complete with stage or workflow status `inconclusive`, `stopped`, or a valid negative claim set.

## Versioning

Stable methods and required fields change only in a new major protocol version. New optional fields and event types may appear in minor versions. Clients ignore unknown optional fields and may opt out of high-volume event families.

The runtime can generate JSON Schema and client types for the exact installed version.
