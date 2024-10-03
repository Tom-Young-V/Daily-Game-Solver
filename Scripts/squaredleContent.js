// content.js
console.log("Squaredle content script loaded!");


var solveMode = false
var board = []
var boardDivs = []
var clickableDivs = []
var wordsList = []
var currentWordIndex = 0
var autoDragging
var boardSize
var specialPuzzle

var highlightedTiles = false
var changedDivs = []

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

function getNext() {

	let added = false

	// if you just tried the recommended word, move on (it could be not included in the puzzle)

	lastWord = document.querySelector("#wordDefiner");
	lastWordIncorrect = document.querySelector("#incorrectWordText");

	if (wordsList[currentWordIndex][0] === "olympic" || wordsList[currentWordIndex][0] === "olympics") {
		currentWordIndex += 1
		added = true
	}

	if (lastWord.textContent === wordsList[currentWordIndex][0] || lastWordIncorrect.textContent === wordsList[currentWordIndex][0]) {
		currentWordIndex += 1
		added = true
	}

	if (currentWordIndex >= wordsList.length) {
		currentWordIndex = 0
		solveMode = false
		return
	}

	// skip over words you already found

	foundWords = []

	foundWordDivs = document.querySelectorAll("#wordsTodayTab > div.wordLengths li[data-word]")
	foundWordDivs.forEach((foundWordDiv) => {
		foundWords.push(foundWordDiv.textContent);
	});

	while (foundWords.includes(wordsList[currentWordIndex][0]) && currentWordIndex < wordsList.length) {
		currentWordIndex += 1;
		added = true
	}

	console.log(currentWordIndex, wordsList.length)
	if (currentWordIndex >= wordsList.length) {
		currentWordIndex = 0
		solveMode = false
	}


}

function getRGB(index) {
	// Assuming `index` is between 4 and 16
	let minIndex = 4;
	let maxIndex = 16;

	let adjustedIndex = (index - minIndex) / (maxIndex - minIndex); // Normalize index to a value between 0 and 1

	// Define the base RGB values for a lighter shade of orange
	let baseRed = 255;
	let baseGreen = 180; // Start with a lighter green to make the initial color lighter
	let baseBlue = 0; // Blue remains 0 for orange shades

	// Aggressively increase green to lighten the color faster
	let red = baseRed;
	let green = Math.min(255, baseGreen + Math.round(adjustedIndex * 2 * (255 - baseGreen))); // Multiply by 2 for more aggressive lightening
	let blue = baseBlue;

	// Set the background color based on the calculated RGB values
	RGB = `rgb(${red}, ${green}, ${blue})`;

	return RGB
}

function highlightTiles() {

	getNext()

	if (! solveMode) {
		console.log("Finished all words solver found")
		return
	}

	let currentWordStrand
	currentWordStrand = wordsList[currentWordIndex]

	console.log(currentWordStrand)

	if (true) {
		autoDragWord(currentWordStrand);
		getUnclickActions()

	} else {
		highlightedTiles = true

		currentWordStrand[1].forEach((letterIndex, wordStrandIndex) => {
			let div
			div = boardDivs[letterIndex]
			changedDivs.push([div, div.style.backgroundColor, div.style.color])
			div.style.backgroundColor = getRGB(wordStrandIndex);
			div.style.color = "black"

		});
	}
	
}

function revertStyles() {
	highlightedTiles = false
	changedDivs.forEach((changedDivInfo) => {
		changedDivInfo[0].style.backgroundColor = changedDivInfo[1];
		changedDivInfo[0].style.color = changedDivInfo[2];
	});

	changedDivs = []
}

