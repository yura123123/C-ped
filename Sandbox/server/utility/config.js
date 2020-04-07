const fs = require('fs');

const ConfigParser = require('configparser');

const config = new ConfigParser();

const configFileName = "sandbox_config.cfg"
const sharedFileName = "shared_config.cfg"

// Is relative to the directory server.js was run.
const configPath = "../../config"
// const configExamplePath = "../../config/example"

/*
function generateDefault() {
	config.addSection('Server');
	config.set('Server', 'debug', false);

	config.write(configExamplePath + "/" + configFileName);
}
*/

if (fs.existsSync(configPath)) {
  config.read(configPath + "/" + configFileName);
  config.read(configPath + "/" + sharedFileName);
}
else {
	console.error("Config directory does not exist.");
}

module.exports = config
