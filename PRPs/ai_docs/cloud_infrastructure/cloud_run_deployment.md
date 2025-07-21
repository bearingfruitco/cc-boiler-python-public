# Google Cloud Run: Deployment, Integration, and Best Practices

## Overview of Google Cloud Run

Google Cloud Run is a fully managed, serverless platform for running containerized applications. It automatically handles provisioning, scaling, and infrastructure management, so you can focus on your code. Key characteristics of Cloud Run include:

* **Containerized Workloads:** You package your Python agent in a container image. Cloud Run can then run it on demand in response to HTTP requests or events. This means you can use any web framework (Flask, FastAPI, etc.) or even just a simple HTTP server in Python.
* **Scalability:** Cloud Run scales **from zero to N** instances based on traffic. If no requests come in, it can scale down to zero (no cost when idle). Under load, it can spin up multiple container instances (by default up to 1000 concurrent instances, adjustable) to handle traffic.
* **Concurrency:** By default, each Cloud Run container instance can handle up to 80 concurrent requests. This can be adjusted (even down to 1 if you prefer each instance to handle one request at a time for simplicity or thread-safety). Higher concurrency can improve efficiency but requires your code to be thread-safe.
* **Stateless and Ephemeral:** Cloud Run instances are stateless. Any instance may be terminated when idle, and local state (files, memory) does not persist across requests or across different instances. Use external storage (Cloud Storage, databases, etc.) for stateful needs. Also plan for **cold starts** – when a new instance starts, there may be a short startup latency. You can mitigate this by specifying a minimum number of warm instances if needed (at the cost of always-on billing).
* **Triggers:** Cloud Run services are invoked via HTTP requests by default (each service gets a HTTPS URL). You can integrate with other trigger types using EventArc and Pub/Sub. For example, Cloud Run can be triggered by Pub/Sub messages, Cloud Scheduler (for cron jobs), or Cloud Events (like Cloud Storage or BigQuery events) via EventArc. We'll discuss trigger methods in detail later.

Overall, Cloud Run is ideal for building an **API or webhook handler service** (like your AI agent) that needs to interact with databases and external APIs, scaling automatically with load and requiring minimal ops maintenance.

## Deploying Cloud Run Services (Source vs. GitHub vs. Container Image)

There are multiple ways to deploy your Python agent to Cloud Run. The main approaches are:

* **Build and Deploy from Source:** You can have Cloud Run build your code into a container image using buildpacks. For example, using the gcloud CLI or Cloud Console, you can point to your source code (in a Git repo or local directory) and let Google Cloud build the container automatically. This is convenient for quick deploys (Cloud Run will generate a Dockerfile or use buildpacks for you).
* **Deploy a Pre-Built Container Image:** Alternatively, you can build the Docker image yourself (using a `Dockerfile`) and push it to a registry (Google Artifact Registry or Container Registry). Then provide that image URL to Cloud Run. This gives more control over the environment (you define the Python runtime, installed packages, etc. in the Dockerfile). It's slightly more work upfront but often preferred for complex apps.
* **Continuous Deployment from GitHub:** Yes – you can (and likely should) integrate Cloud Run deployment with GitHub for CI/CD. Cloud Run can be connected to your GitHub repo so that on each push, an automated build and deploy occurs (using Cloud Build or GitHub Actions). This ensures your Cloud Run service is always up-to-date with your code. Many teams use **GitHub Actions** workflows to build the Docker image and deploy to Cloud Run on each commit. This is generally a best practice once your project grows beyond quick experiments.

