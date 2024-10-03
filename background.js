// background.js
console.log("Extension loaded!");

const waffleURL = "https://wafflegame.net"
const squaredleURL = "https://squaredle.app/"

function activateSolver() {
	chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
		const activeTab = tabs[0];
		if (! activeTab) {
			console.log("Tab not active");
			return
		}

		if (activeTab.url.includes(waffleURL)) {
			console.log("Starting Waffle Solver");
			// Send a message to content.js
			chrome.tabs.sendMessage(activeTab.id, { action: "getBoard", URL: activeTab.url });

		} else if (activeTab.url.includes(squaredleURL)) {
			console.log("Starting Squaredle Solver");
			chrome.tabs.sendMessage(activeTab.id, { action: "getBoard", URL: activeTab.url });

		} else {
			console.log("Failed: Not on a valid webpage");
		}

	});
}

// Detect navigation to the specified URL
chrome.webNavigation.onCompleted.addListener((details) => {
	if (details.url.includes(waffleURL)) {
		console.log('Navigated to https://wafflegame.net');
	} else if (details.url.includes(squaredleURL)) {
		console.log('Navigated to https://squaredle.app/');
	}
});

chrome.action.onClicked.addListener((tab) => {
    // Icon clicked
    console.log("Icon clicked!");
    activateSolver()
});

// Send command to content.js when the command is pressed
chrome.commands.onCommand.addListener((command) => {
	if (command === "solvePuzzle") {
		console.log("solvePuzzle command pressed");
		activateSolver()
	}
});

// Listen for messages from content.js of divInfo when solving
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
	if (message.action === "sendBoardInfo") {

		// the gross python flask stuff

		if (sender.url.includes(waffleURL)) {

			const pythonServerUrl = "http://127.0.0.1:5000/solveWaffle";

			fetch(pythonServerUrl, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ "gameBoardHTML": message.boardInfo }),
			})
				.then((response) => response.json())
				.then((solution) => {
					// Assuming the Python server responds with the solution
					console.log("Received solution from Python:", solution);
					if (solution.finished) {
						console.log("Solution already finished, no need to get the next swap")
					} else if (solution.failed) {
						console.log("Solver failed")
					} else {
						// Now send the solution back to the content script
						chrome.tabs.sendMessage(sender.tab.id, { action: "updateColors", solution });
					}
				})
				.catch((error) => {
					console.error("Error communicating with Python server:", error);
				});

		} else if (sender.url.includes(squaredleURL)) {

			const pythonServerUrl = "http://127.0.0.1:5000/solveSquaredle";
			console.log(message.board)

			fetch(pythonServerUrl, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ "gameBoard": message.board }),
			})
				.then((response) => response.json())
				.then((solution) => {
					// Assuming the Python server responds with the solution
					console.log("Received solution from Python:", solution);

					// Now send the solution back to the content script
					chrome.tabs.sendMessage(sender.tab.id, { action: "sendWordsList", solution });
				})
				.catch((error) => {
					console.error("Error communicating with Python server:", error);
				});
			
		}
	}
});


