document.addEventListener("DOMContentLoaded", () => {

    // ===== SIDEBAR TOGGLE =====
    window.toggleSidebar = function () {
        let sidebar = document.getElementById("sidebar");

        if (window.innerWidth <= 768) {
            sidebar.classList.toggle("show");
        } else {
            sidebar.classList.toggle("hide");
        }

        localStorage.setItem("sidebar", sidebar.classList.contains("hide"));
    };

    // ===== RESTORE SIDEBAR =====
    let sidebar = document.getElementById("sidebar");
    if (localStorage.getItem("sidebar") === "true") {
        sidebar.classList.add("hide");
    }

    // ===== MAGNETIC EFFECT =====
    document.querySelectorAll(".nav-link").forEach(link => {

        link.addEventListener("mousemove", (e) => {
            const rect = link.getBoundingClientRect();

            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const moveX = (x - rect.width / 2) / 15;
            const moveY = (y - rect.height / 2) / 15;

            link.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });

        link.addEventListener("mouseleave", () => {
            link.style.transform = "translate(0,0)";
        });

    });

});

/* ===== NEON CURSOR TRAIL ===== */
document.addEventListener("mousemove", (e) => {

    const trail = document.createElement("div");
    trail.className = "cursor-trail";

    trail.style.left = e.clientX + "px";
    trail.style.top = e.clientY + "px";

    document.body.appendChild(trail);

    // Remove after animation
    setTimeout(() => {
        trail.remove();
    }, 600);

});