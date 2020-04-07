/* eslint-env es6, browser */
/* eslint-disable no-console */
/* global io */

const socket = io();

function collectData() {
	return {};
}

function sendData() {
	let data = collectData();
	socket.emit("data", {data: data});
}

window.onload = function() {
};
