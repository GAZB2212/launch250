"""Where the demo sites deploy from and how their editors log in.

REPO / BRANCH   the GitHub repo and branch Netlify builds and Decap commits to.
BRIDGE          DecapBridge site id per slug. Register each site once at
                https://decapbridge.com (free), paste the id here, rebuild,
                commit. Until an id is set the editor page explains what is missing
                instead of showing a login that cannot work.
"""
REPO = 'GAZB2212/launch250'
# Where each site is reachable right now. Used for the editor's "view site" link
# and its login-page logo. Default is the launch250 subdomain; override while a
# site is still on its netlify.app address.
URL = {
    'plumbing': 'https://launch250-plumbing.netlify.app',
}
BRANCH = 'claude/festive-albattani-iyheb4'   # rename here if you later rename the branch on GitHub
BRIDGE = {
    'plumbing':    'a5f94a16-5122-4549-a7b0-2596822b8329',
    'electrical':  '',
    'joinery':     '',
    'landscaping': '',
    'barbers':     '',
    'doggrooming': '',
}
