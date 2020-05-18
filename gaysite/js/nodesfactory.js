const generateTestcaseArgumentNode = (testcaseNode) => {
	// this code is relate on testcase argument field template

	let template = nodesCache['testcaseArgumentFieldTemplate']
		.content.cloneNode(true);
	let templateRoot = template.querySelector('.argument');
	let templateInput = templateRoot.querySelector('input');

	templateInput.addEventListener('keyup', e => {
		// this listener will create new argument field after you type
		// something into previous one.

		// once field was changes it's not *new* anymore
		if ( e.target.value.length > 0 )
			e.target.classList.remove('new-argument-input');

		// skip *new* fields
		if ( e.target.classList.contains('new-argument-input') ) return;

		if ( testcaseNode.querySelectorAll('.new-argument-input').length == 0 ){
			// add one more *new* field
			testcaseNode.querySelector('.testcase-arguments').appendChild(
				generateTestcaseArgumentNode(testcaseNode));
			// add it to testcaseNodes
			for (let registeredNode of testcaseNodes) {
				if (registeredNode['node'] !== testcaseNode) continue;
				registeredNode.arguments.push(templateInput);
				break;
			}
		}

	}, false)

	templateInput.addEventListener(
		'input',
		e => putArgumentTypeName(
			e,
			templateRoot.querySelector('.argument-type'),
			templateRoot.querySelector('.argument-error')
		),
		false
	);

	templateRoot.querySelector('.delete-argument-button')
		.addEventListener('click', e => {

			// remove from DOM
			if ( !templateInput.classList.contains('new-argument-input') )
				templateRoot.remove();

			// remove from testcaseNodes
			for (let registeredNode of testcaseNodes) {
				if (registeredNode['node'] !== testcaseNode) continue;
				registeredNode['arguments'] = registeredNode['arguments']
					.filter(argument => argument !== templateInput);
				break;
			}

		}, false)

	return templateRoot;

}

const generateTestcaseNode = () => {
	// this code is relate on testcase template

	let template = nodesCache['testcaseTemplate'].content.cloneNode(true);
	let templateRoot = template.querySelector('.testcase');

	let singleArgument = generateTestcaseArgumentNode(templateRoot);
	template.querySelector('.testcase-arguments')
		.appendChild(singleArgument);

	// should remember number in order to find this node later
	templateRoot.testcaseNumber = ++maxTestcaseNumber;
	templateRoot.querySelector('.testcase-number').innerHTML
		= templateRoot.testcaseNumber;

	templateRoot.querySelector('.close-testcase-button')
		.addEventListener('click', e => {
			deleteTestcaseNode(templateRoot);
		}, false);

	templateRoot.querySelector('.testcase-output-field').addEventListener(
		'input',
		e => putArgumentTypeName(
			e,
			templateRoot.querySelector('.output-type'),
			templateRoot.querySelector('.output-error')
		),
		false
	);

	testcaseNodes.push({
		"node": templateRoot,
		"arguments": [],
		"output": template.querySelector('.output')
	});

	return template;

}

const deleteTestcaseNode = (htmlNode) => {

	testcaseNodes = testcaseNodes.filter(testcase => 
		testcase.node.testcaseNumber !== htmlNode.testcaseNumber);

	htmlNode.parentNode.removeChild(htmlNode);

	if (testcaseNodes.length == 0) maxTestcaseNumber = 0;

}

const generateAnswerNode = (data) => {
	// this code is relate on answer template

	let template = nodesCache['searchResultAnswerTemplate']
		.content.cloneNode(true);

	let date = (new Date(data['date'] * 1000)).toLocaleDateString();

	let templateRoot = template.querySelector('.result');
	templateRoot.querySelector('.resultText').innerHTML = data['text'];
	templateRoot.querySelector('.resultText').setAttribute('href', data['href']);
	templateRoot.querySelector('.resultLikes').innerHTML = data['likes'];
	templateRoot.querySelector('.resultDate').innerHTML = date;

	return templateRoot;

}
