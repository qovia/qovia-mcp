// Search Xiaohongshu (RedNote) notes with the Qovia API. Node.js 18+, no dependencies.
//
//   QOVIA_API_KEY=sk-qovia-... node quickstart.mjs coffee

const keyword = process.argv[2] ?? "coffee";
const url = new URL("https://api.qovia.ai/v1/raw/xiaohongshu/search");
url.search = new URLSearchParams({ keyword, sort: "latest" });

const response = await fetch(url, {
  headers: { Authorization: `Bearer ${process.env.QOVIA_API_KEY}` },
});
const body = await response.json();
if (!response.ok) {
  console.error(response.status, body.error?.code, body.error?.message);
  process.exit(1);
}
for (const item of body.data.items) {
  console.log(item.extra.url, "|", item.text.slice(0, 60).replaceAll("\n", " "));
}
console.log(`charged $${body.meta.charged_usd}`);
