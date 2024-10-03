// content.js
console.log("Waffle content script loaded!");

var solveMode = false
var highlightedTiles = false
var changedDivs = []
var currentGrid = []
var currentGridDivs = []
var autoSwapping = false

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

async function highlightTiles(targetPositions) {
	highlightedTiles = true
	console.log(targetPositions[0], targetPositions[1])
	// Loop through each target position

	targetDivs = []

	console.log(currentGridDivs)

	currentGridDivs.forEach((div) => {

		var position = div.getAttribute('data-pos');
		position = JSON.parse(position);
		position = [position.x, position.y];

		if (targetPositions.some(pos => pos[0] === position[0] && pos[1] === position[1])) {
			targetDivs.push(div);
		}

	});

	if (true) {
		swapDivs(targetDivs[0], targetDivs[1]);
		await sleep(250)
		getUnclickActions()

	} else {
		changedDivs = []; // Empty the changedDivs array

		changedDivs.push([div, div.style.backgroundColor, div.style.color]);
		div.style.backgroundColor = "orange";
		div.style.color = "black"
	}

	console.log(changedDivs)
}

function revertStyles() {
	highlightedTiles = false
	changedDivs.forEach((changedDivInfo) => {
		changedDivInfo[0].style.backgroundColor = changedDivInfo[1];
		changedDivInfo[0].style.color = changedDivInfo[2];
	});

}

function swapDivs(startDiv, endDiv) {
	autoSwapping = true

	console.log(startDiv, endDiv);

    // Trigger mousedown event on the start div
    const startRect = startDiv.getBoundingClientRect();
    const mouseDownEvent = new MouseEvent('mousedown', {
        bubbles: true,
        cancelable: true,
        clientX: startRect.left + startRect.width / 2,
        clientY: startRect.top + startRect.height / 2
    });
    startDiv.dispatchEvent(mouseDownEvent);
    console.log('Mouse down event dispatched on startDiv');

    // Simulate mouse movement towards the end div
    const endRect = endDiv.getBoundingClientRect();
    const mouseMoveEvent = new MouseEvent('mousemove', {
        bubbles: true,
        cancelable: true,
        clientX: endRect.left + endRect.width / 2,
        clientY: endRect.top + endRect.height / 2
    });
    document.dispatchEvent(mouseMoveEvent);
    console.log('Mouse move event dispatched towards endDiv');

    // Trigger mouseup event on the end div
    const mouseUpEvent = new MouseEvent('mouseup', {
        bubbles: true,
        cancelable: true,
        clientX: endRect.left + endRect.width / 2,
        clientY: endRect.top + endRect.height / 2
    });
    endDiv.dispatchEvent(mouseUpEvent);
    console.log('Mouse up event dispatched on endDiv');

    autoSwapping = false
}

function getBoard() {

	let specificDivs
	let swapsLeft

	currentURL = window.location.href;

	if (currentURL.includes("daily")) {
		// Select all divs with the class name "tile draggable"
		specificDivs = document.querySelectorAll('.game.game-main.game--active .top .board .tile.draggable');

		swapsLeft = document.querySelector('.game.game-main.game--active .top .swaps .swaps__val').innerHTML;

	} else if (currentURL.includes("deluxe")) {

		specificDivs = document.querySelectorAll('.deluxe.game.game--active.active .top .board .tile.draggable');

		swapsLeft = document.querySelector('.deluxe.game.game--active.active .top .swaps .swaps__val').innerHTML;

	} else {
		const archiveDiv = document.querySelector('.archive-main.game')
		const gameActive = archiveDiv.classList.contains('game--active');

		console.log(gameActive)

		if (! gameActive) {
			solveMode = false
			revertStyles()
			return false
		}

		const gameMode = document.querySelector('.archive .archive__tabs.row')
		const selectedTab = gameMode.querySelector('.tab.tab--selected');

		specificDivs = archiveDiv.querySelectorAll('.top .board .tile.draggable');

		if (selectedTab.classList.contains('tab--daily')) {
			swapsLeft = archiveDiv.querySelector('.top .swaps .swaps__val').innerHTML;
		} else if (selectedTab.classList.contains('tab--deluxe')) {
			swapsLeft = archiveDiv.querySelector('.top .swaps .swaps__val').innerHTML;
		}
	}

	// Create an array to store the div information
	
	currentGridDivs = []
	currentGrid = []; // Empty the currentGrid array

	// Loop through the selected divs
	specificDivs.forEach((div) => {
		currentGrid.push(div.outerHTML);
		currentGridDivs.push(div)
	});
	
	return [currentGrid, swapsLeft]
}

function getUnclickActions() {

	if (autoSwapping) {
		return;
	}

	if (! solveMode) {
		return
	}

	revertStyles()
	var boardInfo = getBoard()

	if (! boardInfo) {
		console.log("Not on the active page, stopped")
		return
	}

	if (boardInfo[0].length) {
		console.log("getting next")
		chrome.runtime.sendMessage({ action: "sendBoardInfo", boardInfo });
	}
}

const menuButton = document.querySelector('.button--menu.icon-button');

menuButton.addEventListener('click', function(event) {
	solveMode = false
	revertStyles()
});

const backButton = document.querySelector('.button--back.icon-button');

backButton.addEventListener('click', function(event) {
	solveMode = false
	revertStyles()
});

const archiveButtons = document.querySelector('.archive-main__buttons');

archiveButtons.addEventListener('click', function(event) {
	solveMode = false
	revertStyles()
});



// Listen for messages from the background script
chrome.runtime.onMessage.addListener((message) => {
	if (message.action === "getBoard") {
		if (! solveMode) {
			console.log("Solver turned on")
			solveMode = true;
		} else {
			console.log("Solver turned off")
			solveMode = false;
			revertStyles();
			return;
		}

		getUnclickActions()

		// if (! highlightedTiles) {
		// 	var boardInfo = getBoard()

		// 	if (! boardInfo) {
		// 		console.log("Not on the active page, stopped")
		// 		return
		// 	}

		// 	if (boardInfo[0].length) {
		// 		currentlySolving = true
		// 		chrome.runtime.sendMessage({ action: "sendBoardInfo", boardInfo });
		// 	} else {
		// 		console.log("failed to find divInfoList")
		// 	}
		// }

	} else if (message.action === "updateColors") {

		const receivedSolution = message.solution;
		// Process the solution as needed
		console.log("Received solution in content script:", receivedSolution);

		// Extract targetPositions from the received solution
		const targetPositions = receivedSolution.nextSwap;

		// Call the highlightTiles function with the extracted targetPositions

		highlightTiles(targetPositions);

	}
});

// document.body.addEventListener('mouseup', getUnclickActions);



