const nodesCache = createNodesCache([
	'main-container', 'search-options', 'search-results',
	'main-search-field', 'main-search-button',
	'found-num', 'found-show-all-button',
	'testcases-container', 'add-testcase-button', 'see-filtered-button',
	'search-results', 'filtered-num', 'results-container',
	'testcaseTemplate', 'testcaseArgumentFieldTemplate',
	'searchResultAnswerTemplate'
]);

let searchResult = null;

// here will be array with the following structure:
// [ {
//		node: testcaseNode,
//		arguments: [argumentNode1, argumentNode2, ...],
//		output: outputNode
//   },
//   ... ]
let testcaseNodes = [];
let maxTestcaseNumber = 0;

nodesCache['main-search-button'].addEventListener('click', e => {

	let query = nodesCache['main-search-field'].value;
	if (query.length == 0) return false;

	// API CALL: find problem
	// output expected:
	// [
	// 	{
	// 		"href": 'http://...',
	// 		"text": "answer1",
	// 		"likes": 0,
	// 		"date": 1589139954
	// 	},
	// 	{
	// 		"href": 'http://...',
	// 		"text": "answer2",
	// 		"likes": 34,
	// 		"date": 1589139954
	// 	},
	// ...
	// ]
	loader.call('get', 'search', {'query': query})
		.then(
			resolve => { searchResult = null; showTestcases(resolve); },
			reject => console.error(reject)
		);

}, false);

nodesCache['found-show-all-button'].addEventListener('click', e => {

	showAllResults();

}, false);

nodesCache['see-filtered-button'].addEventListener('click', e => {

	let testcases = [];
	// iterate all testcases

	for (let testcase of testcaseNodes){

		testcases.push({
			'arguments': testcase['arguments'].map(node => node.value),
			'output': testcase['output'].value
		});

	}

	// API CALL: get filtered results
	// output expected is the same as in GET http://.../search method
	loader.call('get', 'filter', {'testcases': JSON.stringify(testcases)})
		.then(
			resolve => showFiltered(resolve),
			reject => console.error(reject)
		);

}, false);

nodesCache['add-testcase-button'].addEventListener('click', e => {

	let newTestcase = generateTestcaseNode();
	nodesCache['testcases-container'].insertBefore(newTestcase, e.target);

}, false);

const showTestcases = (response) => {
	
	nodesCache['found-num'].innerHTML = response.length;
	searchResult = response;
	document.body.className = 'testcases';

}

const showAllResults = () => {
	
	document.body.className = 'results';
	showFiltered(searchResult);

}

const showFiltered = (response) => {
	
	nodesCache['filtered-num'].innerHTML = response.length;

	let range = document.createRange();
	range.selectNodeContents(nodesCache['results-container']);
	range.deleteContents();
	
	for (let answer of response) {
		nodesCache['results-container'].appendChild(
			generateAnswerNode(answer));
	}


	document.body.classList = 'results';

}

const putArgumentTypeName = (e, argTypeNode, argErrorNode) => {
	// this function is being used for argument/output field event listeners.
	// it puts name of the argument's type into `argTypeNode` or eror text
	// into `argErrorNode`

	if (e.target.value.length == 0) {
		argTypeNode.classList.add('hidden');
		argErrorNode.classList.add('hidden');
		return;
	}

	let type = parseArgument(e.target.value);
	
	if (!type) {
		argTypeNode.classList.add('hidden');
		argErrorNode.classList.remove('hidden');
	}

	else {
		argTypeNode.classList.remove('hidden');
		argTypeNode.innerHTML = type[0];
		argErrorNode.classList.add('hidden');
	}

}

window.onload = () => {
	// uncomment this code for testing
	showTestcases([
		{
			"href": '#',
			"text": "Test text",
			"likes": 10,
			"date": 1589139954
		},
		{
			"href": '#',
			"text": "Test text",
			"likes": 10,
			"date": 1589139954
		},
		{
			"href": '#',
			"text": "Test text",
			"likes": 10,
			"date": 1589139954
		}
	]);
}
