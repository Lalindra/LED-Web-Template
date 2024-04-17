// script.js
function updatePalettePreview() {
    var paletteSelect = document.getElementById("palette");
    var previewDiv = document.getElementById("palette-preview");
    var selectedPalette = paletteSelect.options[paletteSelect.selectedIndex].value;
    var palettes = JSON.parse('{{ palettes | tojson | safe }}');
    var colors = palettes[selectedPalette];
    previewDiv.innerHTML = "";
    colors.forEach(function(color) {
        var colorSample = document.createElement("div");
        colorSample.className = "color-sample";
        colorSample.style.backgroundColor = color;
        previewDiv.appendChild(colorSample);
    });
}
