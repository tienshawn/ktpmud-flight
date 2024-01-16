function showAutocomplete(inputIndex) {
    var inputId = "autocompleteInput" + inputIndex;
    var listId = "autocompleteList" + inputIndex;

    var input = document.getElementById(inputId);
    var dataList = document.getElementById("autocomplete-options" + inputIndex);
    var autocompleteList = document.getElementById(listId);
    var options = dataList.options;
    var inputValue = input.value.toLowerCase();

    // Clear previous autocomplete options
    autocompleteList.innerHTML = '';

    // Display autocomplete options that match the input value
    for (var i = 0; i < options.length; i++) {
        var optionValue = options[i].value.toLowerCase();
        if (optionValue.startsWith(inputValue)) {
            var li = document.createElement('li');
            li.textContent = options[i].value;
            li.onclick = function() {
                input.value = this.textContent;
                autocompleteList.style.display = 'none';
            };
            autocompleteList.appendChild(li);
        }
    }

    // Show or hide the autocomplete list based on whether there are matching options
    autocompleteList.style.display = autocompleteList.children.length > 0 ? 'block' : 'none';
}

// Hide autocomplete list when clicking outside the input and list
document.addEventListener('click', function(event) {
    var autocompleteContainer = document.getElementById("autocompleteContainer");
    var autocompleteLists = document.querySelectorAll('.autocomplete-list');

    for (var i = 0; i < autocompleteLists.length; i++) {
        if (event.target !== autocompleteContainer && !autocompleteContainer.contains(event.target)) {
            autocompleteLists[i].style.display = 'none';
        }
    }
});
