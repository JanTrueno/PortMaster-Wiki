// Hourly rebuild. The site is static and its data (ports, porters, runtimes,
// devices) is downloaded from GitHub while `mkdocs build` runs, so refreshing
// it just means asking Workers Builds for a new build. The cron schedule lives
// in wrangler.jsonc ("triggers"); the deploy hook URL is a Worker *secret*
// called DEPLOY_HOOK_URL (Settings > Variables and secrets), never committed.
//
// Page requests never reach this script: static assets are served before the
// Worker runs, and unknown URLs get site/404.html (not_found_handling).
export default {
  async scheduled(controller, env, ctx) {
    if (!env.DEPLOY_HOOK_URL) {
      throw new Error("DEPLOY_HOOK_URL secret is not set");
    }
    const res = await fetch(env.DEPLOY_HOOK_URL, { method: "POST" });
    if (!res.ok) {
      throw new Error(`Deploy hook returned ${res.status} ${res.statusText}`);
    }
  },
};
