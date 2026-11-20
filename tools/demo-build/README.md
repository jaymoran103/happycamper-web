# demo-build

Builds the demo page from `template.html` and fictional rosters, then checks it.

1. **Build:** `python3 -I build.py . out` writes `out/index.html`.
2. **Check:** `python3 -I mk.py . out` writes `shots/test.html`. Open it in a browser, and read the result block at the bottom. It should say `FAILS=0`.

`expected.js` and the `*/roster.json` files are the real HappyCamper 2.5 engine's output for these rosters. To regenerate them, build happycamper-heart (`mvn -o -DskipTests package`). Then run the Java files in `oracle/` from that repo, with `target/classes:target/lib/*` on the classpath:

- `Oracle <campers.csv> <activities.csv>` prints the enriched roster, assertions and activity report as JSON.
- `Programs <campers.csv> <activities.csv>` prints programs with their round groups.
- `Demand <campers.csv> <activities.csv> <activity>` prints the demand sort order.

To refresh the site after a build, run `python3 -I tools/site/make-site.py` from the repo root. It writes `site/demo.html` from `out/index.html`, and `site/index.html` from the download draft, with the shared header, switcher and footer.

The checks expect v12's left-aligned header. Run against `site/demo.html`, they report 3 alignment failures, because the site centers its header.
