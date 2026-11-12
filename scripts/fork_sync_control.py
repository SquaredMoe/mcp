#!/usr/bin/env python3
"""Monitor all public forks owned by FORK_OWNER; optionally enroll new forks.

No repository code is deleted or force-pushed. Cross-repository writes require
the optional CROSS_REPO_PAT GitHub Actions secret.
"""
import base64
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

OWNER = os.environ.get("FORK_OWNER", "SquaredMoe")
PAT = os.environ.get("CROSS_REPO_PAT", "").strip()
TOKEN = PAT or os.environ.get("GITHUB_TOKEN", "").strip()
WORKFLOW_FILE = "sync-fork-upstream.yml"
WORKFLOW_PATH = ".github/workflows/" + WORKFLOW_FILE
REPORT = pathlib.Path("fork-sync-dashboard.md")
TEMPLATE = pathlib.Path(WORKFLOW_PATH).read_text(encoding="utf-8")
BASE_URL = "https://api.github.com"
NOW = dt.datetime.now(dt.timezone.utc)


def request(path, method="GET", body=None, write=False):
    """Return (HTTP status, decoded JSON); never print tokens."""
    token = PAT if write else TOKEN
    if write and not token:
        return 403, {"message": "CROSS_REPO_PAT is not configured"}
    url = BASE_URL + path
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "SquaredMoe-Fork-Sync-Monitor",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    payload = json.dumps(body).encode("utf-8") if body is not None else None
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            data = response.read()
            return response.status, json.loads(data) if data else {}
    except urllib.error.HTTPError as exc:
        try:
            error = json.loads(exc.read())
        except (ValueError, UnicodeError):
            error = {"message": "HTTP error"}
        return exc.code, error
    except (OSError, ValueError) as exc:
        return 0, {"message": str(exc)}


def repo_path(name):
    return "/repos/" + urllib.parse.quote(name, safe="/")


def list_forks():
    found = {}
    page = 1
    while True:
        status, repos = request(
            "/users/" + urllib.parse.quote(OWNER, safe="")
            + "/repos?type=owner&per_page=100&page=" + str(page)
        )
        if status != 200 or not isinstance(repos, list):
            raise RuntimeError("Cannot list repositories (HTTP " + str(status) + ")")
        for repo in repos:
            if repo.get("fork") and not repo.get("private") and repo.get("owner", {}).get("login", "").casefold() == OWNER.casefold():
                found[repo["full_name"]] = repo
        if len(repos) < 100:
            break
        page += 1
    return [found[name] for name in sorted(found, key=str.casefold)]


