/*
 * Returns hashmap of [id-of-element, element].
 */
const createNodesCache = ids =>  {

	let cache = {};
	ids.forEach(id => cache[id] = document.getElementById(id));
	return cache;

}

const capitalize = string => {
	return string.charAt(0).toUpperCase() + string.slice(1);
};

/*
 * Recursively check if variable is array and all its elements and subarrays
 * contains either numbers or strings.
 */
const isArray = variable => {

	if ( !Array.isArray(variable) ) return false;

	for (let element of variable) {
		if ( ['number', 'string'].includes(typeof element) )
			continue;
		if ( !isArray(element) ) return false;
	}

	return true;

};

/*
 * Try to parse JSON, return result and its type or false otherwise.
 */
const parseArgument = string => {

	let result = null;

	try { result = JSON.parse(string); }
	catch (SyntaxError) { return false; };

	if (typeof result === 'object')
		return isArray(result)
			? ['Array', result] : false;

	return [ capitalize(typeof result), result ];

}