async function autoDragWord(wordStrand) {
	autoDragging = true

	let wordStrandDivs = []

	wordStrand[1].forEach((letterIndex) => {
		wordStrandDivs.push(clickableDivs[letterIndex])

	});

    // Click and hold on the first div
    const firstDiv = wordStrandDivs[0];
    const firstRect = firstDiv.getBoundingClientRect();
    const pointerDownEvent = new PointerEvent('pointerdown', {
        bubbles: true,
        cancelable: true,
        clientX: firstRect.left + firstRect.width / 2,
        clientY: firstRect.top + firstRect.height / 2,
        pointerId: 1,
        isPrimary: true
    });
    firstDiv.dispatchEvent(pointerDownEvent);

    await sleep(15)

    // Drag over the wordStrandDivs
    for (let i = 1; i < wordStrandDivs.length; i++) {
        const wordStrandDiv = wordStrandDivs[i];
        const rect = wordStrandDiv.getBoundingClientRect();
        const pointerMoveEvent = new PointerEvent('pointermove', {
            bubbles: true,
            cancelable: true,
            clientX: rect.left + rect.width / 2,
            clientY: rect.top + rect.height / 2,
            pointerId: 1
        });
        wordStrandDiv.dispatchEvent(pointerMoveEvent);
        
        await sleep(15);
    }

    // Release the click on the last wordStrandDiv
    const lastDiv = wordStrandDivs[wordStrandDivs.length - 1];
    const lastRect = lastDiv.getBoundingClientRect();
    const pointerUpEvent = new PointerEvent('pointerup', {
        bubbles: true,
        cancelable: true,
        clientX: lastRect.left + lastRect.width / 2,
        clientY: lastRect.top + lastRect.height / 2,
        pointerId: 1
    });
    lastDiv.dispatchEvent(pointerUpEvent);

    autoDragging = false;

    getUnclickActions();
}

function getBoard(URL) {

	if (URL.includes("puzzle")) {
		specialPuzzle = true
	} else {
		specialPuzzle = false

		if (URL.includes("xp")) {
			boardSize = 9;
		} else {
			boardSize = 16;
		}
	}
	
	// Select all divs with the correct class name
	let specificDivs;
	specificDivs = document.querySelectorAll('.letters .letter .unnecessaryWrapper');

	// Create an array to store the div information
	
	board = []; // Empty the grid array

	// Loop through the selected divs
	specificDivs.forEach((div, index) => {
		if (specialPuzzle) {
			board.push(div.textContent);
		} else {
			if (index < boardSize) {
				board.push(div.textContent);
			}
		}
	});

	boardDivs = []

	allBoardDivs = document.querySelectorAll('.letters .letter .content');
	allBoardDivs.forEach((div, index) => {
		if (specialPuzzle) {
			boardDivs.push(div);
		} else {
			if (index < boardSize) {
				boardDivs.push(div);
			}
		}
	});

	clickableDivs = []

	allClickableDivs = document.querySelectorAll('.letters .letter .unnecessaryWrapper');
	allClickableDivs.forEach((div, index) => {
		if (specialPuzzle) {
			clickableDivs.push(div)
		} else {
			if (index < boardSize) {
				clickableDivs.push(div);
			}
		}
	});

	return board

}

function getUnclickActions() {
	if (autoDragging) {
		return
	}

	if (! solveMode) {
		return
	}

	revertStyles()

	highlightTiles()
}


// Listen for messages from the background script
chrome.runtime.onMessage.addListener((message) => {
	if (message.action === "getBoard") {

		if (solveMode) {
			console.log("Solver turned off")
			currentWordIndex = 0
			solveMode = false;
			revertStyles();
			return;
		} else {
			console.log("Solver turned on")
			solveMode = true
		}

		var board = getBoard(message.URL)

		console.log(board)

		if (! specialPuzzle) {
			if (board.length != boardSize) {
				console.log("Failed to retrieve board")
				return
			}
		}

		chrome.runtime.sendMessage({ action: "sendBoardInfo", board });

	} else if (message.action === "sendWordsList") {
		wordsList = message.solution.wordsList
		console.log(wordsList)

		highlightTiles()
	}

});

// not sure why it has to be this way but it only works this way for some reason
// document.addEventListener('click', getUnclickActions);





