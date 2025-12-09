const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const testScript = path.join(__dirname, 'test-build-simple.mjs');

console.log('Running test...');
try {
  const output = execSync(`node "${testScript}"`, {
    encoding: 'utf8',
    cwd: __dirname,
    stdio: 'pipe'
  });
  
  fs.writeFileSync('test-output.txt', output);
  console.log('Test output written to test-output.txt');
  console.log('\n' + output);
} catch (error) {
  const errorOutput = error.stdout + '\n' + error.stderr + '\n' + error.message;
  fs.writeFileSync('test-output.txt', errorOutput);
  console.error('Test failed - output written to test-output.txt');
  console.error(errorOutput);
  process.exit(1);
}