**Should you deploy from GitHub?** For a production system with a team, using GitHub-based CI/CD is highly recommended. It provides version control, code review, and an automated trail of deployments. You mentioned possibly using GitHub Actions – that's a great choice. Google provides an official GitHub Action called **`google-github-actions/deploy-cloudrun`** that can deploy a service to Cloud Run (from a container image or from source). For secure authentication, you'd typically set up Workload Identity Federation so that the GitHub Action can act as a Google service account without needing JSON key credentials. This requires a one-time setup of a workload identity pool and assigning roles to a service account, but it avoids storing sensitive keys in GitHub. The service account used by CI/CD will need roles like **Cloud Run Admin, Artifact Registry Writer, and Service Account User** in your project (these allow it to deploy new revisions).

In contrast, manual deploys (e.g. using the `gcloud run deploy` command from your machine for each update) can work for prototypes or very small projects, but they don't scale well for collaboration or frequent updates. Manual deploys risk configuration drift and rely on developers to run the commands each time. Therefore, **deploying via an automated pipeline from GitHub is usually the better approach** for consistency and reliability.

**Deployment process overview:** If you go with GitHub Actions, your flow might be: push code -> GitHub Action builds Docker image (using Docker or Cloud Build) -> pushes image to Artifact Registry -> deploys to Cloud Run. The Cloud Run service gets updated to the new image. You can set this up to deploy to a staging service first, run tests, then deploy to production, etc., depending on your needs (Cloud Run supports traffic splitting between revisions for canary releases as well).

When deploying, you'll choose a **region** (e.g. `us-central1` or wherever closest to your data/users) and a **service name**. Cloud Run will give your service a default domain like `https://<service>-<project>-<region>.run.app`. You can also map a custom domain if needed later.

**Allowing Public Access:** Since your use case involves webhooks and external systems (LeadProsper, API partners, etc.) calling your service, you will likely want to allow **unauthenticated invocations** (public URL). By default, Cloud Run services require authentication via IAM (meaning only callers with a valid Google identity or service account token can invoke). You can disable that requirement to make the endpoint public. For example, when creating the service via console or gcloud, you'd choose "Allow unauthenticated invocations". This effectively grants the special `allUsers` principal the Cloud Run Invoker role on your service, making it reachable by anyone who knows the URL. (If you *don't* want it fully public, you can instead require authentication and only give specific service accounts or users the Invoker role – but for generic webhooks from external systems, that's usually not feasible, so public is easier).

