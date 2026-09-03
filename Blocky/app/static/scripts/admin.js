const sql = document.querySelector("#sql");
const target = document.querySelector("#target");
const results = document.querySelector("#results");
document.querySelector("#run-query").addEventListener("click", async () => {
    results.textContent = "Running...";
    const response = await fetch("/admin/query", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ sql: sql.value, target: target.value }) });
    results.textContent = JSON.stringify(await response.json(), null, 2);
});