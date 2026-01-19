function showSection(section) {
    document.getElementById("hits-section").classList.add("hidden");
    document.getElementById("profile-section").classList.add("hidden");

    if (section === "hits") {
        document.getElementById("hits-section").classList.remove("hidden");
    } else {
        document.getElementById("profile-section").classList.remove("hidden");
    }
}

function parseCSV(text) {
    const lines = text.trim().split("\n");
    const headers = lines[0].split(",");

    return lines.slice(1).map(line => {
        const values = line.split(",");
        const obj = {};
        headers.forEach((h, i) => obj[h.trim()] = values[i]?.trim());
        return obj;
    });
}

async function loadHits() {
    const response = await fetch("data/hits_output.csv");
    const text = await response.text();
    const rows = parseCSV(text);

    const tbody = document.querySelector("#hits-table tbody");
    rows.forEach(r => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
      <td>${r.seq_id}</td>
      <td>${r.best_hit}</td>
    `;
        tbody.appendChild(tr);
    });
}

async function loadProfile() {
    const response = await fetch("data/profile_output.csv");
    const text = await response.text();

    const lines = text.trim().split("\n");
    const headers = lines[0].split(",");
    const values = lines[1].split(",");

    const data = {};
    headers.forEach((h, i) => {
        data[h.trim()] = values[i].trim();
    });

    const tbody = document.querySelector("#profile-table tbody");

    const tr = document.createElement("tr");
    tr.innerHTML = `
    <td>${data.ave_std}</td>
    <td>${data.ave_gmean}</td>
  `;
    tbody.appendChild(tr);
}

loadHits();
loadProfile();