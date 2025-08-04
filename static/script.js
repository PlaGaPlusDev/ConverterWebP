document.addEventListener('DOMContentLoaded', function () {
    const themeSwitcher = document.getElementById('theme-switcher');
    const outputFormat = document.getElementById('output-format');
    const compressionGroup = document.getElementById('compression-group');
    const compressionSlider = document.getElementById('compression');
    const compressionValue = document.getElementById('compression-value');
    const fpsGroup = document.getElementById('fps-group');
    const fpsSlider = document.getElementById('fps');
    const fpsValue = document.getElementById('fps-value');
    const uploadForm = document.getElementById('upload-form');
    const resultDiv = document.getElementById('result');

    // Theme switcher
    themeSwitcher.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'light');
            themeSwitcher.textContent = 'Switch to Dark Mode';
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeSwitcher.textContent = 'Switch to Light Mode';
        }
    });

    // Toggle settings based on format
    outputFormat.addEventListener('change', () => {
        const selectedFormat = outputFormat.value;
        compressionGroup.style.display = 'none';
        fpsGroup.style.display = 'none';

        if (selectedFormat === 'jpg' || selectedFormat === 'webp' || selectedFormat === 'png') {
            compressionGroup.style.display = 'block';
        } else if (selectedFormat === 'gif') {
            fpsGroup.style.display = 'block';
        }
    });

    // Update slider values
    compressionSlider.addEventListener('input', () => {
        compressionValue.textContent = compressionSlider.value;
    });

    fpsSlider.addEventListener('input', () => {
        fpsValue.textContent = fpsSlider.value;
    });

    // Form submission
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const convertButton = uploadForm.querySelector('button[type="submit"]');
        convertButton.textContent = 'Converting...';
        convertButton.disabled = true;
        resultDiv.textContent = '';

        const formData = new FormData(uploadForm);

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                resultDiv.innerHTML = `<a href="${data.download_url}" download>Download Converted File</a>`;
            } else {
                resultDiv.textContent = `Error: ${data.error}`;
            }
        } catch (error) {
            resultDiv.textContent = 'An unexpected error occurred.';
        } finally {
            convertButton.textContent = 'Convert';
            convertButton.disabled = false;
        }
    });

    // Initial check for settings visibility
    outputFormat.dispatchEvent(new Event('change'));
});
