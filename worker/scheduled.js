// Rebuilds the site when its data may have changed. The site is static and the
// ports/porters/runtimes/devices data is downloaded from GitHub while
// `mkdocs build` runs, so "refreshing" just means asking Workers Builds for a
// new build through a deploy hook. Pushes to this repo already build on their
// own (Git integration), so they aren't handled here.
//
// The cron in wrangler.jsonc fires every INTERVAL_MIN minutes:
//   - on the hour it always builds (also picks up PortMaster-Info changes,
//     which are plain commits and have no release to watch);
//   - on the other runs it builds only if a port repo published a release a few
//     minutes ago, so a release shows up within ~15 minutes instead of ~1 hour.
//
// DEPLOY_HOOK_URL is a Worker *secret* (Settings > Variables and secrets),
// never committed. Page requests never reach this script: static assets are
// served before the Worker runs, and unknown URLs get site/404.html.

const RELEASE_FEEDS = [
  "https://github.com/PortsMaster/PortMaster-New/releases.atom",
  "https://github.com/PortsMaster-MV/PortMaster-MV-New/releases.atom",
];

// Must match the cron in wrangler.jsonc.
const INTERVAL_MIN = 10;
// Give a fresh release a few minutes to finish attaching its assets
// (ports.json etc.) before building. A release lands in exactly one run's
// [SETTLE_MIN, SETTLE_MIN + INTERVAL_MIN) window, so it triggers one build.
const SETTLE_MIN = 3;

// Time of the newest release in an Atom feed, in ms since the epoch, or null.
async function newestRelease(feed) {
  const res = await fetch(feed, { headers: { "User-Agent": "portmaster-wiki-rebuild" } });
  if (!res.ok) {
    throw new Error(`${feed} returned ${res.status}`);
  }
  const xml = await res.text();
  const times = [...xml.matchAll(/<entry>[\s\S]*?<updated>([^<]+)<\/updated>/g)]
    .map((m) => Date.parse(m[1]))
    .filter((t) => !Number.isNaN(t));
  return times.length ? Math.max(...times) : null;
}

export default {
  async scheduled(controller, env, ctx) {
    if (!env.DEPLOY_HOOK_URL) {
      throw new Error("DEPLOY_HOOK_URL secret is not set");
    }

    const now = controller.scheduledTime;
    let reason = new Date(now).getUTCMinutes() === 0 ? "hourly refresh" : null;
    const feedErrors = [];

    if (!reason) {
      const results = await Promise.allSettled(RELEASE_FEEDS.map(newestRelease));
      results.forEach((result, i) => {
        if (result.status === "rejected") {
          feedErrors.push(result.reason);
          return;
        }
        if (result.value === null) {
          return;
        }
        const ageMin = (now - result.value) / 60000;
        if (ageMin >= SETTLE_MIN && ageMin < SETTLE_MIN + INTERVAL_MIN) {
          reason = `new release in ${RELEASE_FEEDS[i]}`;
        }
      });
    }

    if (reason) {
      const res = await fetch(env.DEPLOY_HOOK_URL, { method: "POST" });
      if (!res.ok) {
        throw new Error(`Deploy hook returned ${res.status} ${res.statusText}`);
      }
      console.log(`Triggered a build: ${reason}`);
    }

    // A feed that couldn't be read shouldn't pass silently: it is how a
    // release would be missed until the next hourly build.
    if (feedErrors.length) {
      throw feedErrors[0];
    }
  },
};