def generated_cron(name):
    number = int.from_bytes(hashlib.sha256(name.encode("utf-8")).digest()[:4], "big")
    hour = 4 + (number % 5)
    minute = (number // 5) % 60
    return f"{minute} {hour} * * *"


def add_workflow(name):
    scheduled = TEMPLATE.replace('23 4 * * *', generated_cron(name))
    # mcp's existing template uses a different cron; replace any schedule value.
    scheduled = re.sub(r'(cron:\s*")[0-9]+\s+[0-9]+\s+\*\s+\*\s+\*(")',
                       lambda match: match.group(1) + generated_cron(name) + match.group(2),
                       scheduled, count=1)
    content = base64.b64encode(scheduled.encode("utf-8")).decode("ascii")
    return request(repo_path(name) + "/contents/" + WORKFLOW_PATH, method="PUT",
                   body={"message": "ci: enable safe daily upstream sync",
                         "content": content}, write=True)


def time_str(value):
    if not value:
        return "—"
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return "—"


def investigate(repo):
    name = repo["full_name"]
    row = {"name": name, "parent": "—", "state": "Unknown",
           "last": "—", "detail": "", "link": f"https://github.com/{name}/actions/workflows/{WORKFLOW_FILE}"}
    base = repo_path(name)

    if repo.get("archived"):
        row["state"] = "🧊 Archived"
        return row

    status, metadata = request(base)
    if status == 200:
        parent = metadata.get("parent")
        if parent:
            row["parent"] = parent.get("full_name", "—")
        else:
            row["parent"] = "Original unavailable"
    elif status in (401, 403, 0):
        row["detail"] = "Cannot inspect upstream metadata"

    status, workflow = request(base + "/actions/workflows/" + WORKFLOW_FILE)
    if status == 404:
        file_status, _ = request(base + "/contents/" + WORKFLOW_PATH)
        if file_status == 404:
            if PAT and row["parent"] not in ("Original unavailable",):
                create_status, _ = add_workflow(name)
                if create_status == 201:
                    row["state"] = "🆕 Installed today"
                    row["detail"] = "Wait for GitHub to register the workflow"
                else:
                    row["state"] = "🔴 Install failed"
                    row["detail"] = "HTTP " + str(create_status)
            else:
                row["state"] = "🟠 Needs setup"
                row["detail"] = "Set CROSS_REPO_PAT to enroll automatically" if not PAT else "Original upstream unavailable"
        elif file_status == 200:
            row["state"] = "🟠 Not registered"
            row["detail"] = "File exists, but GitHub Actions has not registered it"
        else:
            row["state"] = "⚠️ Cannot inspect"
            row["detail"] = "Workflow file HTTP " + str(file_status)
        return row

    if status != 200:
        row["state"] = "⚠️ Cannot inspect"
        row["detail"] = "Workflow API HTTP " + str(status)
        return row

    state = workflow.get("state", "unknown")
    if state != "active":
        if PAT and state == "disabled_fork":
            enable_status, _ = request(base + "/actions/workflows/" + WORKFLOW_FILE + "/enable",
                                       method="PUT", write=True)
            if enable_status == 204:
                row["state"] = "🟢 Enabled today"
                row["detail"] = "Next scheduled sync is pending"
                return row
            row["detail"] = "Could not activate (HTTP " + str(enable_status) + ")"
        else:
            row["detail"] = "GitHub Actions workflow state: " + state
        row["state"] = "🟠 Disabled"
        return row

    runs_status, runs = request(base + "/actions/workflows/" + WORKFLOW_FILE + "/runs?per_page=1")
    if runs_status != 200:
        row["state"] = "⚠️ Runs unavailable"
        row["detail"] = "HTTP " + str(runs_status)
        return row
    latest = (runs.get("workflow_runs") or [None])[0]
    if latest is None:
        row["state"] = "⏳ Awaiting first run"
        row["detail"] = "Enabled but has no execution history"
        return row

    last_date = latest.get("run_started_at") or latest.get("created_at")
    row["last"] = time_str(last_date)
    row["link"] = latest.get("html_url") or row["link"]
    if latest.get("status") != "completed":
        row["state"] = "🔄 " + latest.get("status", "running").replace("_", " ").title()
    elif latest.get("conclusion") == "success":
        try:
            completed = dt.datetime.fromisoformat(last_date.replace("Z", "+00:00"))
            row["state"] = "🟠 Stale" if NOW - completed > dt.timedelta(hours=40) else "✅ Healthy"
        except (ValueError, AttributeError):
            row["state"] = "✅ Healthy"
    else:
        row["state"] = "🔴 " + str(latest.get("conclusion") or "Failed").title()
    return row


def clean(text):
    return str(text).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def main():
    forks = list_forks()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(investigate, forks))
    good = sum(row["state"].startswith("✅") for row in rows)
    problems = sum(row["state"].startswith(("🔴", "⚠️", "🟠")) for row in rows)
    waiting = len(rows) - good - problems
    mode = "Controller auto-enroll enabled" if PAT else "Read-only controller (ChatGPT daily task also attempts onboarding)"

    lines = [
        "# GitHub Fork Sync Dashboard",
        "",
        "> Automatically generated. **This report does not itself sync code.** Each fork's own GitHub Actions workflow performs synchronization.",
        "",
        f"**Last check:** {NOW.strftime('%Y-%m-%d %H:%M UTC')}  |  **Owner:** [{OWNER}](https://github.com/{OWNER})",
        "",
        f"**Public forks:** **{len(rows)}** &nbsp; · &nbsp; **Healthy:** **{good}** &nbsp; · &nbsp; **Needs attention:** **{problems}** &nbsp; · &nbsp; **Pending/other:** **{waiting}**",
        "",
        f"**New-fork discovery:** automatic &nbsp; · &nbsp; **New-fork installation:** {mode}",
        "",
        "## All forks",
        "",
        "| Fork | Upstream | Sync status | Latest run |",
        "|---|---|---|---|",
    ]
    for row in rows:
        link = row["link"]
        state = row["state"] + ((" — " + row["detail"]) if row["detail"] else "")
        lines.append(
            f"| [{clean(row['name'])}](https://github.com/{row['name']}) "
            f"| {clean(row['parent'])} | [{clean(state)}]({link}) | {clean(row['last'])} |"
        )
    lines += [
        "",
        "## How it works",
        "",
        "- **✅ Healthy:** last sync job passed within roughly 40 hours. It may have found nothing to update.",
        "- **⏳ Awaiting first run:** workflow is enabled, but has not yet executed.",
        "- **🔴 Failed:** open the linked workflow run to diagnose a merge conflict or permissions issue.",
        "- **🟠 Disabled or not registered:** enable Actions on that fork, or inspect its workflow settings.",
        "- **🧊 Archived:** never modified by this controller.",
        "- **Original unavailable:** your existing public fork is kept; no upstream updates can be fetched.",
        "",
        "### Automatic onboarding for future forks",
        "",
        "The monitor checks the owner's public repositories on every scheduled run. To also **install and enable**",
        "safe upstream syncing on newly forked public repositories, create a GitHub Actions repository secret",
        "named `CROSS_REPO_PAT` in `SquaredMoe/mcp`. It must be a fine-grained PAT covering all owned",
        "repositories (including future ones), with **Contents: read/write**, **Workflows: read/write**,",
        "and **Actions: read/write** permissions. Never commit or paste the token into a repository.",
        "For stronger isolation, host this controller in a dedicated, non-forked repository before granting",
        "an account-wide write token. Without the secret, new forks appear here as **Needs setup**",
        "until a separate automation installs their workflows.",
        "The existing daily ChatGPT GitHub Repository Sync task also attempts onboarding through the",
        "connected GitHub app; this depends on that connector having write permission.",
        "",
        "### Notes",
        "",
        "- Each fork syncs separately on a staggered daily UTC schedule; the monitor only reports and enrolls.",
        "- Synchronization merges without force pushing. Conflicts stop the update without deleting your changes.",
        "- GitHub may disable scheduled workflows on inactive public repositories after 60 days.",
        "- This dashboard covers **public forks only**; private repositories are deliberately excluded.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Checked {len(rows)} public forks; healthy={good}; needs_attention={problems}; pending={waiting}")
    for row in rows:
        if row["state"].startswith(("🔴", "⚠️", "🟠")):
            print(row["name"] + ": " + row["state"] + (" — " + row["detail"] if row["detail"] else ""))


if __name__ == "__main__":
    main()
