(function () {
    // Demo-style core logic (use data-theme attribute + localStorage)
    const STORAGE_KEY = 'theme'; // must match snippet

    const toggleBtn = document.querySelector('[data-theme-toggle]');
    const html = document.documentElement;

    function applyTheme(dark) {
        const theme = dark ? 'dark' : 'light';

        // Match the example: only toggle data-theme on <html>
        html.setAttribute('data-theme', theme);

        // Persist preference
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (e) {
            // ignore
        }

        // Update button label (your UI expectation)
        if (toggleBtn) {
            toggleBtn.textContent = dark ? 'Switch to Light' : 'Switch to Dark';
        }

        // Browser chrome / mobile address bar color
        const meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.setAttribute('content', dark ? '#0b1020' : '#f3f4ff');
    }

    // Restore on load (match example)
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'dark' || saved === 'light') {
        applyTheme(saved === 'dark');
    } else {
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(prefersDark);
    }

    // Switch (match example behavior: toggle data-theme)
    if (toggleBtn) {
        toggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const currentTheme = html.getAttribute('data-theme') || 'dark';
            const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
            applyTheme(nextTheme === 'dark');
        });
    }
})();


