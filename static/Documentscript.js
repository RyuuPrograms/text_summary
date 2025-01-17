let documentInputClicked = false;
let documentInput = document.getElementById('text');
documentInput.addEventListener('focus', function() {
    if (!documentInputClicked && documentInput.value.trim() === "DRAG YOUR TEXT HERE...") {
        documentInput.value = '';
        documentInputClicked = true;
    }
});

documentInput.addEventListener('blur', function() {
    if (documentInput.value.trim() === '') {
        documentInput.value = 'DRAG YOUR TEXT HERE...';
        documentInputClicked = false;
    }
});

document.getElementById('summarizeBtn').addEventListener('click', function() {
    summarizeBtnClicked = true;
});

let noteInput = document.getElementById('noteInput');
let notesList = document.getElementById('notesList');
let noteInputClicked = false;
let isFirstClick = true;

noteInput.addEventListener('focus', function() {
    if (!noteInputClicked && noteInput.value.trim() === "NOTES") {
        noteInput.value = '';
        noteInputClicked = true;
        updateNotesList();
    }
});

noteInput.addEventListener('keydown', function(event) {
    if ((event.key === 'Enter' || event.key === 'Clicked') && (event.key !== 'Enter' || event.key !== 'Clicked')) {
        event.preventDefault(); 
        insertBulletPoint();
        updateNotesList();
    }
});
                        
function insertBulletPoint() {
    let currentPosition = noteInput.selectionStart;
    let currentValue = noteInput.value;
    let newValue =
        currentValue.substring(0, currentPosition) + '\n• ' +
        currentValue.substring(currentPosition);
    
    noteInput.value = newValue;
}
document.getElementById("text").addEventListener("keydown", function(e) {
    if (e.key === "Tab") {
        e.preventDefault();
        var start = this.selectionStart;
        var end = this.selectionEnd;

        var spaces = "     ";
        this.value = this.value.substring(0, start) + spaces + this.value.substring(end);

        this.selectionStart = this.selectionEnd = start + spaces.length;
    }
});
