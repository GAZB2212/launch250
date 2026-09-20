"""Where the demo sites deploy from and how their editors log in.

REPO / BRANCH   the GitHub repo and branch Netlify builds and Decap commits to.
BRIDGE          DecapBridge site id per slug. Register each site once at
                https://decapbridge.com (free), paste the id here, rebuild,
                commit. Until an id is set the editor page explains what is missing
                instead of showing a login that cannot work.
"""
REPO = 'GAZB2212/launch250'
BRANCH = 'main'
BRIDGE = {
    'plumbing':    '',
    'electrical':  '',
    'joinery':     '',
    'landscaping': '',
    'barbers':     '',
    'doggrooming': '',
}
