console.log("script.js loaded, pathname =", window.location.pathname);

const API = "http://127.0.0.1:8000/movies";

// =========================
// INDEX PAGE LOGIC
// =========================
if (window.location.pathname.endsWith("index.html") || window.location.pathname === "/") {

    console.log("index.html logic attached");

    // Load movies
    fetch(API)
        .then(res => res.json())
        .then(movies => {
            const list = document.getElementById("moviesList");

            movies.forEach(movie => {
                const li = document.createElement("li");
                li.innerHTML = `
                    <input type="checkbox" value="${movie.id}">
                    ${movie.title}, ${movie.year}, ${movie.actors}
                `;
                list.appendChild(li);
            });
        });

    // Delete selected
    document.getElementById("deleteBtn").addEventListener("click", async () => {
        const checked = [...document.querySelectorAll("input[type=checkbox]:checked")];

        for (const checkbox of checked) {
            await fetch(`${API}/${checkbox.value}`, {
                method: "DELETE"
            });
        }

        location.reload();
    });

    // Delete ALL
    document.getElementById("deleteAllBtn").addEventListener("click", async () => {
        if (!confirm("Are you sure you want to delete ALL movies?")) {
            return;
        }

        await fetch(API, {
            method: "DELETE"
        });

        location.reload();
    });

    // Edit selected
    document.getElementById("editBtn").addEventListener("click", () => {
        const checked = [...document.querySelectorAll("input[type=checkbox]:checked")];

        if (checked.length === 0) {
            alert("Please select a movie to edit.");
            return;
        }

        if (checked.length > 1) {
            alert("Please select ONLY ONE movie to edit.");
            return;
        }

        const id = checked[0].value;
        window.location.href = `add.html?id=${id}`;
    });
}


// =========================
// ADD / EDIT MOVIE PAGE
// =========================
if (window.location.pathname.endsWith("add.html")) {

    console.log("add.html logic attached");

    const urlParams = new URLSearchParams(window.location.search);
    const editId = urlParams.get("id");

    // If editing, load movie data
    if (editId) {
        fetch(`${API}`)
            .then(res => res.json())
            .then(movies => {
                const movie = movies.find(m => m.id == editId);
                if (!movie) return;

                document.getElementById("title").value = movie.title;
                document.getElementById("year").value = movie.year;
                document.getElementById("actors").value = movie.actors;
            });
    }

    document.getElementById("addForm").addEventListener("submit", async (e) => {
        e.preventDefault();

        const movie = {
            title: document.getElementById("title").value,
            year: document.getElementById("year").value,
            actors: document.getElementById("actors").value
        };

        if (editId) {
            // PUT update
            await fetch(`${API}/${editId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(movie)
            });
        } else {
            // POST new
            await fetch(API, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(movie)
            });
        }

        window.location.href = "index.html";
    });
}
