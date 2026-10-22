# Prospecting: build-first outreach

Find a local business with no website, build it a proper site, email them the
preview, sell it for £250. Five a day.

```
 find (06:00 weekdays)      build (07:30, Claude routine)      approve (you)        send (admin page, or Astra)
 launch250-prospect-find -> launch250_prospects   ->  prospect/craft.py          ->  admin page     ->  email with preview link
 Google Places, no website    status: found           own concept, palette, type,    built -> approved   approved -> sent
 + public email hunt          (or no_email)           Higgsfield photos, real reviews (or skipped)        reply -> won / lost
```

Every prospect gets a hand-built page. That is what they are buying, so there
is no template tier. The build is a Claude session (prospect/ROUTINE-PROMPT.md),
not a script, because each site needs art direction and copy written for that
business. prospect/craft.py holds every site's design as data and renders it;
prospect/shoot*.json hold the photo sets, one shoot per trade so a trade's sites
look like one photographer's work without paying for five shoots.

Everything meets in one Supabase table, `launch250_prospects`, which is also
the bridge to any outside marketing agent (see "Working with Astra").

## The pieces

| Piece | Where | What it does |
|---|---|---|
| Finder | Supabase function `launch250-prospect-find`, cron weekdays 06:00 | Searches Google Places for `<trade> in <town>` from the rotating plan in `launch250_settings.prospect_plan`, keeps businesses with **no website** and a phone number, hunts for a public email (DuckDuckGo and Bing snippets, the top result pages, Yell), stores them. Needs the `GOOGLE_MAPS_KEY` secret. |
| Builder | Claude routine (`prospect/ROUTINE-PROMPT.md`) using `prospect/craft.py` | Each weekday morning a Claude session writes a design entry for every new prospect (concept, palette, fonts, copy, real reviews), generates or reuses a Higgsfield photo set for the trade, renders `prospects/<slug>/`, pushes, and marks the row built. `prospect/build.py` keeps the `pull` and `mark` helpers and an old template builder that is no longer part of the flow. |
| Preview host | Netlify site `launch250-prospects`, publish dir `prospects`, domain `preview.launch250.co.uk` | Serves the committed previews. Every page is noindex. |
| Sender | Supabase function `launch250-prospect-send` | Sends the outreach email via Resend from hello@launch250.co.uk. Called from the admin page's **Send the email** button. |
| API | Supabase function `launch250-prospect-api` | Add prospects, list them, fetch the exact email text, update status. Secured by a shared key. This is what Astra uses. |
| Admin | launch250.co.uk/admin.html, Prospects section | See everything, change status, add notes, send. |

## Daily routine

Nothing to run. The 06:00 finder and the 07:30 Claude routine do the work. Your
part is the admin page: open each new preview, press **Approve design** or
**Reject**. Only approved prospects can be sent, by you (**Send the email**) or
by Astra.

To build by hand (a prospect you found yourself, or a rebuild): add its entry
to `SITES` in `prospect/craft.py`, run `python3 prospect/craft.py <slug>`,
commit and push `prospects/`, then mark it built in Supabase (the SQL is in
`prospect/ROUTINE-PROMPT.md`, or `python3 prospect/build.py mark <slug>` with
the two environment variables set).

## Setting up (once)

1. **Google Places.** Google Cloud Console -> create a project -> enable *Places API (New)* -> create an API key restricted to that API. Put it in Supabase -> Edge Functions -> Secrets as `GOOGLE_MAPS_KEY`. Text Search is billed per request; five prospects a day is a few pounds a month at most, and Google gives a monthly free allowance.
2. **Preview host.** Netlify -> Add new site -> Import from Git -> this repo. Base directory `prospects`, publish directory `prospects`, no build command (the `netlify.toml` in that folder sets the noindex headers). Domain management -> add `preview.launch250.co.uk` and the CNAME at the registrar.
3. **The Claude routine.** Create it at claude.ai/code under Routines with the prompt and settings in `prospect/ROUTINE-PROMPT.md`, ticking the Supabase, Higgsfield and GitHub connectors. Without it nothing gets built.
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

- **Astra finds and sends.** It adds prospects (ours finds too; duplicates by name and town are skipped), polls for `status=approved`, pulls the email text, sends it from its own mailbox, and reports `sent`, then `replied` / `won` / `lost` / `opted_out` as the conversation goes. It never sends anything merely `built`.
- **This side builds.** Anything with status `found` gets a preview site and comes back as `built` with a `preview_url`.

Statuses, in order: `found` → `built` → `approved` (you, on the admin page) → `sent` → `replied` → `won` | `lost`. Side states: `no_email` (built but nothing to email; approve it anyway and Astra will hunt for an address, or ring them), `skipped` (rejected), `opted_out` (never contact again; delete the preview).

If Astra sends, keep `launch250-prospect-send` for the ones you want to send by hand; both mark `sent`, so nobody gets two.

## Rules we keep to

- **Only businesses with no website at all.** A bad website is a different pitch.
- **Only public business contact details.** The email we use is one the business has published itself, and the row records where it was found (`email_source`).
- **UK marketing law (PECR).** Unsolicited email to a limited company is allowed with an opt-out; to a sole trader or partnership it technically needs consent. Most tradespeople are sole traders. Every email carries a one-line opt-out and we honour it the same day (`opted_out`, preview deleted). Keep volume low and the message genuinely useful; that is also what makes it work.
- **Nothing of theirs on the preview that they did not publish.** Name, phone, hours and Google reviews are already public. Photos are our licensed trade photography, labelled as placeholders. We do not lift their Facebook photos or logo; we ask for them when they reply.
- **Pricing in the email is the website's pricing.** £250 build, hosting included for year one then £60 a year, domain bought in their own name, nothing to pay until the design is approved, then half and half.
