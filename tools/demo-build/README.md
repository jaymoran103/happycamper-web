# demo-build

Builds the demo page from `template.html` and fictional rosters, then checks it.

1. **Build:** `python3 -I build.py . out` writes `out/index.html`.
2. **Check:** `python3 -I mk.py . out` writes `shots/test.html`. Open it in a browser, and read the result block at the bottom. It should say `FAILS=0`.

`expected.js` and the `*/roster.json` files are the real HappyCamper 2.5 engine's output for these rosters. To regenerate them, build happycamper-heart (`mvn -o -DskipTests package`). Then run the Java files in `oracle/` from that repo, with `target/classes:target/lib/*` on the classpath:

- `Oracle <campers.csv> <activities.csv>` prints the enriched roster, assertions and activity report as JSON.
- `Programs <campers.csv> <activities.csv>` prints programs with their round groups.
- `Demand <campers.csv> <activities.csv> <activity>` prints the demand sort order.

`site/demo.html` is `out/index.html` with the shared site header applied.
