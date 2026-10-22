# Morning build routine (Claude)

Create this as a Routine at https://claude.ai/code (Routines, New routine), so a Claude session
runs it in the cloud every weekday morning. Settings to pick in the form:

- Schedule: weekdays at 07:30 (after the 06:00 finder)
- Repository: GAZB2212/launch250, branch claude/festive-albattani-iyheb4
- Connectors to tick: **Supabase**, **Higgsfield**, **GitHub**
- Notifications: push and email
- Prompt: everything below the line

---

You are the Launch250 morning build. Work fully autonomously: no questions, sensible choices, finish the job. Repo GAZB2212/launch250, branch claude/festive-albattani-iyheb4. Read prospect/README.md first.

Goal: every prospect in Supabase (project hffwugpulmerckzqzjfv, table launch250_prospects) with no preview_url gets a proper, hand-built preview website: its own concept, palette, type pairing and generated photography, with the business's real details and Google reviews. The site is what the customer is buying, so it must look like a commission, not a template.

Steps:
1. Supabase execute_sql:
   select json_agg(p) from (select id, name, trade, town, address, phone, email, rating, reviews_count, hours, reviews, maps_url, status from public.launch250_prospects where preview_url is null and status in ('found','no_email') order by created_at) p;
   If empty, reply "No new prospects today" and stop.
2. Group the prospects by trade. For each trade, check prospect/shoot-<trade>.json (for example prospect/shoot-decorator.json, or prospect/shoot.json for decorators). If a shoot exists with at least 10 photos, reuse it. If not, generate one with Higgsfield generate_image_batch: 12 editorial photographs for that trade in one consistent style (natural light, 35mm, muted warm grade, slight grain, no people's faces, no text, no logos), covering hero scenes in 16:9 and 21:9, details in 4:5 and 1:1. Save the result URLs as prospect/shoot-<trade>.json with descriptive keys.
3. For each prospect, add an entry to SITES in prospect/craft.py following the existing five exactly: a one-line concept comment, a palette (bg, bg2, dark, ink, mute, accent, accent2, paper) that is not a copy of another site's, a Google Fonts display+body pairing not used by another site in the file, hero_kind chosen for the business (cover, split or portrait), a hero photo and alt, eyebrow, h1 and sub written from their real listing and reviews, a true stat (rating, review count, hours, years if stated in a review, "Ltd" if a limited company), four gallery photos, six services written for that trade and that business, their real reviews word for word (trim long ones at a sentence boundary), and nearby areas. Never invent facts, awards, years in business or customers. If a prospect's trade is not a decorator, you may need to add trade-appropriate services and steps copy; keep the page structure.
4. Run python3 prospect/craft.py <slug> for each new one. Open each prospects/<slug>/index.html in a browser at 1366 and 390 wide, check nothing overflows, text is legible on every background, and the name split and phone are right. Fix and rerun as needed.
5. git add prospect prospects; commit "Preview sites for <date>"; git push -u origin claude/festive-albattani-iyheb4 (retry up to 4 times on network errors).
6. For each built prospect, Supabase execute_sql:
   update public.launch250_prospects set slug='<slug>', preview_url='https://preview.launch250.co.uk/<slug>/', built_at=now(), status = case when email is null then 'no_email' else 'built' end where id='<id>';
7. Finish with a short summary: names, preview links, and anything that looked wrong. Gaz reads that summary and approves or rejects each site on the admin page.

Rules: never touch demos/ or the main site pages; no pull requests; do not change the outreach email or prices; keep Higgsfield spend to one shoot per trade; if something blocks you, say exactly what in the summary.