**Containerizing the Python Agent:** Ensure your agent code is structured to run as a web service. For example, if using Flask: define some endpoints (for different webhook routes or functions), and in Dockerfile start the Flask app with a production server (Gunicorn) listening on port \$PORT (Cloud Run sets the container's port via `$PORT` env var). If not using a framework, you could use Python's built-in HTTP server or FastAPI, etc. The container just needs to listen for HTTP and handle requests. Cloud Run will pass incoming HTTP requests to your container.

A simple Python Dockerfile might look like:

```Dockerfile
FROM python:3.11-slim  
WORKDIR /app  
COPY . /app  
RUN pip install -r requirements.txt  # install your dependencies  
ENV PORT=8080  
CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "myagentapp:app"]  # example for Flask app
```

You can adjust based on your app structure. The key is to listen on `0.0.0.0:$PORT`. Cloud Run will route traffic to that port.

## Service Configuration and Settings

When deploying to Cloud Run, you have many configurable settings. Here are the important ones and recommended values for your scenario:

* **Memory and CPU:** By default, a Cloud Run container has 256 MiB of memory and 1 vCPU. You can increase this up to 8 GiB and 4 vCPUs if needed. For a Python agent handling potentially many requests and doing database work, you might want to start with say **512 MiB memory and 1 CPU**, and adjust based on performance. If you do heavy data processing in-memory or large responses, increase memory accordingly.
* **Concurrency:** As mentioned, you can limit concurrency per instance. If your code and libraries are thread-safe and you want to save cost, you can allow >1 concurrency (default 80). This means a single container instance can handle multiple requests in parallel (threads or async). However, if your agent will perform a lot of CPU-bound work for each request (or you want simpler sequential logic), you might set concurrency to 1. This guarantees one request at a time per instance, effectively isolating each request but possibly requiring more instances under load. Evaluate this based on how your agent code behaves.
* **Timeout:** Cloud Run allows each request to run for up to 60 minutes (3600 seconds) now. The default is often 5 minutes if not changed. You should set an appropriate timeout for your requests. For webhooks or API calls, usually a short timeout (a few seconds up to maybe 30s) is ideal so clients aren't waiting forever. For longer background processing, you could extend it. Make sure external callers (like LeadProsper or partners) have matching timeouts – no point in Cloud Run allowing 5 minutes if the caller will give up after 30 seconds. In general, keep it as low as practical to detect hung requests.
* **Auto-scaling settings:** Cloud Run will scale instances automatically. You can optionally set **minimum instances** > 0 to keep some warm instances always ready (reducing cold start latency). You can also set **maximum instances** to control cost or rate limiting. For example, if you wanted to ensure at most 10 concurrent instances (maybe to not overwhelm a database), you can set max instances to 10. In your case, if many webhooks may come in concurrently, ensure the database can handle it or put a reasonable cap.
* **Ingress settings:** By default, ingress is "all" (allows traffic from anywhere, including internet). You can restrict to internal (only allow calls from within your VPC or Google Cloud), but since external services will call this, **keep ingress as "all"**.
* **VPC Connectivity:** If you need to access internal resources or use a fixed egress IP, you can attach a Serverless VPC Connector. For example, if your Supabase database required a specific outbound IP (for whitelisting) or if you needed to reach a private network, a VPC connector is useful. It allows your Cloud Run service to send outbound traffic through your VPC (and through Cloud NAT for a static IP). If Supabase is just open on the internet (with host/port and password), you might not need this. But keep in mind, Cloud Run's outbound IPs are not fixed unless you use a VPC connector with Cloud NAT. Check Supabase's settings; if they offer IP whitelisting and you want to secure the connection, you could set up a VPC connector. Otherwise, ensure your Supabase is configured to allow external connections (it usually is, via SSL).
* **Environment Variables:** Use environment variables to configure your service. Cloud Run makes it easy to set env vars either via the UI, gcloud flags, or YAML. For example, store your database connection strings, API keys (Supabase anon or service keys, etc.), and other config in env vars. You can even mount certain secrets via Secret Manager (which we'll touch on). But at minimum, avoid hardcoding credentials in code – inject them via env vars so they can be changed per environment.

## Database Integration (BigQuery and Supabase)

Your agent will interact with both **BigQuery** (a Google Cloud data warehouse) and **Supabase** (a hosted Postgres database). Here's how to integrate each:

**1. Google BigQuery (GCP Data Warehouse)**
BigQuery is not a traditional OLTP database – it's a analytics warehouse. It can handle huge datasets but has usage patterns and quotas (e.g. streaming inserts, query jobs). For integrating Cloud Run with BigQuery:

* **Use the BigQuery Python Client:** Google provides the `google-cloud-bigquery` Python library. It allows you to run SQL queries, stream inserts, etc., using your Cloud Run service account credentials automatically. In Cloud Run, authentication to GCP services works via **Application Default Credentials (ADC)** – since the code is running as a GCP service account, the BigQuery client can pick that up. For example, you can do:

  ```python
  from google.cloud import bigquery
  client = bigquery.Client()  # uses ADC credentials of the service account
  table_ref = client.dataset("mydataset").table("mytable")
  errors = client.insert_rows_json(table_ref, [{"name": "Alice", "score": 90}])
  if errors:
      logging.error(f"BigQuery insert errors: {errors}")
  ```

  This would stream a JSON row into BigQuery. Alternatively, you can assemble an SQL query and call `client.query(sql)` to run it. The key is that your Cloud Run service's identity must have the right permissions in BigQuery (more on that below).

* **Service Account Permissions for BigQuery:** Make sure the Cloud Run service's IAM service account has appropriate BigQuery roles. To **read/write data** in BigQuery, you typically need to grant at least:

  * **BigQuery Data Editor** on the specific dataset (or project) – this role allows read and write of table data. It includes permissions to create new tables, insert data, and read rows in that dataset.
  * **BigQuery User** (or Job User) at the project level – this allows the service account to run query jobs (which BigQuery executes in the background). In BigQuery, running queries or load jobs requires the ability to create jobs. For instance, *roles/bigquery.user* includes permission to create query jobs (bigquery.jobs.create).

  Essentially, give your service account *BigQuery Job User* permission to create queries, and *BigQuery Data Editor* (or Viewer if only reading) on the datasets it needs to use. This principle is outlined in Google's docs and community answers: the Cloud Run service account needs BigQuery IAM roles to run jobs and access data. Without these, you'd get "access denied" errors when trying to use BigQuery.

* **Networking:** BigQuery is a Google service accessed over Google's internal network. Your Cloud Run service just needs to have the BigQuery API enabled on the project (which it likely is). No special networking needed since it's all within GCP.

* **Performance considerations:** If you are doing frequent small inserts into BigQuery (e.g., for each webhook event), note that BigQuery's streaming inserts are eventually consistent and have a rate cost. BigQuery can handle hundreds of thousands of streaming inserts per minute, but each insert is slightly pricey. If the volume is huge, you might buffer data and load in batches (or consider an intermediary like Pub/Sub). For moderate volumes, direct inserts as shown above are fine.

* **Error handling:** Wrap BigQuery calls in try/except and log errors. For example, if `client.insert_rows_json` returns errors (list of errors per row), log them. If a query job fails, catch the exception. You can use Error Reporting (which we cover later) to track BigQuery exceptions as well.

**2. Supabase (Postgres) Databases**
Supabase is essentially a hosted PostgreSQL with extras. Integrating Cloud Run with Supabase is similar to using any external Postgres database:

* **Connection method:** You have two main options to talk to Supabase:
  a. **Using Supabase client libraries or REST:** Supabase provides client libraries (JS, maybe Python) and a RESTful API. For example, supabase's REST API (via PostgREST) can be called with the supabase URL and an API key. In Python, you could use the `requests` library to call those endpoints.
  b. **Direct Postgres connection:** You can connect to the Supabase Postgres directly using psycopg2 or SQLAlchemy. Supabase gives you a connection string or host, port, user, password, and SSL requirements. For Python, you'd likely use `psycopg2` or `asyncpg` to connect and run SQL. This might be more flexible for complex queries.

* **Credentials:** Store the Supabase connection URL and service key in environment variables. Supabase typically provides an `API URL` and an `anon key` (for client access) and a separate `service role` key for admin access. Use the service role key on your backend if you need to bypass RLS or perform privileged operations. If you connect at the Postgres level, you'll use the database credentials (user/password). These are definitely secrets – do not hardcode them. You might use **Secret Manager** to manage them and have Cloud Run load them as env vars securely.

* **Network and Security:** Supabase is external to GCP, accessed over the public internet (unless you're running Supabase in a GCP VPC, but likely not). Ensure your Cloud Run has internet access (it does by default unless you severely restrict egress). If Supabase has IP whitelisting and you want to secure it, you'd need to use a VPC connector with static egress IP as discussed. Otherwise, just ensure you use SSL (Supabase requires TLS for DB connections by default).

* **Connection pooling:** A potential issue with serverless + Postgres is managing DB connections. Each Cloud Run instance will open a new connection to Postgres. If your traffic spikes and Cloud Run scales to many instances, you could overwhelm the DB with connections. Supabase might have connection limits. To mitigate this, enable connection pooling if Supabase offers it, or use a pooling proxy like PgBouncer (Supabase might have it built-in on the cloud side). At a code level, make sure to close connections when not in use, or use a global connection pool object rather than reconnecting every request. Given Cloud Run instances are reused for multiple requests, you can initialize a DB connection pool on startup and reuse it. For example, if using SQLAlchemy, create the engine globally when the container starts (outside the request handler) so that connections are reused.

* **Supabase usage:** If using the Supabase JS/Python client (which wraps the REST API), it often needs the Supabase URL and anon/service key. That would allow you to call Supabase's insert/select functions easily. Alternatively, using direct SQL gives you full power of Postgres (you might prefer SQL for complex joins or using Supabase's Postgres extensions). Either approach can work; just keep the logic consistent and handle errors (DB errors, constraint violations, etc.).

* **Example:** If using psycopg2, something like:

  ```python
  import psycopg2
  conn = psycopg2.connect(os.environ["SUPABASE_CONN_URL"])
  cur = conn.cursor()
  cur.execute("INSERT INTO leads(name,email) VALUES(%s,%s)", (name, email))
  conn.commit()
  cur.close()
  ```

  If using the Supabase client library (supabase-py), it would be more abstracted. Choose whatever you and your team are comfortable with.

## Webhook and Event Handling

Your agent may need to **receive data from** and **send data to** various external systems: LeadProsper webhooks, affiliate postback URLs, partner APIs, n8n automation triggers, Telegram/Discord notifications, etc. Cloud Run can handle all of these since it can both serve HTTP and make outgoing HTTP requests:

* **Receiving Webhooks/HTTP calls:** For each external system that needs to send data in, you'll expose an endpoint on Cloud Run. If you use a framework like Flask, you might create distinct routes (e.g. `/leadprosper_webhook` and `/partner_ping` etc.) to handle different payload formats. Alternatively, a single endpoint could inspect the payload or headers to distinguish sources. It's often cleaner to separate them. Ensure you document these endpoints (method, expected auth or params) so that the external systems are configured correctly.

  * *Authentication & Security:* Many webhooks have an option to include a secret or token (e.g., a signature, or a known parameter) so you can verify the request is legitimate. If possible, use this. For instance, if LeadProsper can add a shared secret in the URL or an HMAC signature, have your code verify it before processing. This prevents random internet traffic from hitting your endpoint and confusing the agent. If no built-in mechanism, at least use an unguessable URL path.
  * *Idempotency:* Sometimes webhooks might retry or send duplicates. It's wise to guard against processing the same event twice (perhaps by using an unique ID in the payload). Ensure your database operations can handle duplicates or use a de-dup logic if needed.
  * *Response:* Cloud Run will need to respond within a reasonable time. For webhooks, usually a 200 OK indicates success. If you need to do heavy processing, you might quickly queue the work (e.g., publish to Pub/Sub or push to a background task) and immediately return 200 to acknowledge receipt, then do the processing asynchronously. This way the external system isn't kept waiting.

* **Outgoing HTTP calls:** Your agent might need to call external APIs (Supabase REST, n8n webhook URLs, Telegram bot API, Discord webhook URLs, etc.). Cloud Run allows outgoing requests freely (with internet egress). A few points:

  * Use the Python `requests` library or an async equivalent to make calls. Set reasonable timeouts on these calls (so your agent doesn't hang forever if an external service is down).
  * Handle HTTP errors and transient failures. If a call to an external service fails (network error or non-200 response), decide on a retry policy. You might catch the exception and retry a few times, or if it's non-critical, log an error and move on. Don't let the entire Cloud Run request crash due to one failed outgoing call – handle it gracefully (perhaps return an error status to the initial caller if that's appropriate, or just log it if it was a background notification).
  * **Webhook to n8n/Make.com:** If you want to trigger n8n or Make (Integromat), you'll likely call a webhook URL that those services provide. Just treat it as a POST request in your code. If it's critical to ensure the workflow runs, implement retries or have n8n send a response back.
  * **Telegram/Discord notifications:** You can integrate with these directly. For example, Telegram has a Bot API where you send an HTTP POST to `https://api.telegram.org/bot<token>/sendMessage` with chat ID and text. You could code that in your agent to send yourself or a group a message (for alerts or info). Discord webhooks have a specific URL to POST JSON payloads to a channel. These are straightforward HTTP calls. Again, secure the tokens and URLs (store as secrets) and handle errors (e.g., catch exceptions if the message send fails, maybe log and continue).

## Logging and Monitoring

Robust logging is crucial for visibility into your agent's behavior, especially since you want this to be easily understandable by both humans and AI agents. Cloud Run is automatically integrated with **Google Cloud Logging (Stackdriver Logging)**. All `stdout` and `stderr` output from your container is collected as logs. Here's how to leverage this:

* **Use Structured Logging:** Instead of just printing plain text, consider logging in **structured JSON** format. This allows Cloud Logging to parse fields (like severity, event details) which you can filter on. Google's documentation provides examples of structured logging. For Python, you can simply print a JSON string. For instance, you might do:

  ```python
  import json, logging
  entry = {
      "severity": "INFO",
      "message": "Received lead payload",
      "source": "leadprosper",
      "lead_id": lead_id
  }
  print(json.dumps(entry))
  ```

  This will create a log entry with those fields. The special field `"severity"` will set the log level in Cloud Logging (so use `"ERROR"` for errors, etc.). You can include a trace or request ID if you have it, to correlate logs per request. Structured logs make it easier to query later (for example, you can query all logs where `source="leadprosper"`).

* **Standard Logging Practices:** Use `logging.info()`, `logging.error()`, etc., throughout your code to record key events. For instance, log when a webhook is received (maybe log the source and some identifier), log when you write to BigQuery ("inserted row into BQ"), log external API calls ("sent lead to partner X"), and log any exceptions or warnings. This will create a timeline in Cloud Logging that you can inspect. Make sure not to log sensitive data (PII or credentials) – mask or omit those. But do log enough to trace what happened.

* **Viewing Logs:** You can view logs in real-time in the Cloud Console (Logs Explorer), or use the `gcloud` CLI: for example, `gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=YOUR_SERVICE_NAME" --limit 100` will show recent logs. You can filter by severity (`severity>=ERROR` to see errors). This is useful for debugging when something goes wrong. The Cloud Run UI also has a "Logs" tab for each service where you can see logs correlated by request.

* **Error Reporting Integration:** Cloud Run automatically integrates with Cloud Error Reporting. If your code logs an exception stack trace to stderr or stdout, Error Reporting will aggregate it. For example, an uncaught exception that crashes your app (or a caught exception you manually log) will appear in Error Reporting with a stack trace. You can see a list of the top errors, how often they occur, etc., in the Error Reporting console. This is incredibly useful for catching issues over time.

* **Monitoring Metrics:** Cloud Run also emits metrics (like request count, latency, instance count). In Cloud Monitoring, you can set up dashboards or alerts. For instance, you could create an alert on "Cloud Run errors > X in 5 minutes" to notify you (perhaps via email or webhook). If you wanted to hook this into Telegram, you could have the alert call a Cloud Function or webhook that sends a Telegram message. There's some assembly required, but it's doable. Since you prefer Telegram for alerts, you might integrate via an intermediary (for example, an alert -> Pub/Sub -> your Cloud Run agent -> Telegram). This is an advanced setup; initially you might just watch the logs manually or have on-call alerts via email.

## Error Handling and Reliability

Error handling goes hand-in-hand with logging. The goal is to make the system resilient and debuggable. Here are best practices:

* **Gracefully handle exceptions:** Wrap database calls, network requests, and main logic in try/except blocks. Any anticipated failure (like a DB insertion failure, an API timeout, a KeyError in parsing input) should be caught. When caught, log the error with details. If appropriate, return a safe error response to the caller. For example, if a webhook call fails due to bad input, you might return HTTP 400 with a message. If an internal processing fails, you might return 500. But **do not crash the container** if you can help it. Unhandled exceptions will crash that request and possibly the container instance, leading to a cold start next time. It's better to catch the exception, log it, and let the request end gracefully.

* **Use HTTP response codes appropriately:** Cloud Run will return whatever your app responds with. So for external webhooks:
  * If you processed successfully, return 200 OK (or 201, 204 as fits).
  * If the input was invalid, return 400 Bad Request (with a message).
  * If an internal error happened (exception you couldn't recover from), return 500 Internal Server Error.
    These status codes help the caller know what happened. Some webhook providers will retry on certain responses (e.g., LeadProsper might retry if it gets a 500 from you, assuming it's a transient error). Check their docs; if they do retry on failure, ensure your code is idempotent (safe to run twice) to handle that.

* **Retries and Idempotency:** Cloud Run itself can retry requests in some cases. By default, if a container instance crashes or is overloaded, the request may be retried on another instance. You can configure maximum retries for your service (the default for HTTP is usually no retry on 4XX, but might retry on some 5XX). For outgoing calls (like to partner APIs), implement your own retry logic if needed. For example, if posting to Telegram fails due to a transient error, you might catch and retry after a few seconds. But also implement limits (don't retry forever).

* **Transaction handling:** When interacting with databases (BigQuery or Postgres), consider using transactions where appropriate. For BigQuery, if you have a sequence of operations, you might not have multi-step transactions (BigQuery is eventually consistent for streaming inserts, but you could use one big query with multiple statements if needed). For Postgres (Supabase), use transactions if you need to ensure atomicity across multiple statements. Catch exceptions like `psycopg2.IntegrityError` to detect issues like duplicate records.

## Security, IAM, and Permissions

Security is vital in your Cloud Run setup, especially since you deal with database credentials and external access. Let's break down a few areas:

**1. IAM for Cloud Run Service (Invoker Permissions):**
As discussed, if you want your Cloud Run service to be publicly accessible, you need to allow unauthenticated access. This is done by granting `roles/run.invoker` to `allUsers` on the service.

**2. Service Account Roles (for accessing GCP services):**
We created a dedicated service account for the Cloud Run service. Now we must assign IAM roles to that service account so that it can do what it needs:

* **BigQuery Access:** As mentioned, assign **BigQuery Data Editor** on the relevant datasets or project, and **BigQuery User** at the project level (for job run permissions).
* **Secret Manager (if used):** If you decide to store your Supabase credentials or other secrets in Google Secret Manager, you'd grant the service account **Secret Manager Secret Accessor** role on those specific secrets.
* **Cloud Storage or Other APIs:** If your agent will read/write files to Cloud Storage, give Storage roles (e.g., Storage Object Admin/Viewer on a bucket).
* **Pub/Sub:** If you integrate with Pub/Sub, there are multiple service accounts in play.

**3. Principle of Least Privilege:**
Grant your service account only the permissions it needs, and no more. For example, if the Cloud Run agent doesn't need to manage GCP resources, it shouldn't have Editor/Owner roles. Stick to specific roles like BigQuery User, etc.

**4. Encryption and Secrets:**
All traffic to Cloud Run is HTTPS, so inbound webhook data is encrypted in transit. For connecting to Supabase Postgres, use SSL. Store secrets (DB passwords, API keys) in Secret Manager or at least as env vars in Cloud Run. Avoid printing secrets in logs.

## Key Integration Points Summary

1. **Deployment:** GitHub Actions CI/CD recommended for production
2. **Configuration:** Use structured JSON templates for consistency
3. **Databases:** BigQuery for analytics, Supabase for operational data
4. **Webhooks:** Separate endpoints for different sources
5. **Logging:** Structured JSON logging for both human and AI readability
6. **Security:** Dedicated service accounts with minimal permissions
7. **Monitoring:** Cloud Logging, Error Reporting, and custom alerts