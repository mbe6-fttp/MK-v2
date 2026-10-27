document.addEventListener("DOMContentLoaded", () => {
    const searchInput =
        document.getElementById("knowledge-search");
    const sidebar =
        document.getElementById("sidebar");
    const menuToggle =
        document.querySelector(".menu-toggle");
    const sidebarClose =
        document.querySelector("[data-sidebar-close]");
    const mobileLayout =
        window.matchMedia("(max-width: 820px)");
    const themeToggle =
        document.querySelector("[data-theme-toggle]");

    const applyTheme = (theme) => {
        document.body.dataset.theme = theme;
        const isDark = theme === "dark";
        themeToggle?.setAttribute(
            "aria-label",
            isDark ? "Activează tema luminoasă" : "Activează tema întunecată"
        );
        themeToggle?.querySelector(".theme-icon")?.replaceChildren(
            document.createTextNode(isDark ? "☀" : "☾")
        );
    };

    let savedTheme = "light";
    try {
        savedTheme = localStorage.getItem("my-knowledge-theme") || "light";
    } catch (error) {
        console.warn("Nu am putut citi preferința de aspect.", error);
    }
    applyTheme(savedTheme === "dark" ? "dark" : "light");

    themeToggle?.addEventListener("click", () => {
        const nextTheme =
            document.body.dataset.theme === "dark" ? "light" : "dark";
        applyTheme(nextTheme);

        try {
            localStorage.setItem("my-knowledge-theme", nextTheme);
        } catch (error) {
            console.warn("Preferința de aspect nu a putut fi salvată.", error);
        }
    });

    const setSidebarOpen = (isOpen, restoreFocus = false) => {
        document.body.classList.toggle("sidebar-open", isOpen);
        menuToggle?.setAttribute("aria-expanded", String(isOpen));
        menuToggle?.setAttribute(
            "aria-label",
            isOpen ? "Închide meniul" : "Deschide meniul"
        );

        if (isOpen) {
            window.requestAnimationFrame(() => {
                sidebar?.querySelector("a")?.focus();
            });
        } else if (restoreFocus) {
            menuToggle?.focus();
        }
    };

    menuToggle?.addEventListener("click", () => {
        const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
        setSidebarOpen(!isOpen);
    });

    sidebarClose?.addEventListener("click", () => {
        setSidebarOpen(false, true);
    });

    sidebar?.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            if (mobileLayout.matches) {
                setSidebarOpen(false);
            }
        });
    });

    mobileLayout.addEventListener("change", (event) => {
        if (!event.matches) {
            setSidebarOpen(false);
        }
    });

    document.addEventListener("keydown", (event) => {
        const activeElement =
            document.activeElement;
        const isEditing =
            activeElement instanceof HTMLElement &&
            (
                activeElement.isContentEditable ||
                ["INPUT", "TEXTAREA", "SELECT"].includes(activeElement.tagName)
            );

        if (
            event.key === "Escape" &&
            document.body.classList.contains("sidebar-open")
        ) {
            event.preventDefault();
            setSidebarOpen(false, true);
        }

        if (
            event.key === "/" &&
            !isEditing &&
            !event.ctrlKey &&
            !event.metaKey &&
            !event.altKey
        ) {
            event.preventDefault();
            searchInput?.focus();
        }

        if (
            (event.ctrlKey || event.metaKey) &&
            event.key.toLowerCase() === "k"
        ) {
            event.preventDefault();
            searchInput?.focus();
        }
    });

    const textareas =
        document.querySelectorAll("textarea");

    textareas.forEach((textarea) => {
        const counter =
            textarea.closest(".field")?.querySelector("[data-character-count]");

        const resizeTextarea = () => {
            textarea.style.height = "auto";
            textarea.style.height =
                `${textarea.scrollHeight}px`;

            if (counter) {
                const count = new Intl.NumberFormat("ro-RO")
                    .format(textarea.value.length);
                counter.textContent = `${count} caractere`;
            }
        };

        resizeTextarea();
        textarea.addEventListener(
            "input",
            resizeTextarea
        );

    });

    document.querySelectorAll(".flash").forEach((flash) => {
        if (flash.getAttribute("role") === "alert") {
            return;
        }

        setTimeout(() => {
            flash.classList.add("flash-leaving");
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });

});