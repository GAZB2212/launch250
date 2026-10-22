# Prospecting: build-first outreach

Find a local business with no website, build it one, email them the preview,
sell it for £250. Five a day.

```
 find (06:00 weekdays)      build (you, 10 min)        send (admin page, or Astra)
 launch250-prospect-find -> launch250_prospects   ->  prospect/build.py   ->  preview.launch250.co.uk/<slug>/
 Google Places, no website    status: found           prospects/<slug>/       status: built -> sent
 + public email hunt          (or no_email)           commit + push           reply -> won / lost
```

Everything meets in one Supabase table, `launch250_prospects`, which is also
the bridge to any outside marketing agent (see "Working with Astra").

## The pieces

| Piece | Where | What it does |
|---|---|---|
| Finder | Supabase function `launch250-prospect-find`, cron weekdays 06:00 | Searches Google Places for `<trade> in <town>` from the rotating plan in `launch250_settings.prospect_plan`, keeps businesses with **no website** and a phone number, hunts for a public email (DuckDuckGo and Bing snippets, the top result pages, Yell), stores them. Needs the `GOOGLE_MAPS_KEY` secret. |
| Builder | `prospect/build.py` (this repo) | Turns a prospect row into a full preview site under `prospects/<slug>/` using a demo's design and trade copy from `prospect/trades.py`. Also writes the email it expects to go out. |
| Preview host | Netlify site `launch250-prospects`, publish dir `prospects`, domain `preview.launch250.co.uk` | Serves the committed previews. Every page is noindex. |
| Sender | Supabase function `launch250-prospect-send` | Sends the outreach email via Resend from hello@launch250.co.uk. Called from the admin page's **Send the email** button. |
| API | Supabase function `launch250-prospect-api` | Add prospects, list them, fetch the exact email text, update status. Secured by a shared key. This is what Astra uses. |
| Admin | launch250.co.uk/admin.html, Prospects section | See everything, change status, add notes, send. |

## Daily routine (about ten minutes)

```
export SUPABASE_URL=https://hffwugpulmerckzqzjfv.supabase.co
export SUPABASE_SERVICE_KEY=...        # Supabase -> Project Settings -> API -> service_role (never commit it)

python3 prospect/build.py pull         # today's finds -> prospect/queue/*.json
python3 prospect/build.py build --all  # builds prospects/<slug>/ for each
# open a couple locally and sanity-check: python3 -m http.server 8777 then /prospects/<slug>/
git add prospects && git commit -m "Previews for <date>" && git push
python3 prospect/build.py mark <slug>  # for each one you are happy with: status -> built, preview_url set
```

Then on the admin page each one shows **Send the email**. Read the preview
first. If a name split badly or the trade is wrong, fix `content.json` in
`prospects/<slug>/`, rebuild with `build`, push again.

`build` works offline from the queue file, so you can also hand-write a queue
file for a business you found yourself (copy `prospect/queue/example-plumbing-heswall.json`).

## Setting up (once)

1. **Google Places.** Google Cloud Console -> create a project -> enable *Places API (New)* -> create an API key restricted to that API. Put it in Supabase -> Edge Functions -> Secrets as `GOOGLE_MAPS_KEY`. Text Search is billed per request; five prospects a day is a few pounds a month at most, and Google gives a monthly free allowance.
2. **Preview host.** Netlify -> Add new site -> Import from Git -> this repo. Base directory `prospects`, publish directory `prospects`, no build command (the `netlify.toml` in that folder sets the noindex headers). Domain management -> add `preview.launch250.co.uk` and the CNAME at the registrar.
3. **Service key** on the machine that runs `build.py` (see the routine above). The anon key will not do; it cannot read the prospects table.
4. The plan: edit `prospect_plan` in `launch250_settings` (Supabase table editor) to change the trades, towns and how many a day.

## Working with Astra (or any outside agent)

The contract is the API. One header, four calls, plain JSON.

```
Base:   https://hffwugpulmerckzqzjfv.supabase.co/functions/v1/launch250-prospect-api
Header: x-prospect-key: <value of launch250_settings.prospect_api_key>
```

| Call | Body / query | Returns |
|---|---|---|
| `POST ?action=add` | `{"prospects":[{"name","town","trade","phone","email","address","maps_url","notes","source":"astra"}]}` (name and town required, up to 50) | `{"added":[{id,name,town,status}],"skipped":["name (reason)"]}` |
| `GET ?status=built` | any status or a comma list; omit for all | `{"prospects":[{id,name,town,trade,email,phone,status,preview_url,...}]}` |
| `GET ?action=email&id=<uuid>` | | `{"to","subject","text"}`: the exact email to send |
| `POST ?action=update` | `{"id","status":"sent","sent_by":"astra"}` or `{"id","status":"replied","notes":"..."}` | `{"ok":true}` |

Division of labour:

- **Astra finds and sends.** It adds prospects (ours finds too; duplicates by name and town are skipped), polls for `status=built`, pulls the email text, sends it from its own mailbox, and reports `sent`, then `replied` / `won` / `lost` / `opted_out` as the conversation goes.
- **This side builds.** Anything with status `found` gets a preview site and comes back as `built` with a `preview_url`.

Statuses, in order: `found` → `built` → `sent` → `replied` → `won` | `lost`. Side states: `no_email` (worth a phone call instead), `skipped`, `opted_out` (never contact again; delete the preview).

If Astra sends, keep `launch250-prospect-send` for the ones you want to send by hand; both mark `sent`, so nobody gets two.

## Rules we keep to

- **Only businesses with no website at all.** A bad website is a different pitch.
- **Only public business contact details.** The email we use is one the business has published itself, and the row records where it was found (`email_source`).
- **UK marketing law (PECR).** Unsolicited email to a limited company is allowed with an opt-out; to a sole trader or partnership it technically needs consent. Most tradespeople are sole traders. Every email carries a one-line opt-out and we honour it the same day (`opted_out`, preview deleted). Keep volume low and the message genuinely useful; that is also what makes it work.
- **Nothing of theirs on the preview that they did not publish.** Name, phone, hours and Google reviews are already public. Photos are our licensed trade photography, labelled as placeholders. We do not lift their Facebook photos or logo; we ask for them when they reply.
- **Pricing in the email is the website's pricing.** £250 build, hosting included for year one then £60 a year, domain bought in their own name, nothing to pay until the design is approved, then half and half.